some codes for my comet
### pipeline codes
__thecrank.pro__
step 1 /IDL/
calibrates the raw ir frames and saves calibrated frames scan by scan
requires (absolute) path to a master dark to be scaled and used on all frames _dark_path_
and a dark_temp* file for the scale factor used for the dark for each frame _dark_scale_
uses __bulk_calibrate__

__bulk_calibrate.pro__
/IDL/
calibrates all the frames within a directory _filedir_ into another directory _directoryToSave_
uses __bulk_pipeline__

__bulk_pipeline.pro__
/IDL/
a version of basic_pipeline.pro that I have edited a little bit so I could run it in bulk_calibrate and have things work out
needs the other pipeline codes: irrega.pro, getIRSpectralMapSA.pro (sp?), make_ir_flat_v2.pro etc, and also some fit files.
those files might not be in this directory but I have them

__crank_makecubes.pro__
step 2 /IDL/
assembles frames of a scan into a cube for all the scans in a directory
uses combine_rad_fits_folder.pro

__double_exposure.py__
do last /python/
doubles the cubes in the frame-stacking dimension for the particular scans where it is necessary
it also renames the cubes of the scans that are NOT affected by the double exposure gig, so that the "final" cubes being used all share the same naming structure
makes it so easy to code

__double_exposure_space.py__
/python/
does same as above but specifically targets spatially smoothed cubes

### analysis codes
__crank_smoothingspectra.pro__
step3 /IDL/
smoothes all the cubes along their spectral dimensions, every pixel is replaced by a 3-pixel average of that pixel and 2 neighbors on the spectrum (+/-1 wavelength bin)
uses __spectral_mean_cube_v2__

__crank_smoothingspace.pro__
step4+ /IDL/
smoothes all the cubes in the spatial plane(s), pixels are averaged with their 8 closest neighbors, so a 3x3 box
uses __spatial_mean_cube__

__spatial_mean_cube__
/IDL/
a retrofitted spectral_mean_cube(_ v2) that does what's stated above, makes exceptions for each corner and each edge of each frames
uses __resistant_mean_nan__

__crank_gasmaps.py__
step4+ /python/
makes fit files for each scan containing an image of the scene in co2 and the scene in h2o
short term goal is to also incorporate dust, would be cool to use dust co3 and h2o to do an rgb false image
ugh i want her so bad

__fixing_crank_gasmaps.py__
/python/
small improvement to original

__crank_volatileLightCurves.py__
AFTER double exposure /python/
calculates the sum of h2o or co2 in the gas maps for every scan and records that data with the corresponding julian date in a .txt file
easily plotted later, yanno maybe update with dust.
also can account weight for when certain nansums have nans, the nans count as zeros, and those data are plotted alongside data with no nanzeros with no distinction between them.
so weighting by how many pixels are not nan in a given nansum would be a nice little tweak I think, I'll try to catch that on the second crank
uses __playingwithdata__

### uhhh, the codes we made along the way
__big_gas_curves.py__
/python/
plotting the gas light curves, will update with dust one day :)

__continuum_removal.py__
/python/
takes one (1) cube, calculates the h2o and co2 in every pixel of the scan, and records that data in a fit file
not a requisire for the crank, but donated much of its structure to it

__dark_extraction.py__
combs through directories looking for last frames of each scan, extracting data and metadata
extraction.py might be more recent, unsure, will have to deal with

__dark_temperature.py__
/python/
apprently in this repository, don't feel like explaining it right now its a long, loaded story.
i will come back to this

__extraction.py__
don't wanna repeat see dark_extraction

to-do:
* needs to include CTRDIST and PXLSCALE in the extraction

__ircontin.py__
integrates a smooted spectrum in the continuum short wavelength
takes an aperture, location and size

to-do:
* run in batch for light curve from many spectra
* use nucleus location or ask for user input

__light_curve_mri.py__
takes mri photometry and plots a light curve

__master_dark.pro__
takes in the dark frames from some number of scans, and averages them to make the master dark

__meaning_darks.pro__
does a resistant mean (ignoring nans) for each of some number of frames

__playingwithdata.py__
puts scan data and metadata into a single numpy structured array for use elsewhere

__resistant_mean_nan.py__
my attempt of copying resistant_mean_nan.pro into python

__spectral_mean_cube_v2.pro__
takes a cube (2d array of spectra) and returns the cube smoothed along the spectral dimension
i.e. the spectrum in each pixel is smoothed in the spectral direction

__temperature_dixi.py__
gonna be honest, not exactly sure, i was doing a lot of experiments with working out the temperature for this project

__temperature_timeline.py__
puts together a complete(ish) timeline of temperature over the course of the hartey mission
pulls majorly from hri telemetry and then pulls some more from calibrated fits file headers
includes a small fix to some weird results 

__upgraded_darktemp.py__
program for reorganizing dark vs temp data readout to be ordered by time

__upgraded_scandat.py__
similar to upgraded_darktemp.py, for scan metadata

__volatile_light_curve.py__
takes in volatile maps (scalar for integrated water/co2 curves for each pixel in a scan) and makes a light curve from them

to-do:
* aperture support

__wip.py__
plots spectra

__working_continuum__
bro this does a whole continumm removal and spits out a fits image?
idk its a fits table as usual but it might as well also be an image idk
-tweaked the code to A) run faster and B) show the h2o map
-gonna tweak a few more things and see if we can see the co2 map also as well

my data file legend:
oozaru3.txt- golden one
all the scans I'm using, in chronological order, with pixel scale and comet dist
oozaru2.txt-
above but not in order
oozaru.txt-
above but all last scans pulled, no cuts
seven/eight/twelve_v2.txt/dat-
includes pixel scale and comet dist
seven/eight/twelve.txt/dat-

broly.txt-
oozaru3 with no pixel scale and comet dist
ssbevegeta.txt-
broly with no cuts

dark_temp_v2.dat- some useful information, in chronological order,

notes:
more to come
