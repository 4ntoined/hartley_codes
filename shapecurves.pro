@shape_plate_normal
@dot_product
;
function deg2rad, degree
ans = degree * !dpi / 180.0
return,ans
end
;
function rad2deg, radian
ans = radian * 180.0/!dpi
return,ans
end
;
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
;
pro shapecurves,jd,h2orient=h2orient
restore,filename='/home/antojr/hartley2/shape_model/Hartley2_variables.sav'
reads,jd,jd1,format='(f15.7)'    ; Time is a julian day
jdltc = jd1                     ; light travel time is accounted for in the spice
rasc = interpol(raspcr,jddi,jdltc)   
decsc = interpol(decspcr,jddi,jdltc)   
ras = interpol(rasun,jdg,jdltc)   
decs = interpol(decsun,jdg,jdltc)   
obsra = [180.+rasc , -1.*decsc]
sunra = [180.+ras , -1.*decs]
range = interpol(scrange,jddi,jdltc)
ncp_ca = (interpol(ncpclkang,jddi,jd1) + 270.) mod 360.
;
obspos = radec2xyz(obsra)
sunpos = radec2xyz(sunra)
;choosing 27- vs 54-hour roll period w/ h2orient
if keyword_set(h2orient) then h2or = h2orient else h2or = 2
case h2or of
  1: begin
;       print,'Using orientations for Beltons 27 hour roll period '
       modeldesc = 'Belton, 27.8 hr roll period'
       amv_rd = [58.88,58.12]
       nor = size(jdor,/n_elements)
;    check to see if the time is defined
       if jd1 lt jdor[0] or jd1 gt jdor[nor-1] then begin
         print,' Nucleus orientation not defined for the given time - Returning'
         return
       endif
;    interpololate the nucleus positions from belton's 27 day period section
       ralong = (360.+interpol(ra1,jdor,jdltc)) mod 360. ; long axis
       declong = interpol(dec1,jdor,jdltc)
       raint = (360.+ interpol(ra2,jdor,jdltc)) mod 360. ; intermediate axis
       decint = interpol(dec2,jdor,jdltc)
     end
  2: begin
;       print,'Using orientations for Beltons 54 hour roll period '
       modeldesc = 'Belton, 54.4 hr roll period'
       amv_rd = [58.79,54.78]
       nor = size(jdor,/n_elements)
;    check to see if the time is defined
       if jd1 lt jdor[0] or jd1 gt jdor[nor-1] then begin
         print,' Nucleus orientation not defined for the given time - Returning'
         return
       endif
;    interpololate the nucleus positions from belton's 54 day period section
       ralong = (360.+interpol(ra3,jdor,jdltc)) mod 360. ; long axis
       declong = interpol(dec3,jdor,jdltc)
       raint = (360.+interpol(ra4,jdor,jdltc)) mod 360.  ; intermediate axis
       decint = interpol(dec4,jdor,jdltc)
     end
  else: begin
          print,' File for nucleus orientations not defined - Returning'
          return
        end
endcase
;
zpos = radec2xyz([ralong,declong])
ypos = radec2xyz([raint,decint])
xpos = cross_product(ypos,zpos)
;
shape_read_model,'H2',vert,tri,conn,skipline=0
;   vert(3,nvert)     float   array of vertex coordinates 
;   tri(3,ntri)       ulong   array of connections for triangular plates
;   conn(3*ntri)      ulong   vector containing connectivity in IDL format
;   skipline          int     number of header lines to skip 
;print,obspos
;print,sunpos
;
;shape_plate_normal = compute normal vectors given model plates
;plane_intersect_coords = longitude, latitude coords where ??
;points2plane = create a plane from 3 points
;shape_tri_area = area of a triangle on the shape model!, will need
;image2body
;body2image

;vec1_triang_intersect = where a single vector intersects, HAVE
;vecs_triang_intersect = when a/some vector(s) in a set intersects (not where), HAVE
;ll_plot = lat.long info for nucleus ?
;model_display to show shape model w/ orientation, may not be necessary, HAVE
;print,vert[0,*] <- rips 1 from each trio
;print,vert[*,0] <- rips a trio

;print,size(conn)
;print,vert[*,0:2]
;print,""
;print,conn[0:11]
model_display,vert,conn,xpos,zpos,obspos,sunpos,ncp_ca,geom_ret=geom_ret, /axes
;xpos,
;ncp_ca
help,geom_ret

shape_plate_normal,vert,conn,vecs,/unit
ntri = size(vecs)
ntri = ntri[2]
print,"Triangles in the shape model: ",ntri
;print,vecs[*,0:10]
;print,vecs[0,5]^2 + vecs[1,5]^2 + vecs[2,5]^2
;print,obspos
;print,sunpos
print,"ObsPos: ",geom_ret.sub_obs_lon,geom_ret.sub_obs_lat
print,"SunPos: ",geom_ret.sub_sol_lon,geom_ret.sub_sol_lat
;print,xyz2radec(obspos)
;print,radec2xyz(geom_ret.zax_radec)
print,"ObRaDec:",geom_ret.obs_radec
print,"SunRaDec",geom_ret.sun_radec
;print,geom_ret.sub_obs_lon,geom_ret.sub_obs_lat
;
;creating xyz vectors from sub- solar and observer lats and longs
;slon = geom_ret.sub_sol_lon * !dpi/180.0
;slat = geom_ret.sub_sol_lat * !dpi/180.0
;olon = geom_ret.sub_obs_lon * !dpi/180.0
;olat = geom_ret.sub_obs_lat * !dpi/180.0
;sxx = cos( slon ) * cos( slat )
;syy = sin( slon ) * cos( slat )
;szz = sin( slat )
;print,sxx,syy,szz
;
;turning longlat solar and observer coords into xyz coords
obsxyz = lonlat2xyz(geom_ret.sub_obs_lon,geom_ret.sub_obs_lat,unit=1)
sunxyz = lonlat2xyz(geom_ret.sub_sol_lon,geom_ret.sub_sol_lat,unit=0)
print,"ObsXYZ: ",obsxyz
print,"SunXYZ: ",sunxyz
;calculating incidence of shape plates with sun and observer
obsdot = dot_product(obsxyz,vecs)
sundot = dot_product(sunxyz,vecs)
;print,"Shape plates (dot) observer: ",obsdot[0:100]
;print,"Shape plates (dot) solar   : ",sundot[0:100]
;
;if not facing (dot product less than 0) set to 0
obsdot[where(obsdot lt 0.)] = 0.
sundot[where(sundot lt 0.)] = 0.
print,"Shape plates' light to obs: ",obsdot[0:10]
print,"Sunlight to shape plates  : ",sundot[0:10]
;multiply the sun angle result with the observer angle result
seeing = matrix_multiply(obsdot,sundot,/btranspose)
seeing = diag_matrix(seeing)
;print,size(obsdot)
;print,size(sundot)
;print,size(seeing)
print,"Brightness of shape plates: "
print,seeing[0:10]
;print,""
;print,obsdot[0]*sundot[0],obsdot[1]*sundot[1],obsdot[2]*sundot[2],obsdot[3]*sundot[3]
;print,size(seeing)
;sum brightness of all the plates!
shape = total(seeing)
print,"Litness of the shape @ "+jd+': ',shape

return
end
