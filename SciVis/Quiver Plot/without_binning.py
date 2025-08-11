
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LatitudeFormatter, LongitudeFormatter


# Load the dataset
PATH_TO_DATA = './sampled_data/2018-07-01.nc'
data = xr.open_dataset(PATH_TO_DATA)


# Extract wind speed and direction
wind_speed = data['wind_speed']
wind_dir = data['wind_from_direction']
lat = wind_speed['lat'].values
lon = wind_speed['lon'].values
speed = wind_speed.values
direction = wind_dir.values


# Convert wind direction and speed into u and v components
u = -speed * np.sin(np.radians(direction))
v = -speed * np.cos(np.radians(direction))


# Create the first quiver plot with black arrows and arrow length scaled by speed
fig1, ax1 = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax1.add_feature(cfeature.LAND, color='lightgray')
ax1.coastlines()
ax1.add_feature(cfeature.BORDERS, linestyle=':')

# Add gridlines with formatted latitude and longitude labels
gl = ax1.gridlines(draw_labels=True, color='gray', linestyle='--', linewidth=0.5)
gl.top_labels = gl.right_labels = False
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()

# Plot the quiver with black arrows
# Decrease the scale to reduce arrow size and add transform to keep arrows within projection bounds
ax1.quiver(
    lon, lat, u, v, 
    scale=200, width=0.002, 
    color='black', headlength=3, headaxislength=2, 
    transform=ccrs.PlateCarree()
)
ax1.set_title('Quiver Plot: Arrow Length Represents Wind Speed')


# Create the second quiver plot with arrows colored by wind speed magnitude
fig2, ax2 = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax2.add_feature(cfeature.LAND, color='lightgray')
ax2.coastlines()
ax2.add_feature(cfeature.BORDERS, linestyle=':')

# Add gridlines with formatted latitude and longitude labels
gl = ax2.gridlines(draw_labels=True, color='gray', linestyle='--', linewidth=0.5)
gl.top_labels = gl.right_labels = False
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()

# Plot the quiver with arrows colored by wind speed magnitude using 'viridis' colormap
quiver = ax2.quiver(
    lon, lat, u, v, speed, 
    scale=200, width=0.002, 
    cmap='viridis', headlength=3, headaxislength=2, 
    transform=ccrs.PlateCarree()
)
ax2.set_title('Quiver Plot: Arrow Color Represents Wind Speed (Constant Length)')

# Add color bar to show wind speed magnitude
cbar = plt.colorbar(quiver, ax=ax2, orientation='vertical', label='Wind Speed (m/s)')

# Show both plots
plt.show()
