from django.shortcuts import render
from django.http import JsonResponse, Http404
from Run.models import Run
from .models import Sweep


def get_run_keys(request):
    try:
        requested_runs = Run.objects.all()
        run_keys = []
        sweep_keys = []
        sweep_idx = []
        for idx, requested_run in enumerate(requested_runs):
            if requested_run.sweep_id is None:
                run_keys.append({"key": requested_run.key})
            elif requested_run.sweep_id in sweep_keys:
                idx_in_run_keys = sweep_idx[sweep_keys.index(requested_run.sweep_id)]
                run_keys[idx_in_run_keys]["children"].append({"key": requested_run.key})
            else:
                sweep_keys.append(requested_run.sweep_id)
                sweep_idx.append(len(run_keys))
                run_keys.append({"key": requested_run.sweep.name, "children": [{"key": requested_run.key}]})
        return JsonResponse(run_keys, safe=False)
    except Exception as e:
        print(str(e))
        raise Http404(str(e))
