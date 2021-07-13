@resistant_mean_nan
@basic_pipeline
;dk what im doing but im doing it
;oh it's Antoine

pro master_dark,data,sigma_cut,outdata
;this code will need to
;(1) take in a whole lot of frames
;(2) linearize each one, [gonna need the linearity coefficients]
;(3) mean each one,
;(4) divide by the mean to normalize
;(5) add frame to running sum of frames
;(6) divide by the number of frames
;(7) viola, on to the next
;data will come in the shape of 512, 256, # of frames (i think)

;getting parameters for linearization
lins = readfits("BINFF_linearity_coefficients_032112.fit")
;
n_frames = n_elements(data(0,0,*))
wavelength_size = n_elements(data(*,0,0)) ;should be 512
space_size = n_elements(data(0,*,0)) ;should be 256

darks = fltarr(wavelength_size,space_size,n_frames)
for i=0,n_frames-1 do begin
	nonlin_frame = data(*,*,i)
	frame = dixi_linearize_4thorder(nonlin_frame,lins)
	resistant_mean_nan,frame,sigma_cut,framemean,frame_sig,frame_rej
	normal_frame = frame/framemean
	darks[*,*,i] = normal_frame
endfor
;anyway protodark should have all the frames now normalized
;so we will take a resistant mean of each pixel along the frame dimension
;boy
protodark = fltarr(wavelength_size,space_size)
for i=0,wavelength_size-1 do begin
	for j=0,space_size-1 do begin
		resistant_mean_nan,darks[i,j,*],sigma_cut,pix_mean,pix_sig,pix_rej
		protodark[i,j] = pix_mean
	endfor
endfor
;think that might be it, woah
outdata = protodark
writefits,"masterdark_v1.fit",protodark
return
end
