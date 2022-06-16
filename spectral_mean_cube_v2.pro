@resistant_mean_nan
pro spectral_mean_cube,pathToCube,sigma_cut,output
;cube has dimensions [256,32,512]
;each pixel [a,b,*] has a spectrum that needs to be smoothed along that direction
pathy = pathToCube + '/cube_spatial_v1.fit'
data = readfits(pathy,header1)
;going over each pixel
xsize = n_elements(data(*,0,0))
ysize = n_elements(data(0,*,0))
xline = [] ;holding (y)lines of spectra

for x=0,xsize-1 do begin
yline = [] ;will hold spectra along 1 spatial dimension
for y=0,ysize-1 do begin

;spectral dimension averaging for a spectrum
pixel_spec=fltarr(512)
for i=0,511 do begin
	; we will check for endpoints, to truncate the 5-box average
	if i eq 0 then resistant_mean_nan,data[x,y,0:2],sigma_cut,boxaverage,boxsigma else $
	if i eq 1 then resistant_mean_nan,data[x,y,0:3],sigma_cut,boxaverage,boxsigma else $
	if i eq 510 then resistant_mean_nan,data[x,y,508:511],sigma_cut,boxaverage,boxsigma else $
	if i eq 511 then resistant_mean_nan,data[x,y,509:511],sigma_cut,boxaverage,boxsigma else resistant_mean_nan,data[x,y,i-2:i+2],sigma_cut,boxaverage,boxsigma
	pixel_spec[i] = boxaverage
endfor
pixel_specz = reform(pixel_spec, 1, 1, 512, /overwrite)
yline = [ [yline],[pixel_specz] ]
endfor
xline = [ xline,yline ]
endfor
writefits,pathToCube+'/cube_smooth_v2.fit',xline,header1
output = xline
return
end

