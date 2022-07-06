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

pro shapelitness, lumos, jd, h2orient=h2orient, obsradec=radec, earth=earth, $
         ncp_ca=ncp_ca, grid=grid, axes=axes, sunvec=sunvec, amv_plot=amv_plot, $
         ncp_spice=ncp_spice, print_geom=print_geom,print_mess=print_mess, obs_lat=obs_lat,sun_lat=sun_lat,$
         longax_clk = longax_clk,nodisp=nodisp,sunobs=sunobs,axis_ornt=axis_ornt
;hey it's antoine I'm editing stuff
;  Routine to display the shape model orientation of Comet Hartley 2 for any
;      given geometry
;
;  Currently only valid from E-45 to E+22.6 days (set by the time frame of
;     the nucleus orientations in Belton's file.;
; 
;  Inputs:
;     JD (string)   Time at which to display the shape model
;                   if first character is a 'P' then it is taken as days from perihelion
;                   if first character is a 'E' then it is taken as days from encounter
;     H2ORIENT      Determines what nucleus orientation to use
;                        1 = Belton's 27 hr 
;                        2 = Belton's 54 hr (default) 
;     OBSRADEC[2]   RA & Dec of the comet as seen from the observer (deg) at JD
;                   Defaults to the DI spacecraft
;     EARTH         Flag that sets the observer to the Earth (overrides OBSRADEC)
;     SUNOBS        Flag that sets the observer to the Sun (overrides OBSRADEC)
;     NCP_CA        clock angle of the north celestial pole in the image (deg)
;                   Defaults to 0, and is overridden when SPICE is available
;                   for DI
;     GRID          flag for plotting only the wireframe grid of the surface
;                      (not yet implemented)
;     AXES          flag for plotting the body coordinate axes
;     SUNVEC        flag for plotting the sunward vector
;     AMV_PLOT      flag for plotting the ang mom vector
;     NCP_SPICE     flag, if set, forces NCP to come from spice calculations (DI only)
;     PRINT_GEOM    flag for printing out the geometry information
;     NODISP        flag to skip the display section
;
;   Optional Returned
;     OBS_LAT(2)    long and lat of the observer on the comet coordinates
;     SUN_LAT(2)    long and lat of the sun on the comet coordinates
;     LONGAX_CLK    clock angle of the long axis
;     AXIS_ORNT(3,2) RA and Dec of the short, int and long axes of the nucleus
;================================================================================================
;  Uses data stored in the save file Hartley2_variables.sav,  produced using:
;
;  Updated to use the SPICE calculations of Belton's pole orientation
;
; readcol,'/users/farnham/Home/IDL/Shape_models/Models/Hartley2_support/H2_sun_positions.dat',$
;   jdg,rasun,decsun,raerth,decerth,delta,format='(d,f,f,f,f,d)',/silent,skip=6
; readcol,'/users/farnham/Home/IDL/Shape_models/Models/Hartley2_support/Hartley2_xyz_orient_incr.dat',$
;   jdor,tor,ra1,dec1,ra2,dec2,ra3,dec3,ra4,dec4,format='(d,f,f,f,f,f,f,f,f,f,)',skip=7,/silent
; readcol,'/users/farnham/Home/IDL/Shape_models/Models/Hartley2_support/DI_positions.dat',$
;   jddi,raspcr,decspcr,scrange,ncpclkang,format='(d,f,f,f,f)',/silent,skip=6
; save,jdg,rasun,decsun,raerth,decerth,delta,jdor,tor,ra1,dec1,ra2,dec2,ra3,dec3,ra4,dec4,jddi,$
;   raspcr,decspcr,scrange,ncpclkang, description='Nucleus orientation and Earth and sun geometry for Hartley 2',$
;   filename='/home/antojr/hartley2/shape_model/Hartley2_variables.sav'
;================================================================================================
;

on_error, 2

if n_params() lt 1 then begin
  print,'Usage: hartley2_shape_display, jd [,h2orient=h2orient][,obsradec=radec][,ncp_ca=ncp_ca]'
  print,'                               [,/earth][,/sunobs][,/grid][,/axes][,/sunvec][,amv_plot=amv_plot]'
  print,'                               [,/ncp_spice][,/print_geom][,axis_ornt=axis_ornt][,/nodisp]'
  return
endif

; restore the nucleus orientation and sun/earth geometry data
restore,filename='/home/antojr/hartley2/shape_model/Hartley2_variables.sav'

;-------------------------------------------------------------------------------------------
; Deal with the time of the observation
p1 = strupcase(strmid(jd,0,1))
jd1=1.0d
case p1 of
  'P': begin   ;   Time is given as offset from perihelion
       reads,jd,tim1,format='(x,f10.7)'
       jd1 = 2455497.756967203d + tim1
     end
  'E': begin    ;   Time is given as offset from encounter
       reads,jd,tim1,format='(x,f10.7)'
       jd1 = 2455505.0831865d + tim1
     end 
  '2': reads,jd,jd1,format='(f15.7)'    ; Time is a julian day
  else:  begin      ; Not consistent with any of these times
         print,'JD not recognized'
         return
       end
endcase

if jd1 lt 2455443.d or jd1 gt 2455527.d  then begin
  print,' Date is out of range for rotation information - Exiting'
  return
endif

;print,'JD1 = ',jd1,format='(a,f15.7)'

;-------------------------------------------------------------------------------------------
; determine what observer is used
obs = 0     ; Default Observer is DI
if keyword_set(radec) then obs=3
if keyword_set(sunobs) then obs=2
if keyword_set(earth) then obs=1 

; get the ra and dec for the sun and observer
jdltc = jd1                     ; light travel time is accounted for in the spice
case obs of 
   0: begin 
;     sp1 = spice_info(string(jd1,format='(f15.7)'),6,/jd,/noprint)
;     obsra = [180.+sp1.target_ra , -1.*sp1.target_dec]
;     sunra = [180.+sp1.target_ra_sun , -1.*sp1.target_dec_sun]
;     range = sp1.obs_trg_dist
     rasc = interpol(raspcr,jddi,jdltc)   
     decsc = interpol(decspcr,jddi,jdltc)   
     ras = interpol(rasun,jdg,jdltc)   
     decs = interpol(decsun,jdg,jdltc)   
     obsra = [180.+rasc , -1.*decsc]
     sunra = [180.+ras , -1.*decs]
     range = interpol(scrange,jddi,jdltc)

     ncp_ca = (interpol(ncpclkang,jddi,jd1) + 270.) mod 360.
     if keyword_set(ncp_spice) then ncp_ca = (sp1.equn_clkang+270.) mod 360.
     ;  for close approach, always use the spice value
;     if range lt 5000. then ncp_ca = (sp1.equn_clkang+270.) mod 360.
     desc1 = 'DI      '+jd
   end
  1: begin    ; Earth is the observer
;     sp1 = spice_info(string(jd1,format='(f15.7)'),5,/jd,/noprint)
;     range = sp1.obs_trg_dist
;     obsra = [180.+sp1.target_ra , -1.*sp1.target_dec]
;     sunra = [180.+sp1.target_ra_sun , -1.*sp1.target_dec_sun]
     rae = interpol(raerth,jdg,jdltc)   
     dece = interpol(decerth,jdg,jdltc)   
     ras = interpol(rasun,jdg,jdltc)   
     decs = interpol(decsun,jdg,jdltc)   
     range = interpol(delta,jdg,jdltc)   
     ncp_ca = 0
     obsra = [180.+rae ,-1.*dece]
     sunra = [180.+ras ,-1.*decs]
     desc1 = 'Earth    '+jd
     end
  2: begin    ; Sun is the observer direction (don't correct for light time)
;     sp1 = spice_info(string(jd1,format='(f15.7)'),6,/jd,/noprint)
;     sunra = [180.+sp1.target_ra_sun , -1.*sp1.target_dec_sun]
;     obsra = [180.+sp1.target_ra_sun , -1.*sp1.target_dec_sun]
     ras = interpol(rasun,jdg,jd1)   
     decs = interpol(decsun,jdg,jd1)   
     ncp_ca = 0
     sunra = [180.+ras, -1.*decs]
     obsra = [180.+ras , -1.*decs]
     desc1 = 'Sun    '+jd
     end
  3: begin    ; ra and dec of the observer are given (range unknown)
     ras = interpol(rasun,jdg,jdltc)   
     decs = interpol(decsun,jdg,jdltc)   
     if not keyword_set(ncp_ca) then ncp_ca = 0.
     obsra = [180+radec[0],-1.*radec[1]]
     sunra = [180+ras,-1.*decs]
     desc1 = string(radec,format='(f5.1,",",f5.1," ")')+jd
     end
endcase
obspos = radec2xyz(obsra)
sunpos = radec2xyz(sunra)
;print,'obsra = ',obsra
;print,'sunra = ',sunra
;q1=dot_product(obspos,sunpos,angle=ang)
;print,ang/!dtor

;-------------------------------------------------------------------------------------------
; read in the nucleus orientation data and check to make sure it's
; defined for the JD of interest.

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
;
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

; compute the position vectors for the axes, and get the short axis position
zpos = radec2xyz([ralong,declong])
ypos = radec2xyz([raint,decint])
xpos = cross_product(ypos,zpos)
;print,[ralong,declong]
;print,[raint,decint]
;print,'ralong = ',ralong,declong
;print,'rashrt = ',xyz2radec(xpos)

;-------------------------------------------------------------------------------------------
; now call the display routine to show the shape model 

; read in the shape model 
shape_read_model,'H2',vert,tri,conn,skipline=0
area = shape_tri_area(vert,tri)

;print,vert[*,100:105]
;print,size(area)

model_display,vert,conn,xpos,zpos,obspos,sunpos,ncp_ca,axes=axes,sunvec=sunvec,$
   text=desc1,geom_ret=geom_ret,nodisp=nodisp,amv_rd=amv_rd,amv_plot=amv_plot

if keyword_set(print_geom) then begin
  f1='(a,2x,f7.3,3x,f7.3,3x,f7.3)'
  print,'===================================================='
  print,'   Observer and time    ',desc1 ,format='(a,a)'
  print,'   Julian Date          ',jd1,format='(a,f15.7)'
  print,'   Rotation Model       ',modeldesc,format='(a,a)'
  print,' '
  print,'       Vector                 RA       Dec'
  print,'   --------------------    -------   -------'
  print,'   Observer              ',geom_ret.OBS_RADEC,format=f1       
  print,'   Sun                   ',geom_ret.SUN_RADEC,format=f1       
  print,'   Ang. Mom. Vector      ',geom_ret.AMV_RADEC,format=f1       
  print,'   Long Axis             ',geom_ret.ZAX_RADEC,format=f1       
  print,'   Intermediate Axis     ',raint,decint,format=f1       
  print,'   Short Axis            ',geom_ret.XAX_RADEC,format=f1       
  print,' '
  print,'                           Clk_Ang   Aspect      Sun'
  print,'   --------------------    -------   -------  --------'
  print,'   North Cel. Pole       ',geom_ret.NCP_CLKANG,$
         geom_ret.NCP_ASPECT,format=f1        
  print,'   Sun Vector            ',geom_ret.SUN_CLKANG,$
         geom_ret.SUN_ASPECT,format=f1        
  print,'   Ang. Mom. Vector      ',geom_ret.AMV_CLKANG,$
         geom_ret.AMV_ASPECT,format=f1        
  print,'   Long Axis             ',geom_ret.ZAX_CLKANG,$
         geom_ret.ZAX_ASPECT,geom_ret.ZAX_SUN_ANG,format=f1     
  print,'   Intermediate Axis     ',geom_ret.YAX_CLKANG,$
         geom_ret.YAX_ASPECT,geom_ret.YAX_SUN_ANG,format=f1      
  print,'   Short Axis            ',geom_ret.XAX_CLKANG,$
         geom_ret.XAX_ASPECT,geom_ret.XAX_SUN_ANG,format=f1    
;  print,'   Long Axis             ',geom_ret.LONGAX_CLKANG,$
;         geom_ret.LONGAX_ASPECT,geom_ret.LONGAX_SUN_ANG,format=f1     
;  print,'   Intermediate Axis     ',geom_ret.INTAX_CLKANG,$
;         geom_ret.INTAX_ASPECT,geom_ret.INTAX_SUN_ANG,format=f1      
;  print,'   Short Axis            ',geom_ret.SHORTAX_CLKANG,$
;         geom_ret.SHORTAX_ASPECT,geom_ret.SHORTAX_SUN_ANG,format=f1    
  print,' '
  print,'   Sub-XX  Points            Long      Lat'
  print,'   --------------------    -------   -------'
  print,'   Observer              ',geom_ret.SUB_OBS_LON,geom_ret.SUB_OBS_LAT,format=f1        
  print,'   Solar                 ',geom_ret.SUB_SOL_LON,geom_ret.SUB_SOL_LAT,format=f1        
  print,'===================================================='
endif

obs_lat = [geom_ret.SUB_OBS_LON,geom_ret.SUB_OBS_LAT]
sun_lat = [geom_ret.SUB_SOL_LON,geom_ret.SUB_SOL_LAT]
longax_clk = geom_ret.ZAX_CLKANG
axis_ornt = fltarr(3,2)
axis_ornt[0,*] = geom_ret.XAX_RADEC
axis_ornt[1,*] = [raint,decint]
axis_ornt[2,*] = geom_ret.ZAX_RADEC


;;;;Antoine's super cool reflected light calculation code;;;;;

;where are the normal vectors of all the plates in XYZ coords
shape_plate_normal,vert,conn,vecs,/unit
ntri = size(vecs)
ntri = ntri[2]
;print,vecs[*,0:10]
;print,vecs[0,5]^2 + vecs[1,5]^2 + vecs[2,5]^2
;print,obspos
;print,sunpos
;print,xyz2radec(obspos)
;print,radec2xyz(geom_ret.zax_radec)
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
sunxyz = lonlat2xyz(geom_ret.sub_sol_lon,geom_ret.sub_sol_lat,unit=1)
;calculating incidence of shape plates with sun and observer
obsdot = dot_product(obsxyz,vecs)
sundot = dot_product(sunxyz,vecs)
;print,"Shape plates (dot) observer: ",obsdot[0:100]
;print,"Shape plates (dot) solar   : ",sundot[0:100]
;
;if not facing (dot product less than 0) set to 0
obsdot[where(obsdot lt 0.)] = 0.
sundot[where(sundot lt 0.)] = 0.
;multiply the sun angle result with the observer angle result
seeing = matrix_multiply(obsdot,sundot,/btranspose)
seeing = diag_matrix(seeing)
;print,seeing[1000:1010]
;print,area[1000:1010]
;; account for area of triangles
seeing = matrix_multiply(seeing, area,/btranspose)
seeing = diag_matrix(seeing)
;print,seeing[1000:1010]
;print,seeing[1000:1010]/seein
;print,size(obsdot)
;print,size(sundot)
;print,size(seeing)
;print,""
;print,obsdot[0]*sundot[0],obsdot[1]*sundot[1],obsdot[2]*sundot[2],obsdot[3]*sundot[3]
;print,size(seeing)
;sum brightness of all the plates!
lumos = total(seeing)

if keyword_set(print_mess) then begin

print,"Triangles in the shape model: ",ntri
print,"ObsPos: ",geom_ret.sub_obs_lon,geom_ret.sub_obs_lat
print,"SunPos: ",geom_ret.sub_sol_lon,geom_ret.sub_sol_lat
print,"ObRaDec:",geom_ret.obs_radec
print,"SunRaDec",geom_ret.sun_radec
print,"ObsXYZ: ",obsxyz
print,"SunXYZ: ",sunxyz
print,"Shape plates' light to obs: ",obsdot[0:10]
print,"Sunlight to shape plates  : ",sundot[0:10]
print,"Brightness of shape plates: "
print,seeing[0:10]
print,"Litness of the shape @ "+jd+': ',lumos

endif

return
end

