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
    for index in range(1,6):
        pre = time.time_ns()
        print("Loading cover image...")
        loadedImage = Image.open('TestImages/4.2.0{}.tiff'.format(index))
        rgbImage    = loadedImage.convert("RGB")

        print("Loading secret image...")
        secretImage = Image.open('TestImages/Clock.tiff')
        secretImage = secretImage.convert("L") 
        secretArray = np.array(secretImage)

        #Get image layers and convert to numpy arrays
        r, g, b         = rgbImage.split()
        r, g, b         = map(np.array, (r,g,b))
        width, height   = rgbImage.size
        sWidth, sHeight = secretArray.shape

        print("Generating keys...")
        fullImageArray  = np.append([],(r.reshape(1,width*height)[0],g.reshape(1,width*height)[0],b.reshape(1,width*height)[0]))
        PMc             = np.average(fullImageArray)
        PMs             = np.average(secretArray)
        SDc             = np.std(fullImageArray)
        SDs             = np.std(secretArray)

        #Recalculating new keys for map
        x_0, y_0, mu, k = 0.1, 0.2, 8, 8
        eta = (x_0/y_0) * (mu/k)

        x_0 = x_0/(PMc+eta)
        y_0 = y_0/(PMs+eta)

        #Ranges on mu and k: [8,15]
        mu  = (int( mu + (SDc/eta) ) % 8)+8
        k   = (int( k + (SDs/eta) )  % 8)+8

        #Pre-embedding processes
        s   = sWidth * sHeight
        print("Generating chaotic sequence terms...")
        Am,Bm  = tdLCCM.generateTerms(s,x_0,y_0,mu,k)

        print("Combining and sorting results...")
        Xm = np.append(Am,Bm)

        P = np.argsort(Xm)+1

        #Calculate embedding matrix

        #Replace with LC once done
        print("Calculating embedding position matrix...")
        embedPosMatrix = []

        for i in range(2*s):
            # layer   = ((P[i]-1)%3)+1
            layer   = int(   (3*P[i]-1)/(width*height)   )+1
            row     = ((P[i]-1)%height)

            col     = (  math.floor((P[i]-1)/height  )%width)

            embedPosMatrix.append([layer, row, col])
        
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
        pixels = rgbImage.load()
        for i in range(2*s):
            row, col = embedPosMatrix[i][1], embedPosMatrix[i][2]
            r, g, b = pixels[col, row]
            if embedPosMatrix[i][0]==1:
                pixels[col, row] = (int( "0b" + bin(r)[2:].zfill(8)[:4] + bitMatrix[i] ,2), g, b)
            elif embedPosMatrix[i][0]==2:
                pixels[col, row] = (r, int( "0b" + bin(g)[2:].zfill(8)[:4] + bitMatrix[i] ,2), b)
            else:
                pixels[col, row] = (r, g, int( "0b" + bin(b)[2:].zfill(8)[:4] + bitMatrix[i] ,2) )


        print("Saving steganogram...")
        rgbImage.save("Steganograms/Steg4.2.0{}.tiff".format(index))
        print("Done with {}.".format(index))
        print()
        '''END PROCESSING'''
        post =   time.time_ns()
        totals.append(post-pre)

    print()
    print("Average run time: {} seconds".format(np.average(totals)*math.pow(10,-9)))


if __name__=="__main__":
    main()