from adblockparser import AdblockRules

def getWebsiteList():
    return ['https://www.google.com', 'https://www.youtube.com', 'https://cornhub.website']

def getAdblockFilter():
    f = open('easylist.txt')
    fl = []
    for line in f:
        fl.append(line.strip('\n'))
    return AdblockRules(fl)

def getUserAgentList():
    f = open('agents.txt')
    ual = []
    for line in f:
        ual.append(line.strip('\n'))
    return ual

def getMimeList():
    return ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp', 'image/tiff', 'image/svg+xml']
