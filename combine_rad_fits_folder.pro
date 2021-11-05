PRO combine_rad_fits_folder, FILE_DIR = file_dir, NS_FLIP = ns_flip

;;-----------------------------------------------------------------------------
;; PURPOSE:
;; Given an input directory, the program finds all FITs files in the directory, reads
;; the data, and writes out two new FITs files with data in spatial cubes, i.e.
;; (number of samples/rows/spatial, number of images/frames, number of bands/columns/lambda).
;;
;; The files will be written in the same directory the FITs files are located.
;; The first file will contain the calibrated radiance values.
;; The second file will contain the wavelength value at each pixel position (in microns).
;;
;; The user may set a flag to use the wavelength map for each file otherwise the
;; program will default to use a the wavelength map from the first file for all files.
;;
;; If the user does not provide an input directory, the program will first ask the user
;; to select a file in order to build the data cubes.
;;
;; CALLING SEQUENCE:
;;  combine_rad_fits_folder, FILE_DIR = file_dir
;;
;; REQUIRED INPUTS:
;;
;; OUTPUTS:
;;
;; OPTIONAL INPUT KEYWORDS:
;;   FILE_DIR - The directory that is to be searched for FITs files.
;;   NS_FLIP - If set, the program will rotate the data 180 degrees in order to
;;       account for the scan direction of the spectrometer.
;;
;; EXAMPLE:
;;   IDL> combine_fits_folder, FILE_DIR = '~atonjr/small_bodies/DOY_312_Calibrated/', /NS_FLIP
;;
;; PROCEDURES USED (i.e. called directly!):
;;   READFITS - Reads a FITS file
;
;; MODIFICATION HISTORY:
;;  2005-08-02  M. Baca    Initial file written
;;
;;-----------------------------------------------------------------------------

    IF (n_elements(NS_FLIP) EQ 0) THEN NS_FLIP=0
    IF (n_elements(USE_MAPS) EQ 0) THEN USE_MAPS=0

    files_w_ext = file_search(FILE_DIR, '*.fit', COUNT = num_files)
       tmp1 = READFITS(files_w_ext[0], t_hdr, /SILENT)
       wave1 = READFITS(files_w_ext[0], EXTEN=1, /SILENT)
       size_data = SIZE(tmp1)
       data_type = SIZE(tmp1, /TYPE)
       wave_type = SIZE(wave1, /TYPE)
       output_data = MAKE_ARRAY(size_data(1), size_data(2), num_files, TYPE = data_type)
       output_waves = MAKE_ARRAY(size_data(1), size_data(2), num_files, TYPE = wave_type)
       output_data[*,*,0] = tmp1
       output_waves[*,*,0] = wave1
       FOR i = 1, num_files-1 DO BEGIN
         tmp = READFITS(files_w_ext[i], t_hdr, /SILENT)
         wave = READFITS(files_w_ext[i], EXTEN=2, /SILENT)
;                        badpixel = READFITS(files_w_ext[i], EXTEN=1, /SILENT)
;                        tmp(where(badpixel gt 0))=!VALUES.F_NAN
         output_data[*,*,i] = tmp
         output_waves[*,*,i] = wave1
       ENDFOR
;;This makes the three dimensions of the cube as follows, along slit, along scan, spectral 
       output_data = TRANSPOSE(output_data, [1,2,0])
       output_waves = TRANSPOSE(output_waves, [1,2,0])

;; If the data is collected using a south to north scan, the data in
;; the above cube is reversed so that the data are in the same format as a north to south scan
       IF NS_FLIP THEN BEGIN
         output_data = REVERSE(output_data, 2)
         output_waves = REVERSE(output_waves, 2)
       ENDIF
;hey I'm goku
    data_filename = FILE_DIR + '/cube_spatial.fit'
    waves_filename = FILE_DIR + '/cube_wave.fit'

;; If we have a north-to-south scan, two reverses must take place. One reverse takes into
;; account that IDL plots from the bottom up in a window so the data is flipped to look correct
;; in a window. The other reverse takes into account that the data must be reversed left-right since the spatial
;; dimension on the array appears backwards when read out and we work with the sun to the right.
    writefits, data_filename, REVERSE(REVERSE(output_data, 1), 2)
    writefits, waves_filename, REVERSE(REVERSE(output_waves, 1), 2)

END
