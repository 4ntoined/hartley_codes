@combine_rad_fits_folder

pro makecubes

filez = file_search("/chiron4/antojr/calibrated_ir/*")
n_scans = n_elements(filez)

for i=0,n_scans-1 do begin
fname = filez[i]
a = strsplit(fname,'/',/extract)
b = strsplit(a[3],'.',/extract)
doy = b[0]
if doy lt 309 then combine_rad_fits_folder,FILE_DIR = fname,NS_FLIP=0 $
else combine_rad_fits_folder,FILE_DIR=fname,NS_FLIP=1
;if doy gt 308 then print,doy
print,i

endfor
end
