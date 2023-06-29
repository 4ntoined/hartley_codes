#
import requests

url = 'https://pdssbn.astro.umd.edu/holdings/dif-c-hrii-2-epoxi-hartley2-v1.0/DOWNLOAD/data_2010_'
savehere = '/alcyone1/antojr/downloading_h2/zips/'

numbers = list(range(298,322))
filealls = [ url + f'{i}.tgz' for i in numbers ]
#filealls = [  url+i for i in fileends]
#print(filealls)
print(filealls)

#will download all the zipped raw data and save it at savehere
for i in range(len(filealls)):
    r = requests.get(filealls[i])
    with open(savehere+f'data_2010_{numbers[i]}.tgz','wb') as opp:
        opp.write(r.content)
    print(i)


