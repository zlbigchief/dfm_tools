# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 16:54:48 2022

@author: veenstra
"""

import datetime as dt
from pathlib import Path
import numpy as np

try: #0.3.1 release
    from hydrolib.core.io.bc.models import ForcingModel, QuantityUnitPair, TimeInterpolation, TimeSeries
except: #main branch and next release
    from hydrolib.core.io.dflowfm.bc.models import ForcingModel, QuantityUnitPair, TimeInterpolation, TimeSeries

dir_output = './bc_writeperfomance'

# Chosen approach: separate .bc file for each boundary (east and south)
bc_east = ForcingModel()

print('writing timing for bc files with 50 columns')
for nrows in [1000,10000,100000]:
    dtstart = dt.datetime.now()
    print(f'{nrows} rows datablock generation:             ',end='')
    datablock = np.random.uniform(low=-40, high=130.3, size=(nrows,50))
    datablock_list = datablock.tolist()
    
    # Each .bc file can contain 1 or more timeseries, one for each support point:
    steric = TimeSeries(
        name="east2_0001",
        quantityunitpair=[QuantityUnitPair(quantity="time", unit="seconds since 2022-01-01 00:00:00 +00:00"),
                          QuantityUnitPair(quantity="waterlevel", unit="m")],
        timeinterpolation=TimeInterpolation.linear,
        datablock=datablock_list, 
    )
    bc_east.forcing.append(steric)
    time_hydrolib = (dt.datetime.now()-dtstart).total_seconds()
    print(f'{time_hydrolib:.2f} sec')

    print(f'{nrows} rows with hydrolib (unformatted):      ',end='')
    dtstart = dt.datetime.now()
    bc_east.save(filepath=Path(dir_output,"steric_east2_hydrolib.bc"))
    time_hydrolib = (dt.datetime.now()-dtstart).total_seconds()
    print(f'{time_hydrolib:.2f} sec')
    
    try:
        print(f'{nrows} rows with hydrolib (formatted single): ',end='')
        dtstart = dt.datetime.now()
        bc_east.serializer_config.float_format_datablock = '.2f'
        bc_east.save(filepath=Path(dir_output,"steric_east2_hydrolibformattedsingle.bc"))
        time_hydrolib = (dt.datetime.now()-dtstart).total_seconds()
        print(f'{time_hydrolib:.2f} sec')
    except AttributeError:
        print('FAILED (TOO OLD HYDROLIB VERSION)')
    
    metadata_block = """[forcing]
quantity          = time
unit              = seconds since 2022-01-01 00:00:00 +00:00
quantity          = waterlevel
unit              = m\n"""
    
    #normal and most efficient would be np.savetxt(file_out,datablock), but we want to append and also write metadata, so first open file

    print(f'{nrows} rows with savetxt (unformatted):       ',end='')
    dtstart = dt.datetime.now()
    file_out = Path(dir_output,"steric_east2_np.bc")
    with open(file_out,'w') as f_bc:
        f_bc.write(metadata_block)
    with open(file_out,'a') as f_bc:
        np.savetxt(f_bc,datablock)
    time_npsavetxt = (dt.datetime.now()-dtstart).total_seconds()
    print(f'{time_npsavetxt:.2f} sec')

    print(f'{nrows} rows with savetxt (formatted single):  ',end='')
    dtstart = dt.datetime.now()
    file_out = Path(dir_output,"steric_east2_npformattedsingle.bc")
    with open(file_out,'w') as f_bc:
        f_bc.write(metadata_block)
    with open(file_out,'a') as f_bc:
        np.savetxt(f_bc,datablock,fmt='%9.3f')
    time_npsavetxt = (dt.datetime.now()-dtstart).total_seconds()
    print(f'{time_npsavetxt:.2f} sec')
    
    print(f'{nrows} rows with savetxt (formatted percol):  ',end='')
    dtstart = dt.datetime.now()
    file_out = Path(dir_output,"steric_east2_npformattedpercol.bc")
    with open(file_out,'w') as f_bc:
        f_bc.write(metadata_block)
    with open(file_out,'a') as f_bc:
        np.savetxt(f_bc,datablock,fmt='%9.1f'+'%9.3f'*49)
    time_npsavetxt = (dt.datetime.now()-dtstart).total_seconds()
    print(f'{time_npsavetxt:.2f} sec')
    print('')
    
    