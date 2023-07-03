@resistant_mean_nan
@basic_pipeline
;dk what im doing but im doing it
;oh it's Antoine

pro master_dark,data,sigma_cut,savepath,metapath,outdata
;this code will need to
;(1) take in a whole lot of frames
;(2) linearize each one, [gonna need the linearity coefficients]
;(3) mean each one,
;(4) divide by the mean to normalize
;(5) add frame to running sum of frames
;(6) divide by the number of frames
;(7) viola, on to the next
;data will come in the shape of 512, 256, # of frames (i think)
;'/alcyone1/antojr/downloading_h2/raw/filtered_list.txt'
savehere = savepath ; '/alcyone1/antojr/downloading_h2/darkmatters/'
readcol,metapath,cindex,cexpid,cjd,exptime,cframes,cbinff,cpxl,cdist,ctemp,cpath,format='I,A,F,F,I,A,F,F,F,A',skipline=1
;getting parameters for linearization
lins = readfits("BINFF_linearity_coefficients_032112.fit")
;
n_frames = n_elements(data(0,0,*))
wavelength_size = n_elements(data(*,0,0)) ;should be 512
space_size = n_elements(data(0,*,0)) ;should bemeans
darks = fltarr(wavelength_size,space_size,n_frames)
linears = fltarr(wavelength_size,space_size,n_frames)
weighted = fltarr(wavelength_size,space_size,n_frames)
means = fltarr(n_frames)
sigs1 = fltarr(n_frames)
nrej1 = fltarr(n_frames)
;nonlins = fltarr(wavelength_size,space_size,n_frames)

for i=0,n_frames-1 do begin
	nonlin_frame = data(*,*,i)
	frame = dixi_linearize_4thorder(nonlin_frame,lins)
	linears[*,*,i] = frame
	frame_weight = frame / exptime[i]
	weighted[*,*,i] = frame_weight
	resistant_mean_nan,frame_weight,sigma_cut,framemean,frame_sig,frame_rej
	means[i] = framemean
	sigs1[i] = frame_sig
	nrej1[i] = frame_rej
	normal_frame = frame/framemean
	darks[*,*,i] = normal_frame
endfor

writefits, savehere + 'dark_linears.fit', linears
writefits, savehere + 'dark_normals.fit', darks
writefits, savehere + 'dark_weights.fit', weighted
writefits, savehere + 'dark_means_mean.fit', means
writefits, savehere + 'dark_means_sigs.fit', sigs1
writefits, savehere + 'dark_means_nrej.fit', nrej1

;anyway protodark should have all the frames now normalized
;so we will take a resistant mean of each pixel along the frame dimension
;boy
protodark = fltarr(wavelength_size,space_size)
protosigs = fltarr(wavelength_size,space_size)
protonrej = fltarr(wavelength_size,space_size)
for i=0,wavelength_size-1 do begin
	for j=0,space_size-1 do begin
		resistant_mean_nan,darks[i,j,*],sigma_cut,pix_mean,pix_sig,pix_rej
		protodark[i,j] = pix_mean
		protosigs[i,j] = pix_sig
		protonrej[i,j] = pix_rej
	endfor
endfor
;think that might be it, woah
outdata = protodark
writefits,savehere+"masterdark_vA.fit",protodark
writefits,savehere+"masterdark_Asigs.fit",protosigs
writefits,savehere+"masterdark_Anrej.fit",protonrej
return
end
