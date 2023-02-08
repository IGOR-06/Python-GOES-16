#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 18:10:07 2022
@author: igor-06
"""
#---------------------------------------------------------------------------------------------
from netCDF4 import Dataset              # Read / Write NetCDF4 files
import matplotlib.pyplot as plt          # Plotting library
from datetime import datetime, timedelta # Library to convert julian day to dd-mm-yyyy
import cartopy, cartopy.crs as ccrs      # Plot maps
import numpy as np                       # Scientific computing with Python
import cartopy.io.img_tiles as cimgt
from cartopy.feature import ShapelyFeature # importando leitor para shape
from cartopy.io.shapereader import Reader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# =============================================================================
#  Abrir arquivo the GOES-R image
# =============================================================================
file = Dataset("/OR_ABI-L2-CMIPF-M6C11_G16_s20200180500192_e20200180509500_c20200180509589.nc")
# =============================================================================
# # -------------------------- plot colors ----------------------------------
# =============================================================================
# ------------------------ apagar parte da barra de cor
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

ncolors = 256 # get colormap
color_array = plt.get_cmap('gray')(range(ncolors))
color_array[:,-1] = np.linspace(0.0,0.0,ncolors) # change alpha values
map_object = LinearSegmentedColormap.from_list(name='alpha',colors=color_array) # create a colormap object
plt.register_cmap(cmap=map_object)# register this new colormap with matplotlib

# -----------------  colorir parte da barra de cor ----------
gray_cmap = cm.get_cmap('alpha',120)
gray_cmap = gray_cmap(np.linspace(0,1,120))


my_colors2 = cm.get_cmap('gist_ncar',119)
my_colors2 = my_colors2(np.linspace(0,1,119))

gray_cmap[:119,:]=my_colors2
my_cmap2=cm.colors.ListedColormap(gray_cmap)
# =============================================================================
# # -----------------    Get the pixel values  -------------------------
# =============================================================================
data = file.variables['CMI'][:] - 273.15
# =============================================================================
# # Select the extent [min. lon, min. lat, max. lon, max. lat]
# =============================================================================
extent = [-50.0, -30.00, -30.00, -15.00] 
# =============================================================================
# # Choose the plot size (width x height, in inches)
# =============================================================================
googletiles = cimgt.GoogleTiles(desired_tile_form='RGB', style='satellite')
plt.figure(figsize=(8,8))
# Use the Geostationary projection in cartopy
ax = plt.axes(projection=ccrs.PlateCarree())
# =============================================================================
# # Define the image extent
# =============================================================================
img_extent = [extent[0], extent[2], extent[1], extent[3]]
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())
# =============================================================================
# # ----------------  Add a background image  -------------------
# =============================================================================
ax.stock_img()
ax.add_image(googletiles,8)
# =============================================================================
# # Geostationary extent
# =============================================================================
img_extent = (-5434894.67527,5434894.67527,-5434894.67527,5434894.67527)
# =============================================================================
# # Plot the image
# =============================================================================
img = ax.imshow(data, vmin=-80, vmax=0, origin='upper', cmap=my_cmap2, 
                transform=ccrs.Geostationary(central_longitude=-75.0), extent=img_extent,zorder=2)
# =============================================================================
# # ----------------------------- add shapefile
# =============================================================================
###### importando linha de shapes
mapa_amsul = ShapelyFeature(Reader('/amsulrp2.shp').geometries(),
                            ccrs.PlateCarree(),
                            edgecolor='white',
                            linewidth=1,
                            facecolor='None',
                            zorder=2)
ax.add_feature(mapa_amsul)
# =============================================================================
# ax.gridlines(color='white', alpha=0.5, linestyle='--', linewidth=0.5, xlocs=np.arange(-180, 180, 15), ylocs=np.arange(-180, 180, 15), draw_labels=False)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
gl.xlabel_style = {'color': 'black', 'weight': 'bold','fontsize': 10}
gl.ylabel_style = {'color': 'black', 'weight': 'bold','fontsize': 10}
gl.top_labels = False
gl.right_labels = False
# =============================================================================
# # ------------------   Add a colorbar ----------------------------
# =============================================================================
plt.colorbar(img, label='Brightness Temperatures (°C)', extend='both', orientation='horizontal', pad=0.05, fraction=0.05)
# =============================================================================
# # Getting the ABI file date
# =============================================================================
add_seconds = int(file.variables['time_bounds'][0])
date = datetime(2000,1,1,12) + timedelta(seconds=add_seconds)
date_format = date.strftime('%B %d %Y - %H:%M UTC')
datahora = date.strftime('%Y_%m_%d_%H_%M')
# =============================================================================
# # ------------------   Add a title  ------------------------
# =============================================================================
ax.set_title('GOES-16 (Cylindrical Projection)\nBand 11 (8.40 µm)', fontweight='bold', fontsize=10, loc='left')
ax.set_title('Full Disk \n' + date_format, fontsize=10, loc='right')
# =============================================================================
# # ---------------------------  Save the image  ----------------------------
# =============================================================================
plt.show()  
# plt.savefig(f'/GOES_16_band_11_v2_{datahora}_.png', bbox_inches='tight', pad_inches=0.2, dpi=600)
