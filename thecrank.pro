@bulk_calibrate

pro turn,dark_path,dark_scale,start_here
;so dark path will be a path to the normalized master dark
;dark_scale really only needs to be the dark level best fit
;those numbers we already have for every scan so we need only
;put them in idl form
;and will need to make connection between a filename

thefiles = file_search("/chiron5/Sandbox/holt/Hartley2/ir/raw/","*.fit")
;reading in the dark data
openr,1,dark_scale
darkdat = fltarr(8,1321)
readf,1,darkdat
close,1
;darkdat[n,*] gives the nth column of dark_temp.dat
;(jd,temp,darklevel,darkbestfit,exptime,doy,expid(is wrong bc no underscores),outlier flag)
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

for i=start_here,n_scans-1 do begin

doy = fix(darkdat[5,i])
doy = strtrim(string(doy),1)
exx = (exps[0,i])
direc = '/chiron5/Sandbox/holt/Hartley2/ir/raw/'+doy+'/'+exx+'/'
saveHere = '/chiron4/antojr/calibrated_ir/'+doy+'.'+exx+'/'
drk_scl = darkdat[3,i] * darkdat[4]

bulk_calibrate, direc, dark, drk_scl, saveHere
print,i
endfor ;done with this scan
end
