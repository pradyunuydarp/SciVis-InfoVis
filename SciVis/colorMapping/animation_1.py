import xarray as xr
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.colors import ListedColormap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

def load_dataset(folder):
    dataset = {}
    for i in os.listdir(folder):
        if i.endswith(".nc"):
            ds = xr.open_dataset(f"{folder}/{i}")
            add_calculated_field(ds)
            ds = normalize_data(ds)
            dataset[i.replace(".nc", "")] = ds
    return dataset

def normalize_data(ds):
    return (ds - ds.min()) / (ds.max() - ds.min())

def add_calculated_field(ds):
    ds["Correlation Hazard Score"]=(ds["air_temperature"]*0.1-0.73*ds["precipitation_amount"]-0.38*ds["relative_humidity"]+0.34*ds["potential_evapotranspiration"]+0.22*ds["wind_speed"]+0.36*ds["energy_release_component-g"])/(0.1+0.73+0.38+0.34+0.22+0.36)

def plot_variable_over_time(dataset, variable_name, title, cmap, ax, date_index, frame, log_scale=False, discrete=False, num_levels=10, add_color_bar=False):
    data_stack = xr.concat([dataset[key][variable_name] for key in dataset], dim='time')
    data = data_stack.isel(time=frame)

    if log_scale:
        data = np.log1p(data)

    if discrete:
        cmap = ListedColormap(plt.get_cmap(cmap)(np.linspace(0, 1, num_levels)))
    else:
        cmap = plt.get_cmap(cmap)

    # Create a GeoAxes instead of regular axes
    # ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.COASTLINE)

    # Extract latitude and longitude
    lats = data.lat.values
    lons = data.lon.values

    # Plot the data with actual geo coordinates
    img = ax.pcolormesh(lons, lats, data.values, transform=ccrs.PlateCarree(), 
                        cmap=cmap, shading='auto')
    
    # Set up longitude and latitude gridlines with formatting
    ax.gridlines(draw_labels=True, 
                 linewidth=1, 
                 color='gray', 
                 alpha=0.5, 
                 linestyle='--',
                 xformatter=LongitudeFormatter(),
                 yformatter=LatitudeFormatter())
    
    ax.set_title(f"{title} - {date_index[frame]}")
    
    if add_color_bar:
        plt.colorbar(img, ax=ax, fraction=0.046, pad=0.04, shrink=0.7)

def save_images(output_dir, dataset, date_index, num_images=10, cmap="viridis", log_scale=False, discrete=False, num_levels=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for frame in range(min(num_images, len(date_index))):
        # Create figure with Cartopy projection subplots
        fig = plt.figure(figsize=(12, 12))
        
        # Add subplots with PlateCarree projection
        ax1 = fig.add_subplot(2, 1, 1, projection=ccrs.PlateCarree())
        ax2 = fig.add_subplot(2, 1, 2, projection=ccrs.PlateCarree())

        plot_variable_over_time(dataset, "burning_index_g", "Burning Index", cmap, ax1, date_index, frame,
                                log_scale=log_scale, discrete=discrete, num_levels=num_levels, add_color_bar=True)
        plot_variable_over_time(dataset, "Correlation Hazard Score", "Correlation Hazard Score", cmap, ax2, date_index, frame,
                                log_scale=log_scale, discrete=discrete, num_levels=num_levels, add_color_bar=True)

        file_path = os.path.join(output_dir, f"frame_{frame}.png")
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close(fig)

if __name__ == "__main__":
    dataset = load_dataset("../sampled_data")
    date_index = list(dataset.keys())

    output = [
        {"output_dir": "bad_corr_fig_inferno", "cmap": "inferno", "log_scale": False, "discrete": False},
        
    ]
    for out in output:
        save_images(out["output_dir"], dataset, date_index, cmap=out["cmap"], log_scale=out["log_scale"], discrete=out["discrete"])
