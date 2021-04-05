import geopandas as gpd
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

join_total = join['Population'].sum()

new_join = join.groupby(['CountyName', 'Ward'])['Population'].sum()

print('{}  is the largest ward with'.format(new_join.max()))