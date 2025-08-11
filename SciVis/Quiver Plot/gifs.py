import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LatitudeFormatter, LongitudeFormatter
import os
import imageio
from PIL import Image

# Directory containing the .nc files
PATH_TO_DATA = './sampled_data/'
data_dir = PATH_TO_DATA

# Output directory for saving plots
output_dir = './output_images/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to find global min and max wind speeds across all files
def find_global_wind_speed_range(files, data_dir):
    global_min = float('inf')
    global_max = float('-inf')
    for file_name in files:
        file_path = os.path.join(data_dir, file_name)
        data = xr.open_dataset(file_path)
        wind_speed = data['wind_speed'].values
        file_min = np.nanmin(wind_speed)
        file_max = np.nanmax(wind_speed)
        global_min = min(global_min, file_min)
        global_max = max(global_max, file_max)
    return global_min, global_max

# List of all files in the directory
files = sorted([f for f in os.listdir(data_dir) if f.endswith('.nc')])

# Find global min and max wind speeds
global_min_speed, global_max_speed = find_global_wind_speed_range(files, data_dir)

# Function to create quiver plots for a given file and save the plots
def create_quiver_plots(file_path, output_image_path_length, output_image_path_color, global_min_speed, global_max_speed, file_name):
    data = xr.open_dataset(file_path)

    # Extracting only the wind speed and direction
    wind_speed = data['wind_speed']
    wind_dir = data['wind_from_direction']

    # Define the bin size for downsampling (e.g., every 2° of lat/lon)
    lat_bin_size = 2.0
    lon_bin_size = 2.0

    # Latitude and longitude from the dataset
    lat = wind_speed['lat'].values
    lon = wind_speed['lon'].values
    speed = wind_speed.values  # Wind speed data
    direction = wind_dir.values  # Wind direction data

    # Create 2D grids for latitudes and longitudes
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    # Bin the latitudes and longitudes
    lat_bins = np.arange(lat.min(), lat.max(), lat_bin_size)
    lon_bins = np.arange(lon.min(), lon.max(), lon_bin_size)

    # Function to average wind speed and direction within each bin
    def bin_average(data, lat, lon, lat_bins, lon_bins):
        binned_data = np.zeros((len(lat_bins) - 1, len(lon_bins) - 1))
        for i in range(len(lat_bins) - 1):
            for j in range(len(lon_bins) - 1):
                mask = (
                    (lat >= lat_bins[i]) & (lat < lat_bins[i+1]) & 
                    (lon >= lon_bins[j]) & (lon < lon_bins[j+1])
                )
                binned_data[i, j] = data[mask].mean() if np.any(mask) else np.nan
        return binned_data

    # Compute binned averages for wind speed and direction
    avg_speed = bin_average(speed, lat_grid, lon_grid, lat_bins, lon_bins)
    avg_direction = bin_average(direction, lat_grid, lon_grid, lat_bins, lon_bins)

    # Convert wind direction and speed into u and v components for both plots
    u_length_based = -avg_speed * np.sin(np.radians(avg_direction))
    v_length_based = -avg_speed * np.cos(np.radians(avg_direction))

    # For color-based quiver plot (constant u and v)
    u_color_based = -np.sin(np.radians(avg_direction))
    v_color_based = -np.cos(np.radians(avg_direction))

    # Use the midpoints of the lat/lon bins for plotting
    lat_midpoints = (lat_bins[:-1] + lat_bins[1:]) / 2
    lon_midpoints = (lon_bins[:-1] + lon_bins[1:]) / 2
    lon_mid_grid, lat_mid_grid = np.meshgrid(lon_midpoints, lat_midpoints)

    # ---- First plot (Arrow length represents wind speed) ----
    fig, ax1 = plt.subplots(1, 1, figsize=(9, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax1.add_feature(cfeature.LAND, color='lightgray')
    ax1.coastlines()
    ax1.add_feature(cfeature.BORDERS, linestyle=':')

    # Add gridlines and format the ticks
    gl1 = ax1.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linestyle='--')
    gl1.xlabels_top = False
    gl1.ylabels_right = False
    gl1.xformatter = LongitudeFormatter()
    gl1.yformatter = LatitudeFormatter()

    quiver_length = ax1.quiver(
        lon_mid_grid, lat_mid_grid, u_length_based, v_length_based, 
        scale=200, width=0.002, headlength=4, headaxislength=3, color='black'
    )
    ax1.set_title(f'Quiver Plot: Length Represents Wind Speed\n{file_name[:-3]}')
    plt.tight_layout()
    plt.savefig(output_image_path_length)
    plt.close()

    # ---- Second plot (Arrow color represents wind speed) ----
    fig, ax2 = plt.subplots(1, 1, figsize=(9, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax2.add_feature(cfeature.LAND, color='lightgray')
    ax2.coastlines()
    ax2.add_feature(cfeature.BORDERS, linestyle=':')

    # Add gridlines and format the ticks
    gl2 = ax2.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linestyle='--')
    gl2.xlabels_top = False
    gl2.ylabels_right = False
    gl2.xformatter = LongitudeFormatter()
    gl2.yformatter = LatitudeFormatter()

    quiver_color = ax2.quiver(
        lon_mid_grid, lat_mid_grid, u_color_based, v_color_based, avg_speed, 
        scale=50, cmap='viridis', width=0.002, headlength=4, headaxislength=3,
        clim=(global_min_speed, global_max_speed)  # Setting constant color scale
    )
    cbar = plt.colorbar(quiver_color, ax=ax2, orientation='vertical')
    cbar.set_label('Wind Speed (m/s)')
    ax2.set_title(f'Quiver Plot: Color Represents Wind Speed (Constant Length)\n{file_name[:-3]}')
    plt.tight_layout()
    plt.savefig(output_image_path_color)
    plt.close()

# Generate a quiver plot for each file and save as two separate images
for idx, file_name in enumerate(files):
    file_path = os.path.join(data_dir, file_name)
    output_image_path_length = os.path.join(output_dir, f'quiver_length_plot_{idx:03d}.png')
    output_image_path_color = os.path.join(output_dir, f'quiver_color_plot_{idx:03d}.png')
    print(f"Processing {file_name} ...")
    create_quiver_plots(file_path, output_image_path_length, output_image_path_color, global_min_speed, global_max_speed, file_name)

# Now, stitch all saved images into two GIFs
length_images = [Image.open(os.path.join(output_dir, f'quiver_length_plot_{idx:03d}.png')) for idx in range(len(files))]
color_images = [Image.open(os.path.join(output_dir, f'quiver_color_plot_{idx:03d}.png')) for idx in range(len(files))]

# Save as GIF using Pillow with control over duration (duration in milliseconds)
gif_path_length = os.path.join(output_dir, 'quiver_length_animation.gif')
gif_path_color = os.path.join(output_dir, 'quiver_color_animation.gif')

length_images[0].save(gif_path_length, save_all=True, append_images=length_images[1:], duration=1000, loop=0)  # 1000ms = 1 second per frame
color_images[0].save(gif_path_color, save_all=True, append_images=color_images[1:], duration=1000, loop=0)  # 1000ms = 1 second per frame

print(f"GIFs saved at {gif_path_length} and {gif_path_color}")
