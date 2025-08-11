## Parallel Coordinate Plots (PCP)

1. **`containment_pcp.ipynb`**
   - This notebook processes a COVID-19 dataset focused on containment measures across various countries, preparing it for further analysis or visualization.
   - **Data Processing**:
     - Reads a CSV file with data on different containment policies (e.g., school closures, workplace closures).
     - Adds columns for `month` and `year`, later combined into a `Month_Year` column for easy grouping.
     - Removes unnecessary columns, groups data by country and month, and calculates the average containment measure values (e.g., school closings (C1), workplace closings (C2), restrictions on gatherings (C4)).
   - **Output**:
     - Exports a cleaned dataset with selected countries (e.g., Philippines, Chile, Honduras) for monthly average containment measures.
     - Generates a JSON-compatible list structure for potential downstream applications.
     - This process enables tracking of containment policy strictness across countries and time, aiding in understanding pandemic response variations.

2. **`country_cases.ipynb`**
   - This notebook processes a COVID-19 dataset of confirmed cases across various countries, focusing on monthly trends for the top 20 countries.
   - **Data Processing**:
     - Selects the top 20 countries by cases and converts the `Date` column to datetime format.
     - Groups data by country and aggregates on a monthly basis (recording the last confirmed cases at month-end).
     - Creates a dictionary (`country_cases_dict`) mapping each country to its confirmed case data, with missing values filled by the previous month’s value for consistency.
     - Reformats data for specific countries (e.g., Germany, Turkey), and generates an ordered list of dates from March 2020 to June 2021.
   - **Output**:
     - Outputs structured data of confirmed cases over time for each country, suitable for further analysis, visualizations, or as model input.

3. **`pcp_cases.html`**
   - This HTML page creates an interactive visualization of monthly COVID-19 cases for various countries using the Plotly.js library.
   - **Features**:
     - Displays a **Parallel Coordinates Plot (parcoords)** where each line represents a country and each dimension corresponds to the number of confirmed cases at the end of each month (March 2020 - June 2021).
     - Hover functionality shows country names for each line.
   - **Interactivity**:
     - The plot is responsive, adjusting to different screen sizes with customized plot settings (size, background colors, and hover labels).
     - A legend at the bottom indicates each country’s line color, enabling users to interactively explore and compare case trends across countries.

4. **`pcp_containment.html`**
   - This HTML page visualizes "C1 School Closing" policy data over time for various countries.
   - **Visualization**:
     - Uses Plotly.js and D3.js to plot "C1 School Closing" values over multiple months for each country.
     - Each country has a trace on the plot, with months (`Month_Year`) on the x-axis and "C1 School Closing" values on the y-axis.
   - **Interactivity**:
     - Provides a **"dragmode: 'select'"** feature, allowing users to select and focus on specific countries.
     - A plotly_selected event triggers updates, highlighting selected countries and hiding others while retaining legend visibility.
   - **Purpose**:
     - Offers a comparative view of school closure policy evolutions across countries, with flexible focus on specific countries of interest.

## Usage
1. **PCP Folder**:
   - run the command ```sh
                     python -m http.server
                     ```
   - Run the command ```sh
                     python country_cases.py > output.txt
                     ```
   - Copy the output and paste it as the dimensions pcp_cases.html
   - pcp_containment.html dosen't need any such preprocessing   
   - Open the HTML files on the browser to view the plots

## Installation 
1. ```sh
   pip install -r requirements.txt
   ```
