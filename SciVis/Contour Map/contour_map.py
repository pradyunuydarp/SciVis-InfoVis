import os
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
from PIL import Image
import imageio

# List of dates for which the contour plots will be generated
dates_list = ['2018-07-01', '2018-07-19', '2018-08-06', '2018-08-24',
              '2018-09-11', '2018-09-29', '2018-07-10', '2018-07-28',
              '2018-08-15', '2018-09-02', '2018-09-20']

# Function to create contour plot
def plot_air_temperature_contour(lat, lon, air_temp, title="Air Temperature Contour Map", levels=None):
    X, Y = np.meshgrid(lon, lat)
    air_temp_masked = np.ma.masked_invalid(air_temp)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle='--', linewidth=0.5)

    # Use contour for contour lines
    contour_lines = ax.contour(X, Y, air_temp_masked, cmap='coolwarm', linewidths=1.2, levels=levels)

    cbar = plt.colorbar(contour_lines, ax=ax, orientation='horizontal', fraction=0.046, pad=0.07)
    cbar.set_label("Air Temperature (°C)")

    ax.set_title(title)
    ax.set_xticks(np.arange(-130, -60, 10), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(20, 55, 5), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    plt.tight_layout()

    return fig

# Function to create filled contour plot
def plot_air_temperature_contourf(lat, lon, air_temp, title="Air Temperature Contourf Map", levels=None):
    X, Y = np.meshgrid(lon, lat)
    air_temp_masked = np.ma.masked_invalid(air_temp)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle='--', linewidth=0.5)

    # Use contourf for filled contours
    filled_contours = ax.contourf(X, Y, air_temp_masked, cmap='coolwarm', levels=levels)

    cbar = plt.colorbar(filled_contours, ax=ax, orientation='horizontal', fraction=0.046, pad=0.07)
    cbar.set_label("Air Temperature (°C)")

    ax.set_title(title)
    ax.set_xticks(np.arange(-130, -60, 10), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(20, 55, 5), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    plt.tight_layout()

    return fig

# Find global minimum and maximum temperature across all dates
global_min, global_max = np.inf, -np.inf
for date in dates_list:
    file_name = f"./../sampled_data/{date}.nc"
    nc_file = netCDF4.Dataset(file_name, "r")
    air_temp_list = nc_file.variables["air_temperature"][:]
    air_temp_list = air_temp_list - 273.15  # Convert from Kelvin to Celsius
    current_min = np.nanmin(air_temp_list)
    current_max = np.nanmax(air_temp_list)
    global_min = min(global_min, current_min)
    global_max = max(global_max, current_max)
    nc_file.close()

# Define contour levels based on global min and max temperature
levels = np.linspace(global_min, global_max, 10)

# Create directories to save the plots
contour_dir = "./contour_plots"
contourf_dir = "./contourf_plots"
os.makedirs(contour_dir, exist_ok=True)
os.makedirs(contourf_dir, exist_ok=True)

# Create a list to store the filenames of saved contourf images for the GIF
contourf_image_files = []

# Generate and save contour and contourf plots for each date
for date in dates_list:
    file_name = f"./../sampled_data/{date}.nc"
    nc_file = netCDF4.Dataset(file_name, "r")
    lat_list = nc_file.variables["lat"][:]
    lon_list = nc_file.variables["lon"][:]
    air_temp_list = nc_file.variables["air_temperature"][:] - 273.15  # Convert from Kelvin to Celsius

    # Downsample for visualization (optional)
    lat_downsampled = lat_list[::7]
    lon_downsampled = lon_list[::7]
    air_temp_downsampled = air_temp_list[::7, ::7]

    # Create and save contour plot
    contour_fig = plot_air_temperature_contour(lat_downsampled, lon_downsampled, air_temp_downsampled, title=f"Air Temperature Contour on {date}", levels=levels)
    contour_file = os.path.join(contour_dir, f"{date}_contour.png")
    contour_fig.savefig(contour_file)
    plt.close(contour_fig)

    # Create and save contourf plot
    contourf_fig = plot_air_temperature_contourf(lat_downsampled, lon_downsampled, air_temp_downsampled, title=f"Air Temperature Contourf on {date}", levels=levels)
    contourf_file = os.path.join(contourf_dir, f"{date}_contourf.png")
    contourf_fig.savefig(contourf_file)
    plt.close(contourf_fig)

    # Add the contourf image filename to the list for the GIF
    contourf_image_files.append(contourf_file)

    nc_file.close()

# Create the GIF using the saved contourf images
gif_filename = './contourf_plot_animation.gif'
with imageio.get_writer(gif_filename, mode='I', duration=1) as writer:
    for image_file in contourf_image_files:
        img = Image.open(image_file)
        writer.append_data(np.array(img))

print(f"Contour plots saved in {contour_dir}")
print(f"Contourf plots saved in {contourf_dir}")
print(f"GIF saved as {gif_filename}")
