import xarray as xr
import os
import pandas as pd
# Load the data
def slice_data(ds,days=("2018-07-01","2018-09-30")):
    return ds.sel(day=slice(*days))



def create_new_dataset(files):
    for file in files:
        ds = xr.open_dataset("./dataset/"+file)
        
        ds = slice_data(ds)
        ds.to_netcdf("./modified_dataset/"+file)

def sample_and_combine(file_paths):
    datasets = {name: xr.open_dataset("./modified_dataset/"+path) for name, path in file_paths.items()}
    time_samples = datasets['bi'].day.values  
    sampled_dates = time_samples[::len(time_samples) // 10]  # Sample 10 time points

    
    output_dir = "sampled_data"
    os.makedirs(output_dir, exist_ok=True)

   
    for date in sampled_dates:
        
        daily_datasets = {name: ds.sel(day=date) for name, ds in datasets.items()}
        
        daily_combined_ds = xr.merge([ds for ds in daily_datasets.values()],compat="override")
        date=str(date).split('T')[0]
        daily_combined_ds.to_netcdf(f"{output_dir}/{date}.nc")

if __name__=="__main__":
    files = os.listdir("dataset")    
    os.makedirs("modified_dataset",exist_ok=True)
    file_paths = {
    'bi': 'bi_2018.nc',
    'erc': 'erc_2018.nc',
    'etr': 'etr_2018.nc',
    'fm100': 'fm100_2018.nc',
    'fm1000': 'fm1000_2018.nc',
    'pet': 'pet_2018.nc',
    'pr': 'pr_2018.nc',
    'rmax': 'rmax_2018.nc',
    'rmin': 'rmin_2018.nc',
    'sph': 'sph_2018.nc',
    'srad': 'srad_2018.nc',
    'th': 'th_2018.nc',
    'tmmx': 'tmmx_2018.nc',
    'vpd': 'vpd_2018.nc',
    'vs': 'vs_2018.nc'
}
    create_new_dataset(files)

    sample_and_combine(file_paths)
