# InfoVis Network 
## Directory Structure

```
InfoVis/
    network/
        data_preparation.py
        dataset/
        figs/
        workbook.gephi
```

## Files

### `data_preparation.py`

This script is responsible for preparing the network data for visualization. It involves tranforming column headers and adding additional features like impact score. 

### dataset/



This directory contains the raw and processed datasets used for network visualization. The data files in this directory are used by the `data_preparation.py` script. [Reddit Hyperlink dataset](https://snap.stanford.edu/data/soc-RedditHyperlinks.html) was used for the analysis. Only a sample format of the dataset is uploaded onto github as the files are very large.
### figs



This directory contains figures and visualizations generated from the network data using gephi. These figures can be used for analysis and presentation purposes.

### workbook.gephi

This is a Gephi workbook file that contains the network visualization. Gephi is an open-source network analysis and visualization software. The workbook can be opened in Gephi to explore and analyze the network data visually.

## Usage
## Requirements

1. ```bash
   pip install pandas
   ```
2. Gephi software

### Data Preparation

To prepare the network data, run the `data_preparation.py` script. This script will load the raw data, clean it, and transform it into a format suitable for network visualization.

```sh
python data_preparation.py
```

### Network Visualization

To visualize the network data, open the ```workbook.gephi``` file in Gephi. This file contains the network visualization and can be used to explore and analyze the network data interactively.
