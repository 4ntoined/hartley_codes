;Antoine
function lonlat2xyz,lond,latd,unit=unit
;for now give coords in degrees [longitide, latitude]
conversion = !dpi/180.0
lon = lond * conversion
lat = latd * conversion
xx = cos( lon ) * cos( lat )
yy = sin( lon ) * cos( lat )
zz = sin(lat)
;print, xx^2+yy^2+zz^2
mag = sqrt( xx^2 + yy^2 + zz^2 )
;print,mag
;print,xx/mag
if keyword_set(unit) then begin
	xx = xx/mag
	yy = yy/mag
	zz = zz/mag
endif
ans = [xx,yy,zz]
return,ans
end
function targetBody,vertex_xyz,target_ll
; given a vertex in cartesian coords, see if it is close to a target lat long
; take the target radius to be the vertex radius
; convert both to xyz
; do a distance check
; if too distamce, vertex is not on target
;find radius of vertices w/ xyz
vrad = sqrt(total(vertex_xyz*vertex_xyz,1))
;converting target to xyz
target_llr = [target_ll[0],target_ll[1],vrad]
target_xyz = shape_ll2xyz(target_llr)
vert_target_distance = sqrt( (vertex_xyz[0,*]-target_xyz[0])^2 + $
	(vertex_xyz[1,*]-target_xyz[1])^2 + (vertex_xyz[2,*]-target_xyz[2])^2  )
return,vert_target_distance
end

function checkTriVert,vertices,triangs

checkedTri = triangs[0,*]*0
;checkedTri[i]
for i=0,n_elements(triangs[0,*])-1 do begin
vert1 = triangs[0,i]
vert2 = triangs[1,i]
vert3 = triangs[2,i]
d1=where( vertices eq vert1, count1 )
d2=where( vertices eq vert2, count2 )
d3=where( vertices eq vert3, count3 )
if  ((count1 gt 0) or (count2 gt 0) or (count3 gt 0)) then checkedTri[0,i]=1
endfor
return,checkedTri
end

pro shapecurves 
;so we have the sun and observer geometry... we need to initialize some jets, take some sums over facets
;and plot that over time (scan axis)

restore, '/home/antojr/hartley2/shape_model/h2_shape.sav'; vert, tri, conn
restore, '/home/antojr/hartley2/shape_model/obsdot-27.sav'; obss
restore, '/home/antojr/hartley2/shape_model/sundot-27.sav'; suns
;obss[i,*] all facets at time i
;my jet stuff from before
;get the area of all the plates
area = shape_tri_area(vert,tri)
;print,area
;print,size(area)
;jet games
target_lat = 70.
target_lon = 180.
targetll = [target_lat, target_lon]
dists = targetBody(vert,targetll) ;bolo is 2 dimensional, but its just 1 column
jet_radius = 0.2
close_to_target = where( dists lt jet_radius )
if isa(close_to_target,/array) then no_hits = BOOLEAN(0) else no_hits = BOOLEAN(1)
qfix = where(dists eq min(dists))
if no_hits then close_to_target = make_array(1,1,value=qfix[0])
;need to check which triangles use those vertices
jetflags = checkTriVert(close_to_target,tri)
checking = where(jetflags gt 0.0, ntrijets)
;print,'# triangs in jet: '+string(counta)
;going to multiply, sundot by areas and jetflags; take the sum?
;print,size(suns)
;sun2 = matrix_multiply(suns,area,/Btranspose, /Atranspose)
;print,size(sun2)
;print,ntrijets
;print,obss
;print,size(jetflags)
;print,size(matrix_multiply(jetflags,suns,/atranspose,/btranspose))
;go= matrix_multiply(jetflags,suns,/atranspose,/btranspose)
;print,size(go*area)
;print,suns[0,*]
;print,size(suns[0,*]*area)
suns2 = dblarr(1321)
;print,suns2[1320]
for i=0,n_elements(suns[*,0])-1 do begin

sunarea = suns[i,*]*area
;print,sunarea
sunjet = sunarea*jetflags
;print,sunjet
;print,sunjet
;print,suns2[i]
;print,total(sunjet,1)
suns2[i] = total(sunjet)
endfor
;print,suns2
;write_csv,'/home/antojr/codespace/ne_synth3.txt',suns2
return
end
