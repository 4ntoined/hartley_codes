@spatial_mean_cube

pro spacesmooth_crank

fils = file_search('/chiron4/antojr/calibrated_ir/*')
n_scans = n_elements(fils)
sig_cut=2.0
for i=0,n_scans-1 do begin
paths = fils[i]
smooth_space,paths,sig_cut,outsome
print,i
endfor
end

