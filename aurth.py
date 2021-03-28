# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 07:45:30 2021

@author: dev
"""

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os
from skimage import io
from io import BytesIO
import cv2
import requests
import numpy as np
import pandas as pd
import matplotlib.animation as animation
from IPython.display import HTML
from PIL import Image
import matplotlib.pyplot as plt
import Sentinal_image as SI

def getToken():
    # Your client credentials
    client_id = '5dc5d1a1-db6d-4431-bbf3-c582ec698a5d'
    client_secret = 'g5&:D*PaTuJHTs:%]0%40Ee,MCg.N9[Shcj_~y)W'
    # Create a session
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    # Get token for the session
    token_info = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token',client_id=client_id, client_secret=client_secret)
    TOKEN = token_info['access_token']
    # All requests using this session will have an access token automatically added
    resp = oauth.get("https://services.sentinel-hub.com/oauth/tokeninfo")
    return TOKEN

if __name__=="__main__":
    day = "2019-12-31"
    imagestypes=["TRUE_IMG","CO","NO"]
    #imagestypes=["TRUE_IMG","CO"]
    bbox=[
    140.5755615, 
    35.1693180,
    139.0759277,
    35.7821707,
    ]

    name="Tokyo"

    TOKEN=getToken()
    
    #左回りもしくは右回り時の対応
    for i in range(len(bbox)):
        if bbox[i] >= 0:
            bbox[i] = bbox[i]%360
        else:
            bbox[i] = -(abs(bbox[i])%360) + 360
    
        
    fig,axs=plt.subplots(1,len(imagestypes),figsize=(16,8))
    for ax, imaget in zip(axs,imagestypes):
        if imaget=="TRUE_IMG":
            #img=SI.get_img(bbox,day,imaget,TOKEN )
            img=SI.get_s2_true_img(bbox,day,TOKEN )
        elif imaget=="CO":
             img=SI.get_co_img(bbox, day,TOKEN)
        elif imaget=="NO":
            img=SI.get_NO_img(bbox, day,TOKEN)
       
            
            
       # if imaget=="TRUE_IMG":
        #     img = Image.fromarray(io.imread(BytesIO(response.content)))
        #     img.putalpha(alpha=255)
        #     img=np.array(img)
        
        io.imshow(img,ax=ax)
        io.imsave('{}_{}_{}.png'.format(name,imaget,day),img )
    

    # co_color_resize.pngはSentinel hubから切り出した一酸化炭素のカラースケール画像
    #co_color = io.imread(f'img_other/co_color_resize.png')
  #  co_color = cv2.cvtColor(co_img, cv2.COLOR_RGB2RGBA)
  #  print(co_img.shape)
   # print(co_color.shape)
    
  #  plt.imshow(get_concat_h(co_img, co_color))
#余分のデータをダウンロードする方法がない