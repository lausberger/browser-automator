from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.options import Options
from seleniumwire.utils import decode
from adblockparser import AdblockRules
from PIL import Image
import random
import os
import time
import ExperimentHelper

USER_AGENTS = ExperimentHelper.getUserAgentList()
WEBSITE_LIST = ExperimentHelper.getWebsiteList()
ADBLOCK_FILTER = ExperimentHelper.getAdblockFilter()
VALID_MIMES = ExperimentHelper.getMimeList()
EXPERIMENT_TYPES = ['tr-ua', 'control', 'tr-geo']
DIR_NAME = 'data/'
MIN_SIZE = 20480
NUM_TRIALS = 5

# generates a driver configuration based on the type of experiment
# control and User-Agent treatment use a clean Chromium binary
def getOptions(expType):
    options = Options()
    options.binary_location = "/Users/lucas/privacy-activism/privacy-browser/chromium/src/out/Sel99/Chromium.app/Contents/MacOS/Chromium"

    '''
    if expType == 'control' or expType == 'tr-ua':
        options.binary_location = "/Users/lucas/privacy-activism/privacy-browser/chromium/src/out/Default/Chromium.app/Contents/MacOS/Chromium"
    elif expType == 'tr-geo':
        options.binary_location = "/Users/lucas/privacy-activism/privacy-browser/chromium/src/out/Sel99/Chromium.app/Contents/MacOS/Chromium"
    '''

    options.enable_har = True
    options.disable_encoding = False 
    return options

# generates a proxy configuration for a driver 
def getProxyOptions():
    proxyOptions = {
        'exclude_hosts': WEBSITE_LIST
    }
    return proxyOptions

# intercepts a request packet and randomly assigns it a User-Agent header
def userAgentModifier(request):
    del request.headers['User-Agent']
    request.headers['User-Agent'] = random.choice(USER_AGENTS)

# performs a measurement of ads received on the most recent website
# ad images that trigger the adblock filter are saved to that trial's folder
def parseRequestsAndSaveAds(expType, driverRequests, trialNo):
    imgNum = 0
    folderName = expType + '/trial' + str(trialNo) + '/'
    #imgName = DIR_NAME + folderName + '/img' + str(imgNum)
    staticPath = DIR_NAME + folderName + '/img' + str(imgNum)
    imgPath = staticPath

    os.makedirs(DIR_NAME + folderName)

    for request in driverRequests:
        if request.response:
            if ADBLOCK_FILTER.should_block(request.url):
                print(request.url)
                mimeType = request.response.headers['Content-Type']
                if mimeType:
                    if 'image' in mimeType:
                        with open(imgPath, 'wb') as imgFile:
                            imgFile.write(request.response.body)
                        imgFile.close()
                        
                        matchedType = None
                        for mime in VALID_MIMES:
                            if mime in mimeType:
                                matchedType = mime

                        if matchedType:
                            if matchedType == 'image/jpeg':
                                imgPath += '.jpg'
                            elif matchedType == 'image/png':
                                imgPath += '.png'
                            elif matchedType == 'image/gif':
                                imgPath += '.gif'
                            elif matchedType == 'image/bmp':
                                imgPath += '.bmp'
                            elif matchedType == 'image/webp':
                                imgPath += '.webp'
                            elif matchedType == 'image/tiff':
                                imgPath += '.tiff'
                            elif matchedType == 'image/svg+xml':
                                imgPath += '.svg'

                            os.rename(staticPath, imgPath)

                            try:
                                tmpFile = Image.open(imgPath, 'r')
                                if tmpFile.height * tmpFile.width < MIN_SIZE:
                                    os.remove(imgPath)
                                else:
                                    imgNum += 1
                                tmpFile.close()
                            except:
                                if matchedType != 'image/svg+xml':
                                    os.remove(imgPath)
                        else:
                            print("Unhandled MIME type: " + mimeType)
                            print(request.url)

                        imgPath = staticPath

# automates a crawl through the website lists then performs a measurement
# the configuration of the browser used depends on the experiment type
def runExperiment(siteList, numTrials, expType):
    options = getOptions(expType)
    proxyOptions = getProxyOptions()
    for trialNo in range(numTrials):
        driver = webdriver.Chrome(seleniumwire_options=proxyOptions, options=options)
        if expType == 'tr-ua':
            driver.request_interceptor = userAgentModifier
        for website in siteList:
            driver.get(website)
            #time.sleep(10)
        driver.request_interceptor = None
        driver.get('https://www.coolmathgames.com/')
        time.sleep(10)
        parseRequestsAndSaveAds(expType, driver.requests, trialNo)
        driver.close()

# runs all experiments and generates measurement data for each type
# experiments include one control and two differing treatments
def main():
    for experimentType in EXPERIMENT_TYPES:
        runExperiment(WEBSITE_LIST, NUM_TRIALS, experimentType)

if __name__ == "__main__":
    main()

