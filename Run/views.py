import this
from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.conf import settings
from matplotlib.pyplot import switch_backend
from sqlalchemy import case
from .serializers import RunSerializer
from .models import Run
from Album.views import create_img_for_run, random_string
import json
import os
import random
import string
import re

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
    # print(properties)
    file_name = "./media/params/params." + properties['key']
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write("enable_visualization_layer = 1\nhousehold_visualization_mode = 1\ncensus_tract_visualization_mode = 1\n")
        file.write(f"days = {properties['days']}\n")
        file.write(f"influenza_transmissibility = {properties['influenza_transmissibility']}\n")
        file.write(f"fips = {properties['fips']}\n")
        file.write(f"office_size = {properties['office_size']}\n")
        file.write(f"enable_travel = {int(properties['enable_travel'])}\n")
        file.write(f"min_travel_distance = {properties['min_travel_distance']}\n")
        file.write(f"school_closure_policy = {properties['school_closure_policy']}\n")
        file.write(f"school_closure_duration = {properties['school_closure_duration']}\n")
        file.write(f"school_summer_schedule = {int(properties['school_summer_schedule'])}\n")
        file.write(f"sick_day_prob = {properties['sick_day_prob']}\n")

        file.write(f"school_classroom_size = {properties['school_classroom_size']}\n")
        file.write(f"influenza_probability_of_symptoms = {properties['influenza_probability_of_symptoms']}\n")
        file.write(f"community_distance = {properties['community_distance']}\n")
        file.write(f"community_prob = {properties['community_prob']}\n")
        file.write(f"home_neighborhood_prob = {properties['home_neighborhood_prob']}\n")
        file.write(f"influenza_asymp_infectivity = {properties['influenza_asymp_infectivity']}\n")
        file.write(f"influenza_incubation_period_median = {properties['influenza_incubation_period_median']}\n")
        file.write(f"influenza_incubation_period_dispersion = {properties['influenza_incubation_period_dispersion']}\n")
        file.write(f"influenza_symptoms_duration_median = {properties['influenza_symptoms_duration_median']}\n")
        file.write(f"influenza_symptoms_duration_dispersion = {properties['influenza_symptoms_duration_dispersion']}\n")
        file.write(f"enable_face_mask_usage = {int(properties['enable_face_mask_usage'])}\n")
        file.write(f"face_mask_compliance = {properties['face_mask_compliance']}\n")
        file.write(f"influenza_face_mask_transmission_efficacy = {properties['influenza_face_mask_transmission_efficacy']}\n")
        file.write(f"influenza_face_mask_susceptibility_efficacy = {properties['influenza_face_mask_susceptibility_efficacy']}\n")
        file.write(f"enable_hand_washing = {int(properties['enable_hand_washing'])}\n")
        file.write(f"hand_washing_compliance = {properties['hand_washing_compliance']}\n")
        file.write(f"influenza_hand_washing_transmission_efficacy = {properties['influenza_hand_washing_transmission_efficacy']}\n")
        file.write(f"influenza_hand_washing_susceptibility_efficacy = {properties['influenza_hand_washing_susceptibility_efficacy']}\n")
        file.write(f"influenza_face_mask_plus_hand_washing_transmission_efficacy = {properties['influenza_face_mask_plus_hand_washing_transmission_efficacy']}\n")



def get_next_id():
    id_file_name = settings.FRED_BASE + "RESULTS/ID"
    with open(id_file_name, 'r', encoding='utf-8') as file:
        ret = file.readline()
        ret = ret[0:-1]
        ret += '/'
    return ret

def fips_to_map_pos(fips):
    mapping = {
        '42003': " -x -80.5 -X -79.5 -y 40.3 -Y 40.6 ",
        '42063': "-x -79.2 -X -79 -y 40.3 -Y 41"
    }
    return " -x -80.5 -X -79.5 -y 40.3 -Y 40.6 " #mapping[fips]

def create_movie(properties):
    movie_command = "perl " + settings.FRED_BASE + "bin/fred_make_movie" + " -k " + properties['key'] +  " --google 0 --census_tracts 1" + fips_to_map_pos(properties['fips'])
    os.system(movie_command)
    os.system(f"mv {properties['key']}.mp4 ./media/")
    # print(movie_command)

def get_config(request, requested_run_key):
    try:
        requested_run = Run.objects.filter(key=requested_run_key)
        if requested_run.count() != 1:
            raise Exception
        file_name = "./media/params/params." + requested_run_key
        configs = {}
        with open(file_name, 'r', encoding='utf-8') as file:
            line = file.readline()
            while line:
                key, value = re.split("[ = ]+", line)
                configs[key] = value
                line = file.readline()
        return JsonResponse(configs, safe=False)
    except:
        raise Http404("Run does not exist!")
        

def create_run_object(properties, this_id):
    prefix = settings.FRED_BASE + "RESULTS/JOB/" + this_id + "META/"
    with open(prefix + 'START', 'r', encoding='utf-8') as file:
        startdate = file.readline()
    with open(prefix + 'FINISHED', 'r', encoding='utf-8') as file:
        finishdate = file.readline()
    with open(prefix + 'POPSIZE', 'r', encoding='utf-8') as file:
        popsize = int(file.readline())
    with open(prefix + 'DENSITY', 'r', encoding='utf-8') as file:
        density = float(file.readline())
    with open(prefix + 'USER', 'r', encoding='utf-8') as file:
        user = file.readline()
    with open(prefix + 'WHERE', 'r', encoding='utf-8') as file:
        where = file.readline()
    log_name = random_string() + ".txt"
    os.system("cp " + settings.FRED_BASE + "RESULTS/JOB/" + this_id + "DATA/OUT/out1.txt ./media/" + log_name)

    new_run = Run(
        fips = properties['fips'],
        key = properties['key'],
        configpath = "./media/params/params." + properties['key'],
        videopath = properties['key'] + ".mp4",
        logpath = log_name,
        startdate = startdate,
        finishdate = finishdate,
        popsize = popsize,
        density = density,
        user = user,
        where = where
    )
    new_run.save()
    # plotting
    create_img_for_run(properties['key'], new_run)

def create_run(request):
    try:
        # create_params_file according to user specifications
        run_property = json.loads(request.body)
        create_params_file(run_property)
        # run FRED Simulation command
        file_name = "./media/params/params." + run_property['key']
        run_command = "perl " + settings.FRED_BASE + "bin/fred_job -p " + file_name + " -k " + run_property['key']
        this_id = get_next_id()
        # print(run_command)
        os.system(run_command)
        # read shapefile
        shape_file_src = settings.FRED_BASE + "input_files/shapefiles/" + run_property['fips'] + f"/tl_2010_{run_property['fips']}_tract10.shp "
        shape_file_dest =  settings.FRED_BASE + "RESULTS/JOB/" + this_id + "DATA/OUT/VIS/run1/dis0/MAPS/SHAPES/"
        shapefile_command = "perl " + settings.FRED_BASE + "bin/fred_read_shapefile " + shape_file_src + shape_file_dest
        os.system(shapefile_command)
        # print(shapefile_command)
        # create movie
        create_movie(run_property)
        # create run object
        create_run_object(run_property, this_id)
        


        

        response = HttpResponse()
        response.status_code = 200
        return response
    except Exception as err:
        print(str(err))
        raise Http404(str(err))