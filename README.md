dfm_tools
=========

dfm_tools are Python post-processing tools for Delft3D FM model outputfiles (netCDF) and more

- Free software: GNU General Public License v3


Features
--------
- supported formats:
	- D-Flow FM output data (net, map, his, fou, rst files)
	- almost any other netCDF (ERA5, hirlam, SFINCS map, SFINCS his, Sobek observation)
	- Delft3D netCDF output files (you can get netcdf output with keywords in your mdf)
	- converted Delft3D and waqua data (converted to netCDF with getdata.pl) (Delft3D conversion with getdata.pl is not flawless, preferably rerun with netCDF as outputformat instead)
- data handling:
	- select all data based on variable, timestep/datetime, layer, station (not yet on depth)
	- get feedback about available variables, timesteps/datetimes, layers, stations when you retrieve the wrong ones
	- retrieve lists of variables, timesteps/datetimes, stations, cross sections, general structures
	- selection/plotting by polyline/crossection (slicing the ugrid data)
	- merge partitions and delete ghostcells automatically
	- take over masks in original data
- plotting:
	- plot flexible mesh net/map variables as polycollections/patches
	- plot regular grid variables with pcolor (work in progress)
	- plot cartopy features (land, sea, landboundary, country borders, satellite background)
	- plotting z,t-plots (see wishlist section for inaccuracies)
	- plot anything you like and how you like it
- other io functions:
	- tekal (.tek, .pli, .pliz, .pol, .ldb) data
	- read Delft3D files (.grd, .dep)
	- read/write mdu file


Example usage
--------
```python
#import statements
import matplotlib.pyplot as plt
from dfm_tools.get_nc import get_netdata, get_ncmodeldata, plot_netmapdata
from dfm_tools.get_nc_helpers import get_ncvardimlist, get_timesfromnc, get_hisstationlist

#define files. you will probably get error messages with your own file, but these should be self-explanatory
file_nc_map = 'path_to_file'
file_nc_his = 'path_to_file'

#get lists with vars/dims, times, station/crs/structures
vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc_map)
times_pd = get_timesfromnc(file_nc=file_nc_map)
statlist_pd = get_hisstationlist(file_nc=file_nc_his, varname_stat='station_name')

#retrieve his data
data_fromhis_bl = get_ncmodeldata(file_nc=file_nc_his, varname='bedlevel', station='all')
data_fromhis_wl = get_ncmodeldata(file_nc=file_nc_his, varname='waterlevel', station='all', timestep= 'all')
fig, axs = plt.subplots(2,1,figsize=(6,8))
axs[0].plot(data_fromhis_bl.var_stations,data_fromhis_bl,'-')
axs[1].plot(data_fromhis_wl.var_times,data_fromhis_wl,'-')

#retrieve net/map data, plot map data on grid
ugrid = get_netdata(file_nc=file_nc_map)#, multipart=False)
data_frommap_bl = get_ncmodeldata(file_nc=file_nc_map, varname='mesh2d_flowelem_bl')
data_frommap_sal = get_ncmodeldata(file_nc=file_nc_map, varname='mesh2d_sa1', timestep=2, layer='all')
fig, axs = plt.subplots(2,1,figsize=(6,8))
pc = plot_netmapdata(ugrid.verts, values=data_frommap_bl, ax=axs[0], linewidth=0.5, cmap='jet')
pc = plot_netmapdata(ugrid.verts, values=data_frommap_sal[0,:,-1], ax=axs[1], linewidth=0.5, cmap='jet')
```
- for more examples, check https://github.com/openearth/dfm_tools/tests (this is also the pytest testbank)
- examples of (mostly unformatted) figures created by this pytest testbank: n:\\Deltabox\\Bulletin\\veenstra\\info dfm_tools
- please check the TODO sections for known inaccuracies or features that are not yet available
- please report other bugs and feature requests at the developers or at https://github.com/openearth/dfm_tools/issues (include OS, dfm_tools version, reproduction steps)


How to install dfm_tools
--------
- download and install the newest anaconda 64 bit (including PATH checkbox), for instance: https://repo.anaconda.com/archive/Anaconda3-2019.10-Windows-x86_64.exe
- install dfm_tools from github
	- open command window (or anaconda prompt)
	- ``conda create --name dfm_tools_env python=3.7 git`` (creating a venv is recommended, but at least do ``conda install git`` if you choose not to)
	- ``conda activate dfm_tools_env``
	- optional: ``conda install -c conda-forge shapely`` (for slicing 2D/3D data) (conda-forge channel is necessary since main channel does not have shapely>=1.7, lower is not sufficient)
	- optional: ``conda install -c conda-forge cartopy`` (for satellite imagery on plots)
	- ``python -m pip install git+https://github.com/openearth/dfm_tools.git`` (this command installs all required packages and it also updates dfm_tools to the latest version if you already installed it before)
	- test by printing dfm_tools version number: ``python -c "import dfm_tools; print(dfm_tools.__version__)"`` (also try this in Spyder, to check if you are working in the dfm_tools_env venv)
- launch Spyder:
	- for the first time in your venv: open anaconda navigator, select dfm_tools_env from the drop-down menu, install Spyder here (and launch Spyder from here)
	- open 'Spyder(dfm_tools_env)' via your windows start menu


TODO wishlist
--------
- retrieve station/crs/gs list corresponding to a variable with get_hisstationlist(), now already used in stations/gs/crs check of get_nc.get_ncmodeldata()
- select/check functions in dflowutil folder and merge with dfm_tools:
	- including dflowutil_examples/test_dflowutil.py and other test scripts
	- dflowutil contains e.g. read/write functions for general datafromats (tim, bc)
	- same for MBay scripts
- add retrieval via depth instead of layer number (then dflowutil.mesh can be removed?):
	- refer depth w.r.t. reference level, water level or bed level
	- see test_workinprogress.py
- retrieve correct depths:
	- add depth array (interfaces/centers) to his and map variables (z/sigma layer calculation is already in get_modeldata_onintersection function)
	- depths can be retrieved from mesh2d_layer_z/mesh2d_layer_sigma, but has no time dimension so untrue for sigma and maybe for z? (wrong in dflowfm?)
	- layerzfrombedlevel keyword in mdu changes how zlayering is set up. Catch this exception with a keyword if necessary
- improve z,t-plots from hisfile:
	- example in test_get_nc.test_gethismodeldata()
	- WARNING: part of the z interfaces/center data in dflowfm hisfile is currently wrong, check your figures carefully
	- layer argument now has to be provided when retrieving zcoordinate_c (centers) from hisfile, but not when retrieving zcoordinate_w (interfaces), align this.
	- check center/corner correctness, pcolormesh does not completely correspond with contours
- improve cartopy satellite/basemap background:
	- add test if cartopy is installed before importing it, since these are optional modules (also cartopy import in user script, so does not work)
	- add more settings for linewidth/facecolor/alpha/linecolor
	- load geotiffs with satellite imagery (or png's where limits are provided by user) (files provided by user or automatically downloaded from predifined or provided source)
	- load World Imagery data from arcgis mapserver (e.g. https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9)
	- https://stackoverflow.com/questions/12116050/how-to-plot-remote-image-from-http-url
	- https://scitools.org.uk/cartopy/docs/v0.15/_modules/cartopy/mpl/geoaxes.html (stock_img() en background_img())
	- https://github.com/SciTools/cartopy/blob/master/lib/cartopy/data/raster/natural_earth/images.json
	- https://github.com/SciTools/cartopy/blob/master/lib/cartopy/data/raster/natural_earth/50-natural-earth-1-downsampled.png
	- plotting ax.gridlines(draw_labels=True) with cartopy: https://github.com/pyugrid/pyugrid/blob/master/notebook_examples/connectivity_example.ipynb
- add more io-functions:
	- convert data to kml (google earth) or shp?
	- add tekal write functions
- add tidal analysis:
	- https://github.com/sam-cox/pytides
	- https://pypi.org/project/pytides/
	- https://pypi.org/project/tidepy/
	- https://github.com/pwcazenave/tappy
	- https://pypi.org/project/UTide/
	- https://github.com/moflaher/ttide_py
- dimn_time is now actually variable name which does not work if time dimname is not the same as time varname
- make merc keyword always optional by testing for minmax all vertsx between -181 and 361 and minmax all vertsy (lat) between -91 and 91 (+range for overlap for e.g. gtsm model)
- optimize get_ncmodeldata for layerdepths/bedlevel/waterlevel (second intersect function), only retrieve necessary information for crossection
- add inpolygon/inboundbox selection of data:
	- optimize_dist keyword now draws inpolygon around line
	- to optimize intersect function when retrieving bed level and water level (do that with len(firstlinepart) optional keyword)
	- to retrieve other mapdata data faster
- add polygon ginput function (click in plot) (already partly exists in intersect/slice testscript)
- existing dfm model setup functions (and other useful stuff):
	 - https://github.com/openearth/delft3dfmpy (arthur van dam)	
	 - https://svn.oss.deltares.nl/repos/openearthtools/trunk/python/applications/delft3dfm (fiat, sobek etc)
	 - https://svn.oss.deltares.nl/repos/openearthtools/trunk/python/applications/delft3dfm/dflowfmpyplot/pyd3dfm/streamline_ug.py (streamline plotting for structured grids, but many settings)
- make grid reading more flexible:
	- raise understandable error when no mesh2d_edge_x var in netcdf, instead of keyerror none (e.g. with get_netdata on hirlam files)
	- if no ugrid in netfile, try to read provided xy variables and make meshgrid or convert cen2cor or cor2cen if necessary (how to test this?)
	- improve plots for structured grid (CMEMS, ERA5, hirlam, grd etc)
	- https://github.com/NOAA-ORR-ERD/gridded (https://github.com/pyugrid/pyugrid is merged into gridded) (ghostcells en mapmergen worden afgehandeld? meer dan 4 nodes per cel? support for stations?)
	- tests.test_get_nc.test_gethirlam() is eerste opzet voor hirlam/ERA5 data, werkt heel anders dan D-flow FM
	- how to plot properties on edges/nodes (scatter is slow), maybe create dual mesh and plot like faces. most relevant variables are also available on faces, so is this necessary?
	- add support for rstfiles (different way of storing grid data, only face nodes present?)
	- https://svn.oss.deltares.nl/repos/openearthtools/trunk/python/OpenEarthTools/openearthtools/io/dflowfm/patch2tri.py (equivalent van MIA)
	- https://svn.oss.deltares.nl/repos/openearthtools/trunk/python/OpenEarthTools/openearthtools/io/netcdf
	- plotting edges/nodes/faces and legend: https://github.com/pyugrid/pyugrid/blob/master/notebook_examples/connectivity_example.ipynb


TODO non-content
--------
- if you ``conda install -c conda-forge cartopy`` after dfm_tools installation, numpy cannot be found by cartopy. First ``conda install numpy`` and maybe rest of requirements.txt?
- add variable units to plots in test bench (``plt.title('%s (%s)'%(data_fromnc.var_varname, data_fromnc.var_object.units))``)
- readme korter maken (developer info naar aparte file)
- update/delete cookiecutter text files
- add documentation in comments of functions
- create overview of scripts and functions, including missing features
- put testdata on deltares shared location?
- put testdata and testoutput on github and create jupyter notebook instead of pptx?
- arrange auto-testing online (jarvis?): https://docs.pytest.org/en/latest/getting-started.html
- register on PyPI, for easier install via pip (easier for regular users):
	- https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html#register-your-package-with-the-python-package-index-pypi
	- https://packaging.python.org/tutorials/packaging-projects/
	- how to automate this process?
	- also add changelog besides commit comments?
- update license with Deltares terms
- write documentation as comments and generate automatically?
- create overview tree of all functions, also add missing functions here
- paths to project folders in test scripts are ok?
- style guide: https://www.python.org/dev/peps/pep-0008/
- contributing method: environment.yml (README.md) or requirements_dev.txt (CONTRIBUTING.rst)?


Developer information: how to contribute to this git repository
--------
- First request github rights to contribute with the current developers
	- Jelmer Veenstra <jelmer.veenstra@deltares.nl>
	- Lora Buckman
	- Julien Groenenboom
- Get a local checkout of the github repository:
	- Download git from https://git-scm.com/download/win, install with default settings
	- open command line in a folder where you want to clone the dfm_tools github repo, e.g. C:\\DATA
	- ``git clone https://github.com/openearth/dfm_tools.git`` (repos gets cloned to local drive, checkout of master branch)
	- to update: navigate to dfm_tools folder in git bash window and ``git pull`` (combination of git fetch and git merge)
- Create a separate python environment (contains pytest and bumpversion, necessary for developing):
	- open command line and navigate to dfm_tools github folder, e.g. C:\\DATA\\dfm_tools
	- ``conda env create -f environment.yml`` (sometimes you need to press enter if it hangs extremely long)
	- ``conda info --envs`` (shows dfm_tools_env virtual environment)
	- to remove: ``conda remove -n dfm_tools_env --all`` (to remove it again when necessary)
- Install your local github clone via pip (developer mode):
	- open command window, navigate to dfm_tools folder, e.g. C:\\DATA\\dfm_tools
	- ``conda activate dfm_tools_env``
	- ``python -m pip install -e .`` (pip developer mode, any updates to the local folder by github (with ``git pull``) are immediately available in your python. It also installs all required packages)
	- test if dfm_tools is properly installed by printing the version number: ``python -c "import dfm_tools; print(dfm_tools.__version__)"``
	- do not forget to install shapely and cartopy in your venv (see normal installation manual)
- REMOVE THIS PART DUE TO CARTOPY ISSUES WITH THIS METHOD IF SPYDER IS NOT UP TO DATE, AND ALL THE KNOWN BUGS? Optional: link to your venv from Spyder (then no separate Spyder installation necessary in venv)
	- alternative: you can also start spyder via Anaconda Navigator, after selecting your venv
	- open command line and navigate to dfm_tools github folder, e.g. C:\\DATA\\dfm_tools
	- ``conda activate dfm_tools_env``
	- ``python -c "import sys; print(sys.executable)"`` (the resulting path you need some steps later, e.g. C:\\Users\\%USERNAME%\\AppData\\Local\\Continuum\\anaconda3\\envs\\dfm_tools_env\\python.exe)
	- ``conda deactivate``
	- open spyder from start menu or anaconda or anything
	- Go to Tools >> Preferences >> Python interpreter >> point to dfm_tools_env python.exe (print of sys.executable)
	- restart IPython console
	- Known bugs with this method (instead of launching Spyder via anaconda navigator):
		- you get the message that 'spyder-kernels' is not installed or the wrong version:
			- open command window
			- ``conda activate dfm_tools_env``
			- ``python -m pip install spyder-kernels>=1.*`` (for Spyder 4.*) OR ``python -m pip install spyder-kernels==0.*`` (for Spyder 3.*)
			- restart Spyder console and it should work
		- figures are struggling:
			- your matplotlib backend is probably 'Tkagg' instead of 'Qt5Agg' (execute ``import matplotlib; matplotlib.get_backend()`` from the Spyder console)
			- open command window
			- ``conda activate dfm_tools_env``
			- ``python -m pip install pyqt5>=5.7.1``
			- restart Spyder console and it should work better
			- Note: pyqt5 was previously part of the requirements, but it caused errors for some users upon installation
		- you could get an error when slicing data (cross sections of 2D/3D data) (OSError: [WinError 126] The specified module could not be found):
			- this happens when you install shapely via pip in a conda environment
			- reproduce: ``python -c "import shapely.geometry"`` should give the same error, while ``python -c "import shapely"`` works without error
			- open command window
			- ``conda activate dfm_tools_env``
			- ``conda install shapely`` (this fixes the geos dependency, which causes the error)
- Branching:
	- open git bash window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- ``git config --global user.email [emailaddress]``
	- ``git config --global user.name [username]``
	- Create your own branch option 1:
		- manually create a branch on https://github.com/openearth/dfm_tools
		- open git bash window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
		- ``git remote update origin --prune`` (update local branch list)
		- ``git checkout branchname`` (checkout branch)
	- Create your own branch option 2:
		- open git bash window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
		- ``git checkout --branch branchname`` (create new branch and checkout, combination of git branch and git checkout commands)
	- get clean checkout again (overwrite local changes):
		- ``git fetch --all`` (fetches changes)
		- ``git reset --hard`` (resets local checkout of repos branch to server version)
		- ``git pull`` (fetches and merges changes, local checkout of repos branch is now updated again)
- Commit and push your changes to your online branch:
	- open git bash window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- optional: ``git pull origin master`` (gets edits from master to current local branch, might induce conflicts. maybe better to just push to your branch and then handle pull request on github website)
	- ``git add .``
	- ``git commit -m "message to be included with your commit"``
	- ``git push`` (pushes changes to server, do not do this in while working in the master)
- run test bank:
	- open command line in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- ``conda activate dfm_tools_env``
	- ``pytest -v --tb=short`` (runs all tests)
	- ``pytest -v --tb=short -m unittest``
	- ``pytest -v --tb=short -m systemtest``
	- ``pytest -v --tb=short -m acceptance``
	- ``pytest -v --tb=short tests\test_get_nc.py::test_getplotmapWAQOS``
- increasing the version number (with bumpversion):
	- open cmd window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- optional: ``conda activate dfm_tools_env``
	- ``bumpversion major`` or ``bumpversion minor`` or ``bumpversion patch`` (changes version numbers in files and commits changes)
	- push your changes with ``git push`` (from git bash window or cmd also ok?)
- Request merging of your branch on https://github.com/openearth/dfm_tools/branches
