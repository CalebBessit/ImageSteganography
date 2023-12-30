#Pupose : Extracts the secret message from a stegogram using the original algorithm with 2DLCCM
#Author : Caleb Bessit
#Date   : 29 December 2023

import math
import time
import tdLCCM
import numpy as np
from PIL import Image

def main():
    totals = []
    for index in range(1,6):
        pre= time.time_ns()

        #Load stego image
        print("Loading steganogram...")
        stegoImage      = Image.open("Steganograms/Steg4.2.0{}.tiff".format(index))
        stegoImage      = stegoImage.convert("RGB")
        width, height   = stegoImage.size

        #Load extraction data
        print("Loading extraction data...")
        extData = open("ExtractionData/4.2.0{}.txt".format(index),"r")
        lines   = extData.readlines()

        initKeys    = lines[0][lines[0].rfind(":")+2:]
        statVals    = lines[1][lines[1].rfind(":")+2:]
        messLength  = lines[2][lines[2].rfind(":")+2:]

        x_0, y_0, mu, k  = list( map(float, initKeys.split(",")) )
        PMc,PMs,SDc, SDs = list( map(float, statVals.split(",")) )
        s                = int(messLength)

        #Chaotic sequence re-generation with recalculated keys
        eta = (x_0/y_0) * (mu/k)

        x_0Prime = x_0/(PMc+eta)
        y_0Prime = y_0/(PMs+eta)

        #Ranges on mu and k: [8,15]
        muPrime  = (int( mu + (SDc/eta) ) % 8)+8
        kPrime   = (int( k + (SDs/eta) )  % 8)+8
        
        print("Generating chaotic sequence terms...")
        Am,Bm  = tdLCCM.generateTerms(s,x_0Prime,y_0Prime,muPrime,kPrime)

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

            col     = (  math.floor((P[i]-1)/width  )%height)

            embedPosMatrix.append([layer, row, col])

        #Extract and recombine embedded data
        print("Extracting and recombining data...")
        pixels = stegoImage.load()

        extracted = []
        for i in range(0,2*s,2):
            row, col = embedPosMatrix[i][1], embedPosMatrix[i][2]
            r, g, b = pixels[col, row]

            if embedPosMatrix[i][0]==1:
                valueU = bin(r)[2:].zfill(8)[-4:]
            elif embedPosMatrix[i][0]==2:
                valueU = bin(g)[2:].zfill(8)[-4:]
            else:
                valueU = bin(b)[2:].zfill(8)[-4:]

            row, col = embedPosMatrix[i+1][1], embedPosMatrix[i+1][2]
            r, g, b = pixels[col, row]

            if embedPosMatrix[i+1][0]==1:
                valueL = bin(r)[2:].zfill(8)[-4:]
            elif embedPosMatrix[i+1][0]==2:
                valueL = bin(g)[2:].zfill(8)[-4:]
            else:
                valueL = bin(b)[2:].zfill(8)[-4:]

            value = int("0b" + valueU + valueL,2)
            extracted.append(value)

        dim = int( math.sqrt(s) ) 

        

        #Reshape and save
        print("Reshaping and saving extracted data to file...")
        extracted = np.array(extracted).reshape(dim,dim) 
        extracted = extracted.astype(np.uint8)  
        image = Image.fromarray(extracted, mode='L')
        image.save("ExtractedMessages/4.2.0{}.tiff".format(index)) 

        print(f"Done with image {index}.")
        print()

        '''END PROCESSING'''
        post = time.time_ns()
        totals.append(post-pre)

    print("================================")
    print("Average total extraction time: {} seconds".format(np.average(totals)*math.pow(10,-9)))

if __name__=="__main__":
    main()