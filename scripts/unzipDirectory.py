import zipfile,fnmatch,os

root = '/home/keith/nba/neilmj_BasketballData/BasketballData/2016.NBA.Raw.SportVU.Game.Logs'
pattern = '*.7z'
i = 0
for dirName, subdirList, files in os.walk(root):
    for filename in fnmatch.filter(files, pattern):
        i+=1
        if i>=5:
            break
        else:
            #/nba/testData/jsonVU$
            fullFile=os.path.join(root, filename)
            #print (os.path.splitext(filename))#[0]
            zipfile.ZipFile(fullFile).extract('/home/keith/nba/testData/jsonVU')
