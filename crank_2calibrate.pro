@bulk_2calibrate
;Antoine
;this idl procedure calibrates the hartley 2 Ir data from DOYS 298-321
;dont know offhand the common dates and Im not gonna look it up
;this code uses a master dark frame that I created for the IR H2-flyby data
;it once used some complicated formulation to set the scale factor used on the dark
;but it turns out that's trash and I get better results by just using, for each scan,
;;the inscene dark frame as a reference for how to scale the master
;how cool is that

pro turn, inscene=inscene
;dark_path = STRING, path to normalized master dark
;dark_scale = STRING, path to dark vs temp file 
;
;thefiles = file_search("/chiron5/Sandbox/holt/Hartley2/ir/raw/","*.fit")

dark_path_master = '/alcyone1/antojr/downloading_h2/darkmatters/masterdark_vA.fit'	; 1 frame
dark_path_inscene = '/alcyone1/antojr/downloading_h2/darkmatters/dark_linears.fit'	; frame for each scan (1320)
dark_mean_path  = '/alcyone1/antojr/downloading_h2/darkmatters/dark_means_mean.fit'	; float for each scan (1320)
metapath = '/alcyone1/antojr/downloading_h2/raw/filtered_list.txt'			; assorted collected datas
saveroot = '/alcyone1/antojr/cali/'
;dark_scale = 
; DETERMINE SCANLIST ;
;topdir = '/alcyone1/antojr/downloading_h2/raw/'
;metapath = '/alcyone1/antojr/downloading_h2/raw/filtered_list.txt'
readcol,metapath,cindex,expid,cjd,exptime,cframes,cbinff,cpxl,cdist,ctemp,scanpath,format='I,A,F,F,I,A,F,F,F,A',skipline=1
nscans = n_elements( scanpath )

; PREPARE THE DARK ;
; for in-scene, use the linearized dark, scaling factor of 1.0
; for master, use normaled, weighted, m-dark, load in scaling factors
; SCALE ;
if keyword_set( inscene ) then begin	;inscene dark

dark_scale = fltarr(nscans) + 1.
dark = double(readfits(dark_path_inscene,/silent))

endif else begin			;master dark

meaned = double(readfits(dark_mean_path))
dark_scale = meaned * exptime

dark1 = double(readfits(dark_path_master,/silent))
dsize = size(dark1,/dimensions)
dark = fltarr( dsize[0], dsize[1], nscans )
for i=0,nscans-1 do dark[*,*,i] = dark1

endelse

print,"read in the dark"

;reading in the dark scaling data
;openr,1,dark_scale
;darkdat = fltarr(8,1321)
;readf,1,darkdat
;close,1
;darkdat[n,*] gives the nth column of dark_temp.dat
;(jd,temp,darklevel,darkbestfit,exptime,doy,expid,outlier flag)
;openr,1,"/home/antojr/stash/datatxt/expss.txt"
;exps = strarr(1,1321)
;readf,1,exps
;close,1

;loop
for i=0,nscans-1 do begin
;
;doy = fix(darkdat[5,i])
;doy = strtrim(string(doy),1)
;exx = (exps[i])
;direc = '/chiron5/Sandbox/holt/Hartley2/ir/raw/'+doy+'/'+exx+'/'
;saveHere = '/chiron4/antojr/calibrated_ir/'+doy+'.'+exx+'/'
direc = scanpath[i]
savehere = saveroot + expid[i] + '/'
drk_scl = dark_scale[i]
;drk_scl = darkdat[2,i] * darkdat[4,i]
bulk_calibrate, direc, dark[*,*,i], drk_scl, savehere
;print,i
;
endfor
end

