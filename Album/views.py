from django.shortcuts import render
from django.http import JsonResponse, Http404
from .serializers import AlbumSerializer
from .models import Album


def img_list(request, requested_run=None):
    try:
        imgs = Album.objects.filter(run__key=requested_run)
        if imgs.count() == 0:
            raise Exception
        serializer = AlbumSerializer(imgs, many=True)
        return JsonResponse(serializer.data, safe=False)
    except:
        raise Http404("Run does not exist")