from threading import local
from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.conf import settings
from django.core.files import File
from .serializers import AlbumSerializer
from .models import Album
import json
import os
import random
import string

def img_list(request, requested_run=None):
    try:
        imgs = Album.objects.filter(run__key=requested_run)
        if imgs.count() == 0:
            raise Exception
        serializer = AlbumSerializer(imgs, many=True)
        return JsonResponse(serializer.data, safe=False)
    except:
        raise Http404("Run does not exist")

def random_string():
    return ''.join(random.sample(string.ascii_letters + string.digits, 28))

def create_img(request):
    try:
        graph_property = json.loads(request.body)
        command = "perl " + settings.FRED_BASE + "bin/fred_plot"
        for run in graph_property[0]:
            command += " -k " + run
        for var in graph_property[1]:
            command += " -v " + var
        command += " --png 1"
        pic_name = random_string()
        command += " -o " + pic_name
        os.system(command)
        # os.wait()
        local_file = open(pic_name+'.png', mode='rb')
        new_pic = Album(imgpath=File(local_file))
        new_pic.save()
        local_file.close()
        os.system('rm '+pic_name+'.png')
        os.system('rm plot-'+pic_name+'.png.plt')
        response = HttpResponse()
        response.status_code = 200
        return response
    except Exception as err:
        print(str(err))
        raise Http404(str(err))