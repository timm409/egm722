import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches

counties = gpd.read_file('data_files/Counties.shp')
counties = counties.to_crs(epsg=2157)
wards = gpd.read_file('data_files/NI_Wards.shp')
wards = wards.to_crs(epsg=2157)

# your analysis goes here...

sum_wards = wards['Population'].sum()

join = gpd.sjoin(counties, wards, how='inner', lsuffix='left', rsuffix='right')

new_join = join.groupby(['CountyName'])['Population'].sum()

print(new_join)

wardpop = wards.groupby(['Ward'], as_index=False)['Population'].sum()

print('The ward with the largest population is {}'.format(wardpop.max()))
print('The ward with the smallest population is {}'.format(wardpop.min()))

join_total = join['Population'].sum()

clipped = []
for county in counties['CountyName'].unique():
    tmp_clip = gpd.clip(wards, counties[counties['CountyName'] == county])
    for i, row in tmp_clip.iterrows():
        tmp_clip.loc[i, 'CountyName'] = county
    clipped.append(tmp_clip)

clipped_gdf = gpd.GeoDataFrame(pd.concat(clipped))
clip_total = clipped_gdf['Population'].sum()

print(join_total / clip_total)

