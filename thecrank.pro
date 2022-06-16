@bulk_calibrate

pro turn,dark_path,dark_scale
;dark_path = STRING, path to normalized master dark
;dark_scale = STRING, path to dark vs temp file 
;
thefiles = file_search("/chiron5/Sandbox/holt/Hartley2/ir/raw/","*.fit")
;reading in the dark data
openr,1,dark_scale
darkdat = fltarr(8,1321)
readf,1,darkdat
close,1
;darkdat[n,*] gives the nth column of dark_temp.dat
;(jd,temp,darklevel,darkbestfit,exptime,doy,expid,outlier flag)
openr,1,"/home/antojr/stash/datatxt/expss.txt"
exps = strarr(1,1321)
readf,1,exps
close,1
;exps contains the correct exposure id data
;proper dark scale will be the bestfitlevel times the exposure time
;now here is a process we will run for every line in our dark_temp_file
n_scans = n_elements(darkdat(0,*))
dark = double(readfits(dark_path,/silent))
print,"read in the dark"
;print,darkdat[5,4]
;print,fix(darkdat[5,*])

for i=0,n_scans-1 do begin

doy = fix(darkdat[5,i])
doy = strtrim(string(doy),1)
exx = (exps[i])
direc = '/chiron5/Sandbox/holt/Hartley2/ir/raw/'+doy+'/'+exx+'/'
saveHere = '/chiron4/antojr/calibrated_ir/'+doy+'.'+exx+'/'
drk_scl = darkdat[3,i] * darkdat[4,i]
bulk_calibrate, direc, dark, drk_scl, saveHere
print,i

endfor ;done with this scan
end
