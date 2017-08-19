# -*- coding: utf-8 -*-
import os.path
from time import gmtime, strftime
from Tkinter import *
import subprocess
import json
import time
import requests
import traceback
import urlparse


def getInstagramImages():
    localTime = strftime("%Y%m%d%H%M%S", gmtime())
    localTime = str(localTime)
    save_path = os.path.dirname(os.path.abspath(__file__))
    save_path = save_path+'/IGPhotos'
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    #inputUrl = 'https://www.instagram.com/p/BTbuOP7FLV9'
    #inputUrl = 'https://www.instagram.com/p/BTO4Xd8la2q'
    #inputUrl = 'https://www.instagram.com/p/BTuNY3iFNCF'
    #inputUrl = raw_input(">>> 請輸入網址: ")
    domain = domainPath.get()
    inputUrl = domainPath.get()
    url = urlparse.urlparse(inputUrl)
    url = url.scheme+"://"+url.netloc+url.path
    url = url + '?__a=1'
    response = requests.post(url).content
    if 'edge_sidecar_to_children' in response:
        print '此網址為多張照片or影片'
        response = json.loads(response)
        igImagePics = response['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
        for i in range(len(igImagePics)):
            if 'video_url' not in str(response):
                print '照片'
                eachFile = igImagePics[i]['node']['display_url']
                fileType = eachFile[-3:]
            else:
                print '影片'
                eachFile = igImagePics[i]['node']['video_url']
                fileType = eachFile[-3:]
            completeName = os.path.join(save_path,'%s%s.%s' % (localTime,i,fileType))
            f = open(completeName,'wb')
            f.write(requests.get(str(eachFile)).content)
            f.close()      
    else:
        print '此網址為一張照片or影片'
        if 'video_url' not in response:
            print '照片'
            response = json.loads(response)
            igImagePics = response['graphql']['shortcode_media']['display_url']
            fileType = igImagePics[-3:]
        else:
            print '影片'
            response = json.loads(response)
            igImagePics = response['graphql']['shortcode_media']['video_url']
            fileType = igImagePics[-3:]
        completeName = os.path.join(save_path, '%s.%s' % (localTime,fileType))
        f = open(completeName,'wb')
        f.write(requests.get(str(igImagePics)).content)
        f.close()
    print '>>> 照片儲存位置:',save_path

#getInstagramImages()
root = Tk() # create a Tk root window
domainPath = StringVar()  
text = Label(text = '請輸入Instagram照片網址 >>> ex: https://www.instagram.com/p/BTWIV-Al2Uw');
text.pack();
Entry(root,textvariable=domainPath,width=50).pack()

b1 = Button(root,text="IG Photos I'm coming!",command=getInstagramImages)
root.geometry('500x100')
root.title('Instagram Photos Crawler')
b1.pack(side=BOTTOM,padx=10)
root.mainloop() # starts the mainloop



