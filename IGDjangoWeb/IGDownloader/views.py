# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from time import gmtime, strftime
import os.path
import json
import time
import requests
import traceback
import urlparse



def myIndex(request):
    return render(request, 'index.html')

def getInstagramImages(request):
    try:
        if request.method == 'POST':
            inputUrl = request.POST.get('myUrl')
            url = urlparse.urlparse(inputUrl)
            url = url.scheme+"://"+url.netloc+url.path
            url = url + '?__a=1'
            def getImagesUrl():
                response = requests.post(url).content
                if 'edge_sidecar_to_children' in response:
                    print '有多張照片'
                    response = json.loads(response)
                    igImagePics = response['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
                    igImagePicsList = []
                    for i in range(len(igImagePics)):
                        eachImage = igImagePics[i]['node']['display_url']
                        igImagePicsList.append(str(eachImage))
                    return igImagePicsList
                else:
                    print '只有一張照片'
                    response = json.loads(response)
                    igImagePicsList = []
                    igImagePics = response['graphql']['shortcode_media']['display_url']
                    igImagePicsList.append(str(igImagePics))
                    return igImagePicsList
                    #print os.path.isfile('0.jpg')
            imageUrl = getImagesUrl()
            context = {'imageUrl':imageUrl}
            return render(request, 'viewer.html',context)
        else:
            return HttpResponse('404')
    except:
        errorMsg = "Url not found please try again."
        context = {'errorMsg':errorMsg}
        return render(request, 'index.html',context)