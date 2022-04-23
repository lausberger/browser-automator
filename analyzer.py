import io
import os
from google.cloud import vision

DIR = 'data3/'
FOLDERS = ['control', 'geolocation', 'user-agent']
TRIALS = 10
CLIENT = vision.ImageAnnotatorClient()

for e in FOLDERS:
    trialNo = 1
    while trialNo <= TRIALS:
        directory = DIR + e + '/trial' + str(trialNo)
        with open(directory + '/labels.txt', 'a+') as outputFile:
            ssNum = 1
            for x in os.listdir(directory):
                if x[0:11] == 'Screen Shot':
                    outputFile.write('Ad ' + str(ssNum) + ':\n')
                    ssNum += 1
                    imgName = directory + '/' + x  
                    with io.open(imgName, 'rb') as imgFile:
                        imgContent = imgFile.read()
                    visionImage = vision.Image(content=imgContent)
                    labelResponse = CLIENT.label_detection(image=visionImage)
                    textResponse = CLIENT.text_detection(image=visionImage)
                    labels = labelResponse.label_annotations
                    texts = textResponse.text_annotations
                    outputFile.write('\tLabels:\n')
                    for l in labels:
                        outputFile.write('\t\t' + l.description + '\n')
                    outputFile.write('\tText:\n')
                    for t in texts:
                        if '\n' not in t.description:
                            outputFile.write('\t\t' + t.description + '\n')
        trialNo += 1
