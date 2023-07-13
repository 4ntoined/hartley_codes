@spatial_mean_cube

pro spacesmooth_crank

fils = file_search('/alcyone1/antojr/cali/*')
;fils = file_search('/chiron4/antojr/calibrated_ir/*')
;filA = file_search('/chiron4/antojr/calibrated_ir/309*')
;filB = file_search('/chiron4/antojr/calibrated_ir/310*')
;filC = file_search('/chiron4/antojr/calibrated_ir/311*')
;filD = file_search('/chiron4/antojr/calibrated_ir/312*')
;filE = file_search('/chiron4/antojr/calibrated_ir/313*')
;filF = file_search('/chiron4/antojr/calibrated_ir/314*')
;fils = [filA,filB,filC, filD, filE]

n_scans = n_elements(fils)
sig_cut=2.5
prog_count = 1
for i=0,n_scans-1 do begin
paths = fils[i]
smooth_space,paths,sig_cut,outsome

;if i/n_scans ge prog_count * 0.05 then begin
;print,i/n_scans,format='(D6.3)'
;prog_count+=1
;endif

endfor
end

