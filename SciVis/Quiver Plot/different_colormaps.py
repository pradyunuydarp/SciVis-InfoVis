# %% 
import numpy as np 
import matplotlib 
import matplotlib.pyplot as plt 
import xarray as xr 
import cartopy.crs as ccrs 
import cartopy.feature as cfeature 
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter 

# %% 
# Load data 
PATH_TO_DATA = './sampled_data/2018-07-01.nc'
path = PATH_TO_DATA
data = xr.open_dataset(path) 

# Extract wind speed and direction 
wind_speed = data['wind_speed'] 
wind_dir = data['wind_from_direction'] 

# %% 
# Define the bin size for downsampling (e.g., every 2° of lat/lon) 
lat_bin_size = 2 
lon_bin_size = 2 

# %% 
lat = wind_speed['lat'].values 
lon = wind_speed['lon'].values 
speed = wind_speed.values  # Wind speed 
direction = wind_dir.values  # Wind direction in degrees 

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

# Convert wind direction into u and v components (keeping a constant arrow length for plotting) 
constant_speed = 1.5 # This sets the constant magnitude for arrow length 
u_binned_const = -constant_speed * np.sin(np.radians(avg_direction)) 
v_binned_const = -constant_speed * np.cos(np.radians(avg_direction)) 

# Midpoints for lat and lon for plotting 
lat_midpoints = (lat_bins[:-1] + lat_bins[1:]) / 2 
lon_midpoints = (lon_bins[:-1] + lon_bins[1:]) / 2 
lon_mid_grid, lat_mid_grid = np.meshgrid(lon_midpoints, lat_midpoints) 

# %% 
# List of colormaps to use for each subplot 
colormaps = ['viridis', 'plasma', 'inferno', 'cividis'] 

# Create a single figure with 2 rows and 2 columns for the subplots 
fig, axes = plt.subplots(2, 2, figsize=(16, 12), subplot_kw={'projection': ccrs.PlateCarree()}) 

# Flatten the axes array for easy iteration 
axes = axes.flatten() 

# Create plots for each colormap 
for ax, cmap in zip(axes, colormaps): 
    # Add features to the axis 
    ax.add_feature(cfeature.LAND, color='lightgray') 
    ax.coastlines() 
    ax.add_feature(cfeature.BORDERS, linestyle=':') 

    # Add gridlines and format the ticks 
    gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linestyle='--') 
    gl.xlabels_top = False 
    gl.ylabels_right = False 
    gl.xformatter = LongitudeFormatter() 
    gl.yformatter = LatitudeFormatter() 

    # Create quiver plot with constant arrow length and color representing wind speed 
    quiver = ax.quiver( 
        lon_mid_grid, lat_mid_grid, u_binned_const, v_binned_const, avg_speed,  # color based on wind speed
        scale=50, cmap=cmap, width=0.002, headlength=4, headaxislength=3 
    ) 
    
    # Add colorbar to each subplot 
    cbar = plt.colorbar(quiver, ax=ax, orientation='vertical') 
    cbar.set_label('Wind Speed (m/s)') 
    ax.set_title(f'Quiver Plot with Colormap: {cmap} for the date 2018-07-01') 

# Adjust layout to prevent overlapping 
plt.tight_layout() 

# Display the plot 
plt.show()
