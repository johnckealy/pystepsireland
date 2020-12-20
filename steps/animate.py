
from extrapolation import extrapolate, original_field
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
from utils import find_gridpoint, shell_command
from pysteps.visualization import plot_precip_field
import pprint
import numpy as np
import cartopy.crs as ccrs
from datetime import datetime, timedelta
from glob import glob
import os
import re


fig = plt.figure()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)


def point_value(field, lonpoint, latpoint):
    F = np.load('coords.npz')
    lons = F['lons']
    lats = F['lats']
    lons = np.flipud(lons)
    lats = np.flipud(lats)
    coords = find_gridpoint(lons, lats, lonpoint, latpoint)
    return field[coords]


def animate_extrapolants(ref_date, i, extrapolated_field, metadata, lonpoint, latpoint,):
    fig.clf()
    frame_date = datetime.strptime(ref_date, "%Y%m%d%H%M") + timedelta(minutes=i*5)
    print(f"frame date = {frame_date}")
    plot_precip_field(extrapolated_field, geodata=metadata, map='cartopy', drawlonlatlines=True, cartopy_scale='10m')
    plt.plot(lonpoint, latpoint, color='r', marker='o', transform=ccrs.PlateCarree())
    plt.title(frame_date)
    plt.savefig(f"tmp/Ireland_exp_{frame_date}.png", dpi=300)

def create_extrapolants_gif(ref_date, latpoint, lonpoint, n_leadtimes=3, num_prev_files=3, provider="meteireann"):
    shell_command('mkdir tmp/')
    oe_field, extrapolated_fields, metadata = extrapolate(ref_date, n_leadtimes=n_leadtimes, num_prev_files=num_prev_files, provider=provider)
    for i in range(len(extrapolated_fields)):
        animate_extrapolants(ref_date, i, extrapolated_fields[i, :, :], metadata, lonpoint, latpoint)
    shell_command('convert -delay 50 tmp/Ireland_exp_*.png -loop 0 Ireland_exp.gif')
    shell_command('rm tmp/*')
    shell_command('rmdir tmp/')


def animate_originals(date, lonpoint, latpoint):
    fig.clf()
    o_field, metadata = original_field(date, provider="meteireann")
    cont = plot_precip_field(o_field, geodata=metadata, map="cartopy", drawlonlatlines=True, cartopy_scale='10m')
    point_precip = point_value(o_field, lonpoint, latpoint)
    print(f"Point value at [{lonpoint}, {latpoint}] is {point_precip} mm/hr")
    plt.plot(lonpoint, latpoint, color='r', marker='o', transform=ccrs.PlateCarree())
    plt.title(datetime.strptime(date, "%Y%m%d%H%M"))
    plt.savefig(f"tmp/Ireland_org_{date}.png", dpi=300)

def create_originals_gif(dates, latpoint, lonpoint ):
    shell_command('mkdir tmp/')
    for i,date in enumerate(dates):
        animate_originals(date, lonpoint, latpoint)
    shell_command('convert -delay 50 tmp/Ireland*.png -loop 0 Ireland_org.gif')
    shell_command('rm tmp/*')
    shell_command('rmdir tmp/')



if __name__=="__main__":
    latpoint, lonpoint = 54.304075, -8.541018
    filenames = [os.path.basename(file) for file in glob('/home/jokea/code/pystepsireland/radar/meteireann/20200705/*.hdf')]
    filenames.sort()
    datetimes = [ re.search('\d{14}', filename).group()[:-2] for filename in filenames ]
    datetimes = datetimes[:]
    # breakpoint()
    
    # create_originals_gif(datetimes, latpoint, lonpoint )
    create_extrapolants_gif('202007051610', latpoint, lonpoint, n_leadtimes=15, num_prev_files=len(datetimes)-1)
