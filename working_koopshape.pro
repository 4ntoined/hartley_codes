;this name was originally be used for something else so watch out for that
@working_shapelit

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
;lights = dblarr(n_scans)
n_tris=20584
obs = dblarr(n_scans,n_tris)
sun = dblarr(n_scans,n_tris)

for i=0,n_scans-1 do begin

shapelitness,sundot,obsdot,jds[i],70,180,h2orient=1,/nodisp
;print,size(sundot)
sun[i,*] = sundot
obs[i,*] = obsdot
;print,size(sun[i,*])
endfor
print,sun[0:2,*]
;shapelitness,julian,outter,h2orient=2
;lights = string(lights)
;openw,2,'litness.txt'
;v3 denotes area, v2 no area accounting
save,filename='sundot-54-2.sav',sun
save,filename='obsdot-54-2.sav',obs


;write_csv,'ne_synth4.txt',s
;close,2

;oh she's over
return
end
