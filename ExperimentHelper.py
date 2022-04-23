from adblockparser import AdblockRules

def getWebsiteList():
    f = open('travelurls.txt')
    wl = []
    for line in f:
        if line != '\n':
            wl.append(line.strip('\n'))
    f.close()
    return wl

def getAdblockFilter():
    f = open('easylist.txt')
    fl = []
    for line in f:
        fl.append(line.strip('\n'))
    f.close()
    return AdblockRules(fl)

def getUserAgentList():
    f = open('agents.txt')
    ual = []
    for line in f:
        ual.append(line.strip('\n'))
    f.close()
    return ual

def getMimeList():
    return ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp', 'image/tiff', 'image/svg+xml', 'image/avif']
