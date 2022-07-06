;this name was originally be used for something else so watch out for that
@shapelitness_v2

pro shapecurves
;im gonna read in a bunch of julian dates
openr,1,'/home/antojr/stash/datatxt/scantimes_idl.txt'
scans = dblarr(2,1321)
readf,1,scans
close,1
jds = string(scans[1,*],format='(f12.4)')
;run shapelitness on each one of them
;print, typename(jds[14])
n_scans = n_elements(jds)
lights = dblarr(n_scans)
for i=0,n_scans-1 do begin

shapelitness,ghost,jds[i],h2orient=1,/nodisp
lights[i] = ghost
print,'done with ',i

endfor
;shapelitness,julian,outter,h2orient=2
;lights = string(lights)
;openw,2,'litness.txt'
;v3 denotes area, v2 no area accouting
write_csv,'litness_v3_27.txt',lights
;close,2

;oh she's over
return
end
