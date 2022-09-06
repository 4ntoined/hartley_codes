@bulk_calibrate
;Antoine
;this idl procedure calibrates the hartley 2 Ir data from DOYS 298-321
;dont know offhand the common dates and Im not gonna look it up
;this code uses a master dark frame that I created for the IR H2-flyby data
;it once used some complicated formulation to set the scale factor used on the dark
;but it turns out that's trash and I get better results by just using, for each scan,
;;the inscene dark frame as a reference for how to scale the master
;how cool is that

pro turn,dark_path,dark_scale
;dark_path = STRING, path to normalized master dark
;dark_scale = STRING, path to dark vs temp file 
;
thefiles = file_search("/chiron5/Sandbox/holt/Hartley2/ir/raw/","*.fit")
;reading in the dark scaling data
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
n_scans = n_elements(darkdat(0,*))
;load up the master dark frame
dark = double(readfits(dark_path,/silent))
print,"read in the dark"
;loop
for i=0,n_scans-1 do begin
;
doy = fix(darkdat[5,i])
doy = strtrim(string(doy),1)
exx = (exps[i])
direc = '/chiron5/Sandbox/holt/Hartley2/ir/raw/'+doy+'/'+exx+'/'
saveHere = '/chiron4/antojr/calibrated_ir/'+doy+'.'+exx+'/'
drk_scl = darkdat[2,i] * darkdat[4,i]
bulk_calibrate, direc, dark, drk_scl, saveHere
;print,i
endfor
end

