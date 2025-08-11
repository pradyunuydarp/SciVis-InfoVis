# Air Temperature Contour Map Analysis (July - September 2018)

This project provides an analysis of air temperature variations across the United States for the period of July to September 2018 using contour plots. The visualization highlights temperature patterns, with notable observations in the southwestern U.S., where elevated temperatures are likely linked to California forest fires during this time. Similar observations are supported by heatmap and quiver plot analyses.

## Project Structure

The project is organized as follows:

### 1. fill/
This directory contains contour plots with filled color maps, which provide a continuous gradient to represent temperature variations across the U.S., aiding in the visualization of regional temperature distribution.

- **Subfolders by Color Map**:
  - Each subfolder (e.g., `coolwarm`, `viridis`, etc.) contains contour fill images generated for each date from July to September 2018.
  - Different color maps are used to analyze which is most effective for identifying temperature trends.

### 2. marching-squares/
This directory includes contour plots without filled color maps, displaying only contour lines. This style allows for a comparison of visibility and interpretability compared to filled contour maps.

- **Subfolders by Color Map**:
  - Each subfolder contains non-contour fill images for each date, using various color maps for direct comparison with the contour fill maps.

### 3. subplots/
This folder contains comparison images that illustrate the differences between contour fill and non-contour fill plots across various color maps. These comparisons help determine the effectiveness of filled versus unfilled contours for data interpretation.

### 4. contour_map.py
Two methods are used, one for generating contour fill maps, and another for maps without contour fill (marching squares only). Different parameters can be changed to obtain maps of varying levels, colourmaps. The different plots generated and enclosed within the folders were created in this manner by changing the parameters of these functions manually.

### 5. gifs/
This folder contains two animated GIFs, one for contour fill and another for non-contour fill plots. Each GIF shows the progression of air temperature changes over time from July to September 2018.

   - **`contour_fill.gif`**: Animated sequence of contour fill plots.
   - **`non_contour_fill.gif`**: Animated sequence of non-contour fill plots.

## Observations

From the contour plots, a consistent pattern of elevated temperatures in the southwestern part of the U.S. is observed, likely due to the California forest fires during the summer of 2018. The filled contour maps provide a more continuous and easily interpretable view of temperature gradients, while the non-contour fill maps, though less visually continuous, allow for precise delineation of contour lines.

## Usage

1. **View Contour Maps**: Browse the `contour_fill/` and `non_contour_fill/` folders to explore different color maps and observe temperature distribution for each date.
2. **Run the Notebook**: Open `contour_map.ipynb` to regenerate plots or adjust visualization settings such as color maps, contour levels, or projection style.
3. **Compare Animated Plots**: Review the GIFs in `gifs/` to analyze temporal changes in temperature over the period.

## How to run the code
```
python -r requirements.txt
python3 contour_map.py
```

This will create 2 folders, one with images of contour maps using contourfill, one without. The GIF is created only for contour fill method.
