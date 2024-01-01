#Description : Implementation of image steganography algorithm on greyscale images.
#Author      : Caleb Bessit
#Date        : 01 January 2024

#Decription : Implementation of image steganography algorithm developed by Caleb Bessit
#Author     : Caleb Bessit
#Date       : 27 December 2023

import math
import time
import tdLCCM
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def main():
    # Open the TIFF image and convert to RGB
    totals = []
    for index in range(1,11):
        pre = time.time_ns()
        print("Loading cover image...")
        loadedImage     = Image.open('GreyTestImages/7.1.{}.tiff'.format(str(index).zfill(2)))
        greyImage       = loadedImage.convert("L")
        greyArray       = np.array(greyImage)

        print("Loading secret image...")
        secretImage = Image.open('TestImages/Clock.tiff')
        secretImage = secretImage.convert("L") 
        secretArray = np.array(secretImage)

        #Get image layers and convert to numpy arrays
        width, height   = greyArray.shape
        sWidth, sHeight = secretArray.shape

        print("Generating keys...")
        PMc             = np.average(greyArray)
        PMs             = np.average(secretArray)
        SDc             = np.std(greyArray)
        SDs             = np.std(secretArray)

        #Recalculating new keys for map
        x_0, y_0, mu, k = 0.1, 0.2, 8, 8
        eta = (x_0/y_0) * (mu/k)

        x_0Prime = x_0/(PMc+eta)
        y_0Prime = y_0/(PMs+eta)

        #Ranges on mu and k: [8,15]
        muPrime  = (int( mu + (SDc/eta) ) % 8)+8
        kPrime   = (int( k + (SDs/eta) )  % 8)+8

        #Pre-embedding processes
        s   = sWidth * sHeight
        print("Generating chaotic sequence terms...")
        Am,Bm  = tdLCCM.generateTerms(s,x_0Prime,y_0Prime,muPrime,kPrime)

        print("Combining and sorting results...")
        Xm = np.append(Am,Bm)

        P = np.argsort(Xm)+1

        #Calculate embedding matrix

        #Replace with LC once done
        print("Calculating embedding position matrix...")
        embedPosMatrix = []
        scalingFactor  = (width*height)//(2*s)

        for i in range(2*s):
            # layer   = ((P[i]-1)%3)+1
            # layer   = int(   (3*P[i]-1)/(width*height)   )+1
            row     = ((scalingFactor*P[i]-1)%height)

            col     = (  math.floor((scalingFactor*P[i]-1)/width  )%height)

            embedPosMatrix.append([row, col])
        
        #Create bit-matrix of secret data
        print("Generating secret bit matrix...")
        secretArray = secretArray.reshape(1,sWidth*sHeight)[0]
        

        bitMatrix   = []
        for i in secretArray:
            # bitMat = np.array( list(  map( int, list(bin(i)[2:])) ) )
            string = bin(i)[2:].zfill(8)
            bitMatrix.append(string[:4])
            bitMatrix.append(string[4:])

        
        #Embedding process
        print("Embedding data...")
        for i in range(2*s):
            row, col = embedPosMatrix[i][0], embedPosMatrix[i][1]

            currValue = greyArray[col][row]
            greyArray[col][row] = int( "0b" + bin(currValue)[2:].zfill(8)[:4] + bitMatrix[i] ,2)
            


        print("Saving steganogram...")
        greyImage = Image.fromarray(greyArray.astype(np.uint8), mode='L')
        greyImage.save("GreySteganograms/Steg7.1.{}.tiff".format(str(index).zfill(2)))

        print("Saving extraction data...")
        initKeys    = "Initial keys <x_0, y_0, mu, k>: {},{},{},{}".format(x_0,y_0,mu,k)
        statValues  = "Stat values <PMc,PMs,SDc, SDs>: {},{},{},{}".format(PMc,PMs,SDc,SDs)
        length      = "Message length: {}".format(s)
        
        extDataFile = open("GreyExtractionData/7.1.{}.txt".format(str(index).zfill(2)),"w")
        extDataFile.write(initKeys+"\n"+statValues+"\n"+length)
        extDataFile.close()

        print("Done with {}.".format(index))
        print()
        '''END PROCESSING'''
        post =   time.time_ns()
        totals.append(post-pre)

    print()
    print("Average run time: {} seconds".format(np.average(totals)*math.pow(10,-9)))


if __name__=="__main__":
    main()