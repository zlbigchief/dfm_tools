# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 15:13:45 2022

@author: veenstra
"""

#WARNING: the resulting grid might not be orthogonal

import xarray as xr #pip install xarray
import hatyan #pip install hatyan

#file_nc = r'p:\1230882-emodnet_hrsm\GTSMv5.0\runs\GM42_2000m_eu0900m_ITfac6p0_wx\gtsm_200s_2000m_eu0900m_ca2000m_v4_0003_net.nc'
#data_xr = xr.open_dataset(file_nc)
#varlist = data_xr.variables.mapping.keys()
#print(data_xr['wgs84'])

file_nc = r'p:\11206813-006-kpp2021_rmm-2d\C_Work\31_RMM_FMmodel\computations\model_setup\run_206_2013\rmm_v1p7_0000_net.nc' #file with projected coordinate system
data_xr = xr.open_dataset(file_nc,drop_variables=['projected_coordinate_system'])
varlist = data_xr.variables.mapping.keys()

for varname_x in ['mesh2d_enc_x','NetNode_x','NetLinkContour_x','NetLink_xu']:
    varname_y = varname_x.replace('_x','_y')
    var_x = data_xr[varname_x]
    var_y = data_xr[varname_y]
    var_x_out, var_y_out = hatyan.convert_coordinates(var_x, var_y, epsg_in=28992, epsg_out=4326)
    data_xr[varname_x].data = var_x_out
    data_xr[varname_x].attrs['units'] = 'degrees_east'
    data_xr[varname_x].attrs['standard_name'] = 'longitude'
    data_xr[varname_x].attrs['long_name'] = 'longitude'
    data_xr[varname_y].data = var_y_out
    data_xr[varname_y].attrs['units'] = 'degrees_north'
    data_xr[varname_y].attrs['standard_name'] = 'latitude'
    data_xr[varname_y].attrs['long_name'] = 'latitude'
    
    #add wgs84 attributes (projected system was dropped upon loading)
    data_xr['wgs84'] = -2147483647
    data_xr['wgs84'].attrs = {'name': 'WGS84',
                              'epsg': 4326,
                              'grid_mapping_name': 'latitude_longitude',
                              'longitude_of_prime_meridian': 0.0,
                              'semi_major_axis': 6378137.0,
                              'semi_minor_axis': 6356752.314245,
                              'inverse_flattening': 298.257223563,
                               'EPSG_code': 'EPSG:4326',
                              'value': 'value is equal to EPSG code',
                              'proj4_params': ''}
                       
data_xr.to_netcdf(file_nc.replace('_net.nc','_WGS84_net.nc'))

