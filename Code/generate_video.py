# -*- coding: utf-8 -*-
"""
Created on Sat May 15 20:49:25 2021

@author: Sai Mudumba
"""

import cv2
import os
def generate_video():
    image_folder = "C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass\\" # make sure to use your folder
    video_name = 'mygeneratedvideo.avi'
    os.chdir("C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass")
      
    images = [img for img in os.listdir(image_folder) if img.endswith("png")]
     
    # Array images should only consider
    # the image files ignoring others if any
    print(images) 
  
    frame = cv2.imread(os.path.join(image_folder, images[0]))
  
    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape  
  
    video = cv2.VideoWriter(video_name, 0, 15, (width, height)) 
  
    # Appending the images to the video one by one
    for image in images: 
        video.write(cv2.imread(os.path.join(image_folder, image))) 
      
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows() 
    video.release()  # releasing the video generated
  
  
