@resistant_mean_nan
pro darkmean, data, sigma_cut, output, fitsname
;cube has dimensions [512,256,# of frames] i think
;

num_frames = n_elements(data(0,0,*))
means = fltarr(num_frames)
for i=0,num_frames-1 do begin
	frame = data(*,*,i)
	resistant_mean_nan,frame,sigma_cut,framemean,frame_sig,frame_rej
	means[i] = framemean
endfor
writefits,fitsname,means
output = means
return
end

