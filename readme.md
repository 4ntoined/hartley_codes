some codes for my comet

__dark_extraction.py__
combs through directories looking for last frames of each scan, extracting data and metadata
extraction.py might be more recent, unsure, will have to deal with

__extraction.py__
don't wanna repeat see dark_extraction

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

notes:
more to come
