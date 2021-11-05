;'m
;Goku-------------------------------------------------------------------------------------------------------------------
;Deep Impact Hartley 2 data processing pipeline algorith where scaled in-scene darks are used
;-----------------------------------------------------------------------------------------------------------------------
;Input files needed
;Hartley 2 raw frame with header (frame)
;Hartley 2 in-scene dark frame that Antoine creates from an average of all in-sceen darks that have already been
;linearlized before averaging (dark)
;Hartley 2 linearity coefficients from pipeline (lin_params)
;Hartley 2 master flat from pipeline (master_flat)
;Hartley 2 asf profile from pipeline (asf_profile)
;Hartley 2 absolute calibration from pipeline (calwave,calflux)
;Hartley 2 bad pixels for BINFF from pipeline (bad_pix)
;-----------------------------------------------------------------------------------------------------------------------

;-----------------------------------------------------------------------------------------------------------------------
;IDL Procedures that you will need
;basic_pipeline.pro                     ;this file with the basic pipeline steps
;make_ir_flat_v2.pro                    ;Tony Farnham's pixel by pixel treatment of the lunar master flatfields

;getIRSpectralMapSA.pro                 ;Silvia Protopapa's code for spectral mapping with smile correction
;irrega.pro                             ;called by getIRSpectraMapSA
;-----------------------------------------------------------------------------------------------------------------------

;-----------------------------------------------------------------------------------------------------------------------
;How to run IDL:
;At a terminal prompt on an Astronomy Dept. computer/server type
;
;LINUX Prompt> idl
;
;-----------------------------------------------------------------------------------------------------------------------

;-----------------------------------------------------------------------------------------------------------------------
;How to read/write fits files in IDL:
;
;IDL Prompt> output_variable_name = readfits('input_filename_with_path.fit',header)
;
;IDL Prompt> writefits,'output_filename_with_path.fit',data_array_to_be_saved
;
;-----------------------------------------------------------------------------------------------------------------------

;-----------------------------------------------------------------------------------------------------------------------
;How to linearize a raw data frame:
;First, define the linearity parameters for the HRI-IR detector by reading in the appropriate calibraton file
;
;IDL prompt> lin_params=readfits('BINFF_linearity_coefficients_032112.fit')
;
;Then apply those parameters to the raw data file
;
;IDL prompt> linearized_frame_output = dixi_linearize_4thorder(raw_frame, line_params)
;
;-----------------------------------------------------------------------------------------------------------------------

;-----------------------------------------------------------------------------------------------------------------------
;How to run the whole pipeline on a raw frame:
;First, compile the IDL codes needed
;
;IDL prompt> .run make_ir_flat_v2
;IDL prompt> .run getIRSpectralMapSA
;IDL prompt> .run irrega
;IDL prompt> .run basic_pipeline
;
;Then, read in a raw data fits file and its header with double precision
;
;IDL prompt> raw_frame = double(readfits('name_of_raw_file.fits',raw_frame_hdr))
;
;Then, read in the dark frame that you created with double precision
;
;IDL prompt> dark = double(readfits('name_of_dark_file.fits'))

;Then, run the pipeline with a supplied scale factor (use 1.0 if scaling isn't necessary):
;
;IDL prompt> Hartley2_pipeline,raw_frame,raw_frame_hdr,dark,dark_scale_factor
;
;-----------------------------------------------------------------------------------------------------------------------

;-----------------------------------------------------------------------------------------------------------------------
;Linearization function
function dixi_linearize_4thorder,data,lin_params

lin = lin_params(*,*,0) + lin_params(*,*,1)*data(*,*) + lin_params(*,*,2)*data(*,*)^2d0 + lin_params(*,*,3)*data(*,*)^3d0 + lin_params(*,*,4)*data(*,*)^4d0

return,data/lin

end

;-----------------------------------------------------------------------------------------------------------------------
;Pipeline algorithm
;Antoine here, I am changing this so it outputs the final data for use in a larger program
pro Hartley2_pipeline,frame,hdr,dark,dark_scale_factor,output_file,output_wave

lin_params=readfits('BINFF_linearity_coefficients_032112.fit',/SILENT)
master_flat=readfits('HRIIR_master_flat_ubff_pix_dec13.fits',/SILENT)
asf_profile=readfits('asf_transmission_final_dec13.fits',/SILENT)
readcol,'ConversionMap2013.txt',calwave,calflux,/SILENT
bad_pix=readfits('BINFF_badpix.fit',/SILENT)
bad_pix=bad_pix*1.0

file_lin=dixi_linearize_4thorder(frame,lin_params)
file_dksub=file_lin-(dark*dark_scale_factor)
flat=make_ir_flat_v2(master_flat,asf_profile,sxpar(hdr,'OPTBENT'),sxpar(hdr,'IMGMODE'),flat_ver=1)
file_flat=file_dksub/flat
spectral_maps=getirspectralmapSA(hdr)
wave=spectral_maps(*,*,0)
dlam=spectral_maps(*,*,1)
file_abscal=file_lin*0.

for j=0,255 do begin
  file_abscal(*,j)=file_flat(*,j)*interpol(calflux*2.0,calwave,wave(*,j))*2./(sxpar(hdr,'INTTIME')/1000.)/dlam(*,j)/2.
 endfor

file_badpix=file_abscal
file_badpix(where(bad_pix eq 1))=!VALUES.F_NAN

calibrated_file=file_badpix
output_file = calibrated_file
output_wave = wave
;writefits,'Calibrated_filename.fit',calibrated_file,hdr
;writefits,'Calibrated_filename.fit',wave,/append
return
end

