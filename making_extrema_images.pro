;Antoine
pro making
;need to do h2o peaks3 (6), co2 peaks 123 (~18), all troughs (~36) (..double all of this to account for the suns view.... bye)
;...can i curse
pr = '/home/antojr/codespace/results_code/'
saving_here = [pr+ 'pngs_peaks3/shape_h2o_', pr+'pngs_peaks1/shape_co2_',pr+'pngs_peaks2/shape_co2_',pr+'pngs_peaks3/shape_co2_'   ]
saving_suns = [ pr+'pngs_peaks3/shape_sun_h2o_', pr+'pngs_peaks1/shape_sun_co2_',pr+'pngs_peaks2/shape_sun_co2_',pr+'pngs_peaks3/shape_sun_co2_'   ]
saving_3 = [ pr+'pngs_trous1/shape_h2o_', pr+'pngs_trous2/shape_h2o_',pr+'pngs_trous3/shape_h2o_',pr+'pngs_trous1/shape_co2_',pr+'pngs_trous2/shape_co2_',pr+'pngs_trous3/shape_co2_' ]
saving_4 = [ pr+'pngs_trous1/shape_sun_h2o_', pr+'pngs_trous2/shape_sun_h2o_',pr+'pngs_trous3/shape_sun_h2o_',pr+'pngs_trous1/shape_sun_co2_',pr+'pngs_trous2/shape_sun_co2_',pr+'pngs_trous3/shape_sun_co2_' ]
alph = ['A','B','C','D','E','F']

;timers = double(readfits('/home/antojr/codespace/results_code/peak_times.fits'))
;timers = double(readfits('/home/antojr/codespace/results_code/peak_times_2.fit',/no_unsigned))
;timers[3 6, 2, 2]
; so then 
;timers = timers + 2455000.000000000
;timers = string(timers)
;print,timers[1]
;timing2 = [ timers[0,*,1,0],timers[1,*,1,0],timers[2,*,1,0],timers[0,*,1,1],timers[1,*,1,1],timers[2,*,1,1]]
timing2 = [ ['2455506.45542973','2455508.77423631','2455511.09304288','2455513.37986593','24555.6506972','2455518.01747908'], $
	    ['-99.','2455509.42989886','2455511.78068897','2455514.13147909','2455516.38631859','-99.'], $
	    ['2455507.9906396','2455510.29345441','2455512.56428568','2455514.86710049','-99.','-99.'], $
	    ['2455506.40745442','2455508.726261','2455511.01308404','2455513.36387416','2455515.6506972','2455518.00148731'], $
	    ['-99.','2455509.42989886','2455511.70073013','2455514.05152025','2455516.38631859','-99.'], $
	    ['2455507.97464783','2455510.26147087','2455512.54829391','2455514.85110872','-99.','-990']  ]
print, timing2[1,3]
timingr = [ [ '-99.', '2455509.74973425','2455512.05254906','2455514.46730625','2455516.85007991','-99.'], $
	['2455505.99166841','2455508.27849145','2455510.59729803','2455512.88412107','2455515.15495234','-99.' ], $
	['2455506.83926219','2455509.12605524','2455511.42887004','2455513.71569309','2455516.01850789','2455518.3213227'], $
	['-99.','2455509.717755071','2455512.00457375','2455514.30738856','2455516.74613341','-99.'] ]

;print,timingr[ 1,3  ]

for k=0,1 do begin; for sun and no sun sigh

for i =0,5 do begin ;for the 4 peaks i have left

for j =0,5 do begin ;for the 6 cycles in the cycling

;secret_variable = 2.
;if timingr[j,i] ne '-99.' then begin
if timing2[j,i] ne '-99.' then begin

;peaks
;if k eq 0 then hartley2_shape_display, timingr[ j,i ] , h2orient=1,/axes,/save_disp, save_name = saving_here[ i ]+alph[ j ]+'.png'  $
;else if k eq 1 then hartley2_shape_display, timingr[ j,i ] , h2orient=1,/axes,/save_disp,/sunobs,save_name = saving_suns[ i ]+alph[ j ]+'.png'

;troughs
if k eq 0 then hartley2_shape_display, timing2[j,i]  , h2orient=1,/axes,/save_disp, save_name = saving_3[ i ]+alph[ j ]+'.png'  $
else if k eq 1 then hartley2_shape_display, timing2[j,i]  , h2orient=1,/axes,/save_disp,/sunobs,save_name = saving_4[ i ]+alph[ j ]+'.png'


endif 

endfor

endfor

endfor

return
end

