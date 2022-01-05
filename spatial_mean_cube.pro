;Antoine
;so this one will take a cube, preferably _final, will start with smooth cubes
;but no reason it wont also be applicable to the non smoothed
;I love writing code but not when it's difficult
@resistant_mean_nan

pro smooth_space,pathToCubeDirectory,sigma_cut,output
;cube goes [256,n_frames,512]
;sooo I will look at the non-doubled smooth cubes to work with
;
pathy = pathToCubeDirectory + '/cube_smooth_v1.fit'
data = readfits(pathy,head,/SILENT)
xsize = n_elements(data(*,0,0)) ;should always be 256 but i trust not myself nor computers
ysize = n_elements(data(0,*,0))
n_waves = n_elements(data(0,0,*)) ;also always 512 but ""
;gonna make up the rest from here

newcube = []
for x=0,xsize-1 do begin
;check if x=0: yes, check if y=0 or last (if yes: its a corner), no: its an edge
;check if x=last, same as above
;this should collect all the problem areas
;okay let's go
;nvm i will just check for each of 4 corners and the 4 sets of edges
;because they each need different protocols anyway
;pain
yline = []
for y=0,ysize-1 do begin
spec_line = fltarr(n_waves)
for z=0,n_waves-1 do begin
;#### corners ####
if (x eq 0) and (y eq 0) then begin ;corner 1
resistant_mean_nan,data[x:x+1,y:y+1,z],sigma_cut,boxavg,boxsig
endif else if (x eq 0) and (y eq ysize-1) then begin ;corner 2
resistant_mean_nan,data[x:x+1,y-1:y,z],sigma_cut,boxavg,boxsig
endif else if (x eq xsize-1) and (y eq ysize-1) then begin ;corner 3
resistant_mean_nan,data[x-1:x,y-1:y,z],sigma_cut,boxavg,boxsig
endif else if (x eq xsize-1) and (y eq 0) then begin ;corner 4
resistant_mean_nan,data[x-1:x,y:y+1,z],sigma_cut,boxavg,boxsig
;####  edges  ####
endif else if x eq 0 then begin ;edge 1, shouldnt run through the corners again
resistant_mean_nan,data[x:x+1,y-1:y+1,z],sigma_cut,boxavg,boxsig
endif else if y eq 0 then begin ;edge 2, these lines are skipped if a corner block activates
resistant_mean_nan,data[x-1:x+1,y:y+1,z],sigma_cut,boxavg,boxsig
endif else if x eq xsize-1 then begin ;edge 3, so these will only activate for the edges
resistant_mean_nan,data[x-1:x,y-1:y+1,z],sigma_cut,boxavg,boxsig
endif else if y eq ysize-1 then begin ;edge 4, yay
resistant_mean_nan,data[x-1:x+1,y-1:y,z],sigma_cut,boxavg,boxsig
;#### else ####
endif else begin ; checked for corners and edges, everything else is easy and simple
resistant_mean_nan,data[x-1:x+1,y-1:y+1,z],sigma_cut,boxavg,boxsig
endelse
spec_line[z] = boxavg
endfor ;for nwaves
zline = reform(spec_line, 1,1,n_waves,/overwrite)
yline = [[yline],[zline]]
endfor ;for ysize
newcube = [ newcube,yline ]
endfor ;for xsize
writefits,pathToCubeDirectory+'/cube_smoothspace_v1.fit',newcube,head
output = newcube
return
end

