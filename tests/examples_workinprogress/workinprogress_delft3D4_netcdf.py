# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 21:54:57 2021

@author: veenstra


to get delft3D to write netCDF output instead of .dat files, add these lines to your mdf:
    FlNcdf= #maphis#
    ncFormat=4

"""

import os
import numpy as np
#import datetime as dt
import matplotlib.pyplot as plt
plt.close('all')
from pathlib import Path
import xarray as xr #TODO: convert to xarray

from dfm_tools.get_nc import get_ncmodeldata#, get_netdata, plot_netmapdata
from dfm_tools.get_nc_helpers import get_ncvarproperties
from dfm_tools.regulargrid import uva2xymagdeg
from dfm_tools.hydrolib_helpers import pointlike_to_DataFrame

from hydrolib.core.io.polyfile.models import PolyFile

dir_testinput = r'c:\DATA\dfm_tools_testdata'
dir_output = '.'

file_ldb = Path(r'p:\archivedprojects\1220688-lake-kivu\3_modelling\1_FLOW\4_CH4_CO2_included\008\lake_kivu_geo.ldb')
polyfile_object = PolyFile(file_ldb)
data_ldb = pointlike_to_DataFrame(polyfile_object.objects[0])

file_nc = r'p:\archivedprojects\1220688-lake-kivu\3_modelling\1_FLOW\7_heatfluxinhis\062_netcdf\trim-thiery_002_coarse.nc'
vars_pd = get_ncvarproperties(file_nc=file_nc)
data_xr = xr.open_dataset(file_nc)
#data_xr = data_xr.set_coords(['x','y','edge_x','edge_y'])

"""
#mask variables correctly, then bfill
mask_XY = (data_xr.KCS==0).drop(['XZ','YZ']) #TODO: have to drop coords somehow, otherwise they are removed from variable with where
#mask_XY = (data_xr.XZ==0) & (data_xr.YZ==0)
data_xr['XZ'] = data_xr.XZ.where(~mask_XY)
data_xr['YZ'] = data_xr.YZ.where(~mask_XY)
#data_xr['XZ'] = data_xr.XZ.ffill(dim='M').ffill(dim='N').bfill('M').bfill('N')
#data_xr['YZ'] = data_xr.YZ.ffill(dim='M').ffill(dim='N').bfill('M').bfill('N')

mask_XYCOR = (data_xr.XCOR==-999.999) & (data_xr.YCOR==-999.999)
mask_XYCOR = (data_xr.XCOR==0) & (data_xr.YCOR==0)
data_xr['XCOR'] = data_xr.XCOR.where(~mask_XYCOR)
data_xr['YCOR'] = data_xr.YCOR.where(~mask_XYCOR)
#data_xr['XCOR'] = data_xr.XZ.ffill(dim='M').ffill(dim='N').bfill('M').bfill('N')
#data_xr['YCOR'] = data_xr.YZ.ffill(dim='M').ffill(dim='N').bfill('M').bfill('N')
"""

data_nc_XZ = get_ncmodeldata(file_nc=file_nc, varname='XZ')
data_nc_YZ = get_ncmodeldata(file_nc=file_nc, varname='YZ')
data_nc_XCOR = get_ncmodeldata(file_nc=file_nc, varname='XCOR')
data_nc_YCOR = get_ncmodeldata(file_nc=file_nc, varname='YCOR')
data_nc_ALFAS = get_ncmodeldata(file_nc=file_nc, varname='ALFAS') #contains rotation of all cells wrt real world
#data_nc_S1 = get_ncmodeldata(file_nc=file_nc, varname='S1',timestep='all')
data_nc_QNET = get_ncmodeldata(file_nc=file_nc, varname='QNET',timestep='all')
data_nc_DPV0 = get_ncmodeldata(file_nc=file_nc, varname='DPV0')
#data_nc_QEVA = get_ncmodeldata(file_nc=file_nc, varname='QEVA',timestep='all')
data_nc_KCU = get_ncmodeldata(file_nc=file_nc, varname='KCU')
data_nc_KCV = get_ncmodeldata(file_nc=file_nc, varname='KCV')

layno=-2


data_nc_U1 = get_ncmodeldata(file_nc=file_nc, varname='U1',timestep='all',layer=layno)
data_nc_V1 = get_ncmodeldata(file_nc=file_nc, varname='V1',timestep='all',layer=layno)

mask_XY = (data_nc_XZ==0) & (data_nc_YZ==0)
data_nc_XZ[mask_XY] = np.nan
data_nc_YZ[mask_XY] = np.nan
mask_XYCOR = (data_nc_XCOR<=-999.999) & (data_nc_YCOR<=-999.999)
data_nc_XCOR[mask_XYCOR] = np.nan
data_nc_YCOR[mask_XYCOR] = np.nan


fig, ax = plt.subplots()
ax.plot(data_nc_XCOR,data_nc_YCOR,'-b',linewidth=0.2)
ax.plot(data_nc_XCOR.T,data_nc_YCOR.T,'-b',linewidth=0.2)
ax.set_aspect('equal')
plt.savefig(os.path.join(dir_output,'kivu_mesh'))

fig, axs = plt.subplots(1,3, figsize=(16,7))
for iT, timestep in enumerate([1,10,15]):
    ax=axs[iT]
    vel_x, vel_y, vel_magn, direction_naut_deg = uva2xymagdeg(U1=data_nc_U1[timestep,0,:,:],V1=data_nc_V1[timestep,0,:,:],ALFAS=data_nc_ALFAS)#,
    #                                                          KCU=data_nc_KCU, KCV=data_nc_KCV)
    #pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,direction_naut_deg[1:,1:],cmap='jet')
    #pc.set_clim([0,360])
    pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,vel_magn[1:,1:],cmap='jet')
    pc.set_clim([0,0.15])
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('velocity magnitude (%s)'%(data_nc_U1.var_ncattrs['units']))
    ax.set_title('t=%d (%s)'%(timestep, data_nc_U1.var_times.iloc[timestep]))
    ax.set_aspect('equal')
    ax.quiver(data_nc_XZ[::2,::2], data_nc_YZ[::2,::2], vel_x[::2,::2], vel_y[::2,::2], 
              scale=3,color='w',width=0.005)#, edgecolor='face', cmap='jet')
fig.tight_layout()
plt.savefig(os.path.join(dir_output,'kivu_velocity_pcolor'))

fig, axs = plt.subplots(1,3, figsize=(16,7))
for iT, timestep in enumerate([1,10,15]):
    ax=axs[iT]
    vel_x, vel_y, vel_magn, direction_naut_deg = uva2xymagdeg(U1=data_nc_U1[timestep,0,:,:],V1=data_nc_V1[timestep,0,:,:],ALFAS=data_nc_ALFAS)#,
    #                                                          KCU=data_nc_KCU, KCV=data_nc_KCV)
    #pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,vel_magn[1:,1:],cmap='jet')
    ax.set_title('t=%d (%s)'%(timestep, data_nc_U1.var_times.iloc[timestep]))
    ax.set_aspect('equal')
    pc = ax.quiver(data_nc_XZ[::2,::2], data_nc_YZ[::2,::2], vel_x[::2,::2], vel_y[::2,::2], vel_magn[::2,::2],
              scale=3,color='w',width=0.005, edgecolor='face', cmap='jet')
    pc.set_clim([0,0.15])
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('velocity magnitude (%s)'%(data_nc_U1.var_ncattrs['units']))
fig.tight_layout()
plt.savefig(os.path.join(dir_output,'kivu_velocity'))

#QNET
fig, axs = plt.subplots(1,3, figsize=(16,7))
for iT, timestep in enumerate([1,10,15]):
    ax=axs[iT]
    pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,data_nc_QNET[iT,1:,1:],cmap='jet') #TODO: part of data is removed, not desireable. also using cor instead of cen.
    pc.set_clim([-60,60])
    cbar = fig.colorbar(pc, ax=ax)
    cbar.set_label('%s (%s)'%(data_nc_QNET.var_varname, data_nc_QNET.var_ncattrs['units']))
    ax.set_title('t=%d (%s)'%(timestep, data_nc_QNET.var_times.iloc[timestep]))
    ax.set_aspect('equal')
fig.tight_layout()
plt.savefig(os.path.join(dir_output,'kivu_Qnet'))

#BED
fig, ax = plt.subplots(figsize=(6,8))
pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,data_nc_DPV0[1:,1:],cmap='jet') #TODO: part of data is removed, not desireable. also using cor instead of cen.
cbar = fig.colorbar(pc, ax=ax)
cbar.set_label('%s (%s)'%(data_nc_DPV0.var_varname, data_nc_DPV0.var_ncattrs['units']))
ax.set_aspect('equal')
fig.tight_layout()
plt.savefig(os.path.join(dir_output,'kivu_bedlevel'))



#from MAP DATA CURVEDBEND
file_nc = os.path.join(dir_testinput,'D3D_3D_sigma_curved_bend_nc\\trim-cb2-sal-added-3d.nc')
vars_pd = get_ncvarproperties(file_nc=file_nc)

data_nc_XZ = get_ncmodeldata(file_nc=file_nc, varname='XZ')
data_nc_YZ = get_ncmodeldata(file_nc=file_nc, varname='YZ')
data_nc_XCOR = get_ncmodeldata(file_nc=file_nc, varname='XCOR')
data_nc_YCOR = get_ncmodeldata(file_nc=file_nc, varname='YCOR')
data_nc_ALFAS = get_ncmodeldata(file_nc=file_nc, varname='ALFAS') #contains rotation of all cells wrt real world
data_nc_U1 = get_ncmodeldata(file_nc=file_nc, varname='U1',timestep='all',layer='all')
data_nc_V1 = get_ncmodeldata(file_nc=file_nc, varname='V1',timestep='all',layer='all')
#data_nc_S1 = get_ncmodeldata(file_nc=file_nc, varname='S1',timestep='all')
data_nc_KCU = get_ncmodeldata(file_nc=file_nc, varname='KCU')
data_nc_KCV = get_ncmodeldata(file_nc=file_nc, varname='KCV')

mask_XY = (data_nc_XZ==0) & (data_nc_YZ==0)
data_nc_XZ[mask_XY] = np.nan
data_nc_YZ[mask_XY] = np.nan
mask_XYCOR = (data_nc_XCOR==0) & (data_nc_YCOR==0)
data_nc_XCOR[mask_XYCOR] = np.nan
data_nc_YCOR[mask_XYCOR] = np.nan
#masking should work but quiver does not read masks for X and Y, so use own
#data_nc_XZ.mask = mask_XY
#data_nc_YZ.mask = mask_XY

fig, ax = plt.subplots()
ax.plot(data_nc_XCOR,data_nc_YCOR,'-b',linewidth=0.2)
ax.plot(data_nc_XCOR.T,data_nc_YCOR.T,'-b',linewidth=0.2)
ax.set_aspect('equal')
lim_x = [0,4100]
lim_y = [0,4100]
ax.set_xlim(lim_x)
ax.set_ylim(lim_y)
plt.savefig(os.path.join(dir_output,'curvedbend_mesh'))

txt_abcd = 'abcdefgh'
var_clim = [0,1.2]
ncols=2
fig, axs = plt.subplots(2,ncols, figsize=(8.6,8))
fig.suptitle('velocity magnitude on four times')
for iT, timestep in enumerate([0,1,2,4]):
    id0 = int(np.floor(iT/ncols))
    id1 = iT%ncols
    #print('[%s,%s]'%(id0,id1))
    ax=axs[id0,id1]
    vel_x, vel_y, vel_magn, direction_naut_deg = uva2xymagdeg(U1=data_nc_U1[timestep,9,:,:],V1=data_nc_V1[timestep,9,:,:],ALFAS=data_nc_ALFAS)#,
    #                                                          KCU=data_nc_KCU, KCV=data_nc_KCV)
    pc = ax.pcolor(data_nc_XCOR,data_nc_YCOR,vel_magn[1:,1:],cmap='jet') #TODO: part of data is removed, not desireable
    pc.set_clim(var_clim)
    #cbar = fig.colorbar(pc, ax=ax)
    #cbar.set_label('velocity magnitude (%s)'%(data_nc_U1.var_ncattrs['units']))
    #ax.set_title('t=%d (%s)'%(timestep, data_nc_U1.var_times.iloc[timestep]))
    ax.set_aspect('equal')
    #ax.quiver(data_nc_XZ[::2,::2], data_nc_YZ[::2,::2], vel_x[::2,::2], vel_y[::2,::2],
    #          scale=15,color='w',width=0.005)#, edgecolor='face', cmap='jet')
    ax.quiver(data_nc_XZ, data_nc_YZ, vel_x, vel_y,
              scale=25,color='w',width=0.003)#, edgecolor='face', cmap='jet')
    #add grid
    ax.plot(data_nc_XCOR,data_nc_YCOR,'-b',linewidth=0.2)
    ax.plot(data_nc_XCOR.T,data_nc_YCOR.T,'-b',linewidth=0.2)
    #additional figure formatting to tweak the details
    ax.grid(alpha=0.4)
    if id1 != 0:
        ax.get_yaxis().set_ticklabels([])
    else:
        ax.set_ylabel('y dist', labelpad=-0.5)
    if id0 == 0:
        ax.get_xaxis().set_ticklabels([])
    else:
        ax.set_xlabel('x dist')
    ax.tick_params(axis='x', labelsize=9)
    ax.tick_params(axis='y', labelsize=9)
    lim_x = [0,4100]
    lim_y = [0,4100]
    ax.set_xlim(lim_x)
    ax.set_ylim(lim_y)
    ax.text(lim_x[0]+0.02*np.diff(lim_x), lim_y[0]+0.95*np.diff(lim_y), '%s) t=%d (%s)'%(txt_abcd[iT],timestep, data_nc_U1.var_times.iloc[timestep]),fontweight='bold',fontsize=12)
fig.tight_layout()
#additional figure formatting to tweak the details
plt.subplots_adjust(left=0.07, right=0.90, bottom=0.065, top=0.95, wspace=0.03, hspace=0.04)
cbar_ax = fig.add_axes([0.91, 0.065, 0.02, 0.885])
cbar = fig.colorbar(pc, cax=cbar_ax, ticks=np.linspace(var_clim[0],var_clim[1],7))
#cbar_ax.set_xlabel('[%s]'%(data_nc_U1.var_ncattrs['units']))
cbar_ax.set_ylabel('velocity magnitude [%s]'%(data_nc_U1.var_ncattrs['units']))
plt.savefig(os.path.join(dir_output,'curvedbend_velocity_pcolor'))


