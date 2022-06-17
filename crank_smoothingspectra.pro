@spectral_mean_cube_v2
pro smoothem,sig_cut,box_size
;cube has dimensions [256,32,512]
;each pixel [a,b,*] has a spectrum that needs to be smoothed along that direction
fils = file_search('/chiron4/antojr/calibrated_ir/*')
n_scans = n_elements(fils)
;sig_cut=2.0
for i=0,n_scans-1 do begin

pathy = fils[i]
spectral_mean_cube,pathy,sig_cut,box_size,outtie
print,i

endfor
end

