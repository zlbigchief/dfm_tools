# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 21:59:05 2021

@author: veenstra
"""

import os
import matplotlib.pyplot as plt
plt.close('all')

from dfm_tools.get_nc import get_netdata, get_ncmodeldata, plot_netmapdata
from dfm_tools.get_nc_helpers import get_ncvarproperties
from dfm_tools.regulargrid import scatter_to_regulargrid

dir_testinput = r'c:\DATA\dfm_tools_testdata'
dir_output = '.'

#TODO: contour plot of surfaces (e.g. cotidal chart), with polycollection (FM grid) or regular grid, exclude 'land' (shapely overlap between cells of two grids? or create polygon around all edges of original grid (also islands) and use that to cut the resulting regular grid)

file_nc = os.path.join(dir_testinput,'DFM_3D_z_Grevelingen','computations','run01','DFM_OUTPUT_Grevelingen-FM','Grevelingen-FM_0000_map.nc')
#file_nc = os.path.join(dir_testinput,'DFM_sigma_curved_bend\\DFM_OUTPUT_cb_3d\\cb_3d_map.nc')
#file_nc = 'p:\\1204257-dcsmzuno\\2013-2017\\3D-DCSM-FM\\A17b\\DFM_OUTPUT_DCSM-FM_0_5nm\\DCSM-FM_0_5nm_0000_map.nc'
#file_nc = 'p:\\11205258-006-kpp2020_rmm-g6\\C_Work\\08_RMM_FMmodel\\computations\\run_156\\DFM_OUTPUT_RMM_dflowfm\\RMM_dflowfm_0000_map.nc'

clim_bl = [-40,10]

vars_pd = get_ncvarproperties(file_nc=file_nc)
ugrid = get_netdata(file_nc=file_nc)
#get bed layer
data_frommap_x = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_face_x')
data_frommap_y = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_face_y')
data_frommap_bl = get_ncmodeldata(file_nc=file_nc, varname='mesh2d_flowelem_bl')

for maskland_dist in [None,100]:
    #interpolate to regular grid
    x_grid, y_grid, val_grid = scatter_to_regulargrid(xcoords=data_frommap_x, ycoords=data_frommap_y, ncellx=100, ncelly=80, values=data_frommap_bl, method='linear', maskland_dist=maskland_dist)

    #create plot with ugrid and cross section line
    fig, axs = plt.subplots(3,1,figsize=(6,9))
    ax=axs[0]
    pc = plot_netmapdata(ugrid.verts, values=data_frommap_bl, ax=ax, linewidth=0.5, edgecolors='face', cmap='jet')#, color='crimson', facecolor="None")
    pc.set_clim(clim_bl)
    fig.colorbar(pc, ax=ax)
    ax=axs[1]
    pc = ax.contourf(x_grid, y_grid, val_grid)
    pc.set_clim(clim_bl)
    fig.colorbar(pc, ax=ax)
    ax=axs[2]
    ax.contour(x_grid, y_grid, val_grid)
    fig.colorbar(pc, ax=ax)
    plt.savefig(os.path.join(dir_output,'%s_gridbedcontour_masklanddist%s'%(os.path.basename(file_nc).replace('.',''),maskland_dist)))

