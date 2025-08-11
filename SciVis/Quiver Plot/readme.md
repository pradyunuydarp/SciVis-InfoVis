## Quiver Plots

1. **`different_color_maps.py`**
   - This script creates a set of quiver plots visualizing wind speed and direction data from a NetCDF dataset. 
   - **Libraries used**: `xarray` for loading the dataset, `pandas` for binning, and `matplotlib` with `cartopy` for geographic plotting.
   - **Data Processing**: 
     - Extracts wind speed and direction.
     - Bins latitude and longitude into 2-degree intervals.
     - Groups data to calculate the mean wind speed and direction within each bin.
   - **Visualization**:
     - Generates four quiver plots on a 2x2 grid, each with a different colormap (`viridis`, `plasma`, `inferno`, and `cividis`).
     - Quiver arrows represent wind direction, while color indicates wind speed.
     - Each subplot includes coastlines, borders, and formatted tick labels for latitude and longitude, displayed on a geographic projection.

2. **`quiver_plot.ipynb`**
   - This Jupyter Notebook visualizes wind speed and direction from a NetCDF dataset as a quiver plot.
   - **Data Processing**:
     - Downsamples the dataset into 2-degree latitude and longitude bins, calculating average wind speed and direction within each bin.
     - Converts wind direction into vector components (u and v) for plotting.
   - **Visualization**:
     - The length of each arrow in the quiver plot is proportional to wind speed (longer arrows indicate stronger winds).
     - Uses `scale_units='xy'` for consistent geographic scaling, and `scale=None` to keep arrow length directly proportional to wind speed.
     - Rendered on a geographic map with coastlines and borders for context, showing intuitive wind patterns across the region.

3. **`gifs.py`**
   - This script generates animated GIFs of wind speed and direction from a series of NetCDF files.
   - **Workflow**:
     - Scans the dataset directory and calculates global minimum and maximum wind speeds to standardize color scaling.
     - For each file:
       - Downscales data into 2-degree bins, averaging wind speed and direction within each bin.
       - Creates two types of quiver plots:
         - One with arrow length indicating wind speed.
         - One with constant arrow length, with color indicating wind speed.
     - **Output**:
       - Saves each plot as an image.
       - Combines images into two GIF animations, providing visual representations of wind patterns over time, using both speed-based length and color coding for wind intensity.

## Usage

1. **Containment_pcp.ipynb**:
   - Open the notebook in Jupyter.
   - Run the cells sequentially to process the data and generate the Parallel Coordinates Plot.

2. **Country_Cases.ipynb**:
   - Open the notebook in Jupyter.
   - Run the cells sequentially to analyze and visualize the confirmed COVID-19 cases data.

3. **gifs.py**:
   - Run the script using Python:
     ```sh
     python gifs.py
     ```
   - Ensure that the required NetCDF files are in the specified data directory.

4. **different_colormaps.py**:
   - Run the script using Python:
     ```sh
     python different_colormaps.py
     ```
   - Ensure that the required NetCDF files are in the specified data directory.

## Installation

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>

2. ```sh
   pip install -r requirements.txt
   ```
