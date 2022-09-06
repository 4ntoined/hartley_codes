@bulk_pipeline

pro bulk_calibrate, filedir, dark_frame, dark_scale, directoryToSave
;
;dark = double(readfits(dark_frame)) already provided by thecrank when used in wider context
files = file_search(filedir, "hi*.fit", count=n_frames)
;
;file_mkdir,directoryToSave

for i=0,n_frames-1 do begin
	frame = double(readfits(files[i],frameheader,/SILENT))
	Hartley2_pipeline, frame,frameheader,dark_frame,dark_scale,ohf,ohw
	fname = directoryToSave + "/dal_" + string(format='(I03)',i+1) + '.fit'
	writefits,fname,ohf,frameheader
	writefits,fname,ohw,/append
endfor
end

