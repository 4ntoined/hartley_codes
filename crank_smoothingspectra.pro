@spectral_mean_cube_v2
pro smoothem,sig_cut,box_size
;cube has dimensions [256,32,512]
;each pixel [a,b,*] has a spectrum that needs to be smoothed along that direction

;this run Im smoothing all but a few DOYs
fils = file_search('/chiron4/antojr/calibrated_ir/*')
;filsA = file_search('/chiron4/antojr/calibrated_ir/298*')
;fils = file_search('/chiron4/antojr/calibrated_ir/319.4100023')
;filsb = file_search('/chiron4/antojr/calibrated_ir/299*')
;filsc = file_search('/chiron4/antojr/calibrated_ir/300*')
;filsd = file_search('/chiron4/antojr/calibrated_ir/301*')
;filse = file_search('/chiron4/antojr/calibrated_ir/302*')
;filsf = file_search('/chiron4/antojr/calibrated_ir/303*')
;fils1 = file_search('/chiron4/antojr/calibrated_ir/304*')
;fils2 = file_search('/chiron4/antojr/calibrated_ir/312*')
;fils3 = file_search('/chiron4/antojr/calibrated_ir/313*')
;fils4 = file_search('/chiron4/antojr/calibrated_ir/314*')
;fils5 = file_search('/chiron4/antojr/calibrated_ir/315*')
;fils6 = file_search('/chiron4/antojr/calibrated_ir/316*')
;fils7 = file_search('/chiron4/antojr/calibrated_ir/317*')
;fils8 = file_search('/chiron4/antojr/calibrated_ir/318*')
;fils9 = file_search('/chiron4/antojr/calibrated_ir/319*')
;fils0 = file_search('/chiron4/antojr/calibrated_ir/320*')
;filsp = file_search('/chiron4/antojr/calibrated_ir/321*')
;fils = [filsA,filsb,filsc,filsd,filse,filsf,filsp, fils1,$
;	fils2,fils3,fils4,fils5,fils6,fils7,fils8,fils9,fils0]
n_scans = n_elements(fils)
;loop
for i=0,n_scans-1 do begin
;each iteration will take a directory, find the data cube and smooth its spectra
pathy = fils[i]
spectral_mean_cube,pathy,sig_cut,box_size,outtie
;print,i
endfor
end

