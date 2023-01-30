@combine_rad_fits_folder

pro makecubes

filez = file_search("/chiron4/antojr/calibrated_ir/*")
n_scans = n_elements(filez)
;loop
;6 Sept 2022, first run was halted at 314.4200013_, running again from there [638]
for i=638,n_scans-1 do begin
fname = filez[i]
a = strsplit(fname,'/',/extract)
b = strsplit(a[3],'.',/extract)
doy = b[0]
if doy lt 308 then combine_rad_fits_folder,FILE_DIR = fname $
else combine_rad_fits_folder,FILE_DIR=fname,/NS_FLIP
;print,i
endfor
end

