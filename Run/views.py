from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.conf import settings
from .serializers import RunSerializer
from .models import Run
import json
import os
import random
import string

def get_meta_data(request, requested_run_key=None):
    try:
        requested_run = Run.objects.filter(key=requested_run_key)
        if requested_run.count() != 1:
            raise Exception
        serializer = RunSerializer(requested_run, many=True)
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

def create_params_file(properties):
    pass
def create_run(request):
    try:
        # create_params_file according to user specifications
        run_property = json.loads(request.body)
        create_params_file(run_property)
        # run FRED Simulation command
        run_command = "perl " + settings.FRED_BASE + "bin/fred_job -p " + "./media/params/params." + run_property['key'] + " -k " + run_property['key']
        print(run_command)
        # read shapefile
        shapefile_command = "perl " + settings.FRED_BASE + "input_files/shapefiles/" + run_property['fips'] + f"/tl_2010_{run_property['fips']}_tract10.shp " + settings.FRED_BASE + "RESULTS/JOB/" + run_property['key'] + " -k " + run_property['key']
        # create movie

        # create run object

        # plotting



        
        # os.system(run_command)

        # for run in graph_property[0]:
        #     command += " -k " + run
        # for var in graph_property[1]:
        #     command += " -v " + var
        # command += " --png 1"
        # pic_name = random_string()
        # command += " -o " + pic_name
        # os.system(command)
        # # os.wait()
        # local_file = open(pic_name+'.png', mode='rb')
        # new_pic = Album(imgpath=File(local_file))
        # new_pic.save()
        # local_file.close()
        # os.system('rm '+pic_name+'.png')
        # os.system('rm plot-'+pic_name+'.png.plt')
        response = HttpResponse()
        response.status_code = 200
        return response
    except Exception as err:
        print(str(err))
        raise Http404(str(err))