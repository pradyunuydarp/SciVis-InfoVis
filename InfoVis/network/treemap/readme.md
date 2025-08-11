# COVID-19 Cases Treemap Visualization

This folder contains information about the treemap visualization of COVID-19 cases, showcasing both hierarchical and non-hierarchical views of the data. The hierarchical treemap shows the distribution of cases across regions and months in the USA, while the non-hierarchical treemap provides an overview by country.

### File Descriptions

- **index4.html**: This HTML file contains the code for rendering the hierarchical treemap, which shows COVID-19 cases in the USA organized by region and month. Open this file in a browser to view the hierarchical treemap.
  
- **index5.html**: This HTML file is for the non-hierarchical treemap, visualizing COVID-19 cases by country. Open this file in a browser to see the non-hierarchical treemap.

- **cleandata.ipynb**: This ipynb file was used to isolate a subset from the original data source.

- **hierarchical_data.csv**: The data file used by `index4.html` for hierarchical visualization. This CSV includes columns for regions, months, and case counts in the USA.

- **non-hierarchical_data.csv**: The data file used by `index5.html` for non-hierarchical visualization. This CSV includes country names and corresponding COVID-19 case counts.

- **hierarchical**: Contains screenshots of the hierarchical treemap visualization.
  
- **non-hierarchical**: Contains screenshots of the non-hierarchical treemap visualization.

## Running the Treemap Visualizations

To view the visualizations, simply open the respective HTML file in a web browser. Each HTML file pulls data from its associated CSV file and renders the treemap using JavaScript libraries.

1. **Open Hierarchical Treemap**:
   - Locate `index4.html` in your file explorer.
   - Open this file in any modern browser (e.g., Chrome, Firefox, Edge) to view the hierarchical treemap visualization of COVID-19 cases in the USA by region and month.

2. **Open Non-Hierarchical Treemap**:
   - Locate `index5.html` in your file explorer.
   - Open this file in a modern browser to view the non-hierarchical treemap visualization of COVID-19 cases by country.

### Libraries Used

The visualizations utilize the following libraries:
- **FusionCharts**: For rendering treemap visualizations.
- **PapaParse**: To parse CSV data into a format usable by the JavaScript code.

Ensure that an active internet connection is available, as the HTML files fetch these libraries from CDNs.

## Notes

- The `CSV` files should remain in the same directory as the HTML files to ensure the data loads correctly.
- Images are stored in the `images` directory for reference or documentation purposes.
  
