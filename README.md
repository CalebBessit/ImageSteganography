
# Image Steganography

This project involved implementing an image steganography algorithm but with a newly proposed two-dimensional chaotic map, and further work will be done to resolve a critical issue with the algorithm.

For context, steganography is the lesser-known cousin of cryptography, where the main aim is not necessarily to make intercepted data unreadable, but to make it appear as if there is no secret data at all. In particular, image steganography involves concealing confidential data within seemingly ordinary image data. 

One of the main criticisms of the algorithm (and a problem with steganography in general) is the sacrifice of visual quality over issues such as capacity or security. I intend to modify the algorithm to consider cover image contents when embedding data, thereby improving the visual quality while minimizing the compromise of other key factors.

In addition, I will utilize an encryption algorithm from an earlier project to further enhance the algorithm's security.

## Files

The file `imageSteganographer.py` takes in a set of color TIFF format images and produces stego-images using the algorithm. This implementation takes in a set of test images in the `TestImages/` directory and stores the stego-images in the the `Steganograms/` directory. The associated data needed to extract the secret messages is stored in the `ExtractionData/` directory.

The file `secretMessageExtractor.py` takes a stego-image from the `Steganograms/` directory and extracts the secret message. The extracted secret message is stored in the `ExtractedMessages/` directory.

There is an implementation that stores secret messages in greyscale TIFF format images, called `greyImageSteganographer.py`. It similar directories such as `GreyTestImages/`, `GreySteganograms/`, and `GreyExtractionData/`, but there is no secre message extractor for the grey implementation as of yet.