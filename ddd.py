#
import requests

class downloader:
    def __init__(self,url,nlow,nhigh):
        self.url = url
        self.nums = tuple(range(nlow,nhigh))
        return
    def gen_urls(self):
        #nums = tuple(range(low,high))
        self.fils = [ self.url + f'{i}.tgz' for i in self.nums ]
        self.nfils = len(self.fils)
        return self.fils
    def download(self,savepath):
        #nlist = len(filelist)
        #ii = 0
        prog = 1.
        for i in range(self.nfils):
            r = requests.get(self.fils[i])
            with open(savepath+f'data_2010_{self.nums[i]}.tgz','wb') as opp:  opp.write(r.content)
            pert = i/self.nfils
            if pert >= prog *0.1:
                print(f'{pert*100.:.2f}%')
                prog+=1
        return
    def blank(self):
        return

if __name__ == '__main__':
    url = 'https://pdssbn.astro.umd.edu/holdings/' +\
        'dif-c-hrii-2-epoxi-hartley2-v1.0/DOWNLOAD/' +\
        'data_2010_'
    savehere = '/alcyone1/antojr/downloading_h2/wild'
    doy_range = (298, 322)
    d1 = downloader(url,doy_range[0],doy_range[1])
    d1.gen_urls()
    d1.download(savehere)
else:
    pass
#numbers = list(range(298,322))
#filealls = [ url + f'{i}.tgz' for i in numbers ]
#filealls = [  url+i for i in fileends]
#print(filealls)
#filealls, numbers = gen_urls(298,322)
#print(filealls)

#will download all the zipped raw data and save it at savehere

#for i in range(len(filealls)):
#    r = requests.get(filealls[i])
#    print(i)



