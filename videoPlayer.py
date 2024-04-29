#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import blockingQueue #imports the file

def extractFrames(fileName, outputBuffer, maxFramesToLoad=9999):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print(f'Reading frame {count} {success}')
    while success and count < maxFramesToLoad:
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # add the frame to the buffer
        outputBuffer.put(image)
       
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1

    outputBuffer.put("DONE") # let it know that its DONE
    print('Frame extraction complete')


def displayFrames(inputBuffer):
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    frame = inputBuffer.get()
    
    while frame is not None and frame != "DONE":
        # get the next frame
        #frame = inputBuffer.get()

        print(f'Displaying frame {count}')        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

        # get the next frame
        frame = inputBuffer.get()

    print('Finished displaying all frames')
    # cleanup the windows
    cv2.destroyAllWindows()


def convertGrayscale(inputBuffer, outputBuffer):
    # Initialize frame count
    count = 0

    # get frame
    frame = inputBuffer.get()

    while frame is not None and frame != "DONE" and count < 72:

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # generate output file
        outputBuffer.put(grayscaleFrame)

        count += 1

        # generate input for the next frame
        frame = inputBuffer.get()
        
    outputBuffer.put("DONE") # finished
    
# -----------------------------------------------------------------------------

# filename of clip to load
filename = 'clip.mp4'

# extract the frames  
extractionQueue = blockingQueue.blockingQueue(10)

extractionThread = threading.Thread(target = lambda: extractFrames(filename,extractionQueue, 72))

# convert to grayscale
grayscaleQueue = blockingQueue.blockingQueue(10)

grayscaleThread = threading.Thread(target = lambda: convertGrayscale(extractionQueue,grayscaleQueue))

# display the frames
displayThread = threading.Thread(target = lambda: displayFrames(grayscaleQueue))

# start all the threads
extractionThread.start()
grayscaleThread.start()
displayThread.start()

