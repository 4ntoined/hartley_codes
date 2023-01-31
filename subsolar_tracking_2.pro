;this name was originally be used for something else so watch out for that
@hartley2_shape_display

pro subsolarpoints
;im gonna read in a bunch of julian dates
openr,1,'/home/antojr/stash/datatxt/scantimes_idl.txt'
scans = dblarr(2,1321)
readf,1,scans
close,1
jds = string(scans[1,*],format='(f12.4)')
;run shapelitness on each one of them
;print, typename(jds[14])
n_scans = n_elements(jds)
sun_lonlat = dblarr(2, n_scans)
obs_lonlat = dblarr(2,n_scans)
for i=0,n_scans-1 do begin

  hartley2_shape_display, jds[i], sun_lat=sun_lat, obs_lat=obs_lat, h2orient=1, /nodisp
  sun_lonlat[*,i] = sun_lat
  obs_lonlat[*,i] = obs_lat

endfor
;shapelitness,julian,outter,h2orient=2
;lights = string(lights)
;openw,2,'litness.txt'
;v3 denotes area, v2 no area accounting
;write_csv,'/home/antojr/stash/datatxt/litness_jetsun100_ambient_+70+180.txt',lights
;close,2
;print,sun_lonlat
;save, sun_lonlat, obs_lonlat, filename='sun_obs_lonlat.sav'
write_csv,'/home/antojr/codespace/results_code/shape_subsolar_lonlat.txt',sun_lonlat,header=['LON','LAT']
write_csv,'/home/antojr/codespace/results_code/shape_subobser_lonlat.txt',obs_lonlat,Header=['LON','LAT']
;oh she's over
return
end
