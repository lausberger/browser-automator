from seleniumwire import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
EXPERIMENT_TYPES = ['control', 'user-agent', 'geolocation']
DIR_NAME = 'data3/'
MIN_SIZE = 10240
NUM_TRIALS = 10
MEASUREMENT_SITE = 'https://www.speedtest.net'

# generates a driver configuration based on the type of experiment
# control and User-Agent treatment use a clean Chromium binary
def getOptions(expType):
    options = Options()

    if expType == 'control' or expType == 'user-agent':
        options.binary_location = "/Users/lucas/privacy-activism/privacy-browser/chromium/src/out/Default/Chromium.app/Contents/MacOS/Chromium"
    elif expType == 'geolocation':
        options.binary_location = "/Users/lucas/privacy-activism/privacy-browser/chromium/src/out/Sel99/Chromium.app/Contents/MacOS/Chromium"

    #options.disable_encoding = True 
    '''
    # These are disabled because they trigger bot detection on test set websites
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')         
    options.add_argument("window-size=1920,1080")
    '''
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
    imgNum = 1
    folderName = expType + '/trial' + str(trialNo) + '/'
    staticPath = DIR_NAME + folderName + 'img' + str(imgNum)
    imgPath = staticPath

    print(expType + ' trial ' + str(trialNo))

    try: 
        print('making directory ' + DIR_NAME + folderName)
        os.makedirs(DIR_NAME + folderName)
    except:
        # do nothing if directories already exist
        # it's only a problem if the images already exist
        print('directory ' + DIR_NAME + folderName + ' already exists')

    for request in driverRequests:
        if request.response:
            if ADBLOCK_FILTER.should_block(request.url):
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
                            elif matchedType == 'image/avif':
                                imgPath += '.avif'

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
    try:
        os.makedirs(DIR_NAME + expType)
        print('making directory ' + DIR_NAME + expType)
    except:
        print('directory ' + DIR_NAME + expType + ' already exists')
    trialNo = 1
    while trialNo <= numTrials:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(120)
        if expType == 'user-agent':
            driver.request_interceptor = userAgentModifier
        for website in siteList:
            print(website)
            driver.get(website)
            time.sleep(5)
        if expType == 'user-agent':
            del driver.request_interceptor
        #del driver.requests
        driver.set_window_size(1440, 1440)
        driver.get(MEASUREMENT_SITE)
        time.sleep(60)
        '''
        # These will not work without Chromium operating in 'headless' mode
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
        '''
        # this is not consistent enough to warrant its use
        #parseRequestsAndSaveAds(expType, driver.requests, trialNo)
        driver.find_element(by=By.TAG_NAME, value='body').screenshot(DIR_NAME + expType + '/trial' + str(trialNo) + '.png')
        driver.close()
        trialNo += 1

# runs all experiments and generates measurement data for each type
# experiments include one control and two differing treatments
def main():
    for experimentType in EXPERIMENT_TYPES:
        options = getOptions(experimentType)
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        permsDriver = webdriver.Chrome(options=options)
        permsDriver.get('https://www.google.com')
        input('Ensure permissions for ' + experimentType + ' binary are correct, then press any key to continue')
        permsDriver.close()
        print('Beginning experiment type: ' + experimentType)
        runExperiment(WEBSITE_LIST, NUM_TRIALS, experimentType)
        input('Experiment ' + experimentType + ' has concluded successfully. Press any key to continue')

if __name__ == "__main__":
    main()
