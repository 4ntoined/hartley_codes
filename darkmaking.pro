@master_dark


pro darker

darkfilename = "/alcyone1/antojr/downloading_h2/rawdarks.fit"
sigma_cut = 2.5
rawdarks = readfits(darkfilename ,header)
savepath = '/alcyone1/antojr/downloading_h2/darkmatters/'
metapath = '/alcyone1/antojr/downloading_h2/raw/filtered_list.txt'

master_dark, rawdarks, sigma_cut, savepath, metapath, outtie


end
