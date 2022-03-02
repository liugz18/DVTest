from django.shortcuts import render
from django.http import JsonResponse, Http404
from .serializers import RunSerializer
from .models import Run


def get_meta_data(request, requested_run_key=None):
    try:
        requested_run = Run.objects.filter(key=requested_run_key)
        if requested_run.count() != 1:
            raise Exception
        serializer = RunSerializer(requested_run.last(), many=False)
        return JsonResponse(serializer.data, safe=False)
    except:
        raise Http404("Run does not exist!")

def get_run_keys(request):
    try:
        requested_runs = Run.objects.all()
        run_keys = []
        for requested_run in requested_runs:
            run_keys.append({"key": requested_run.key})
        return JsonResponse(run_keys, safe=False)
    except:
        raise Http404("Get run keys error!")
