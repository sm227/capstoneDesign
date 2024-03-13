from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import logging
import capstoneDesign.script as api
import json


@login_required(login_url='common:login')
def index(request):
    logging.basicConfig(level=logging.DEBUG)

    if request.method == 'POST':
        youtube_link = request.POST.get('youtube_link')
        full_link = youtube_link.split('/')
        return render(request, 'index2.html', {'youtube_link': youtube_link, 'full': full_link[2]})

    return render(request, 'index.html')


@login_required(login_url='common:login')
def index2(request):
    youtube_link = request.GET.get('youtube_link')
    full_link = youtube_link.split('/')
    print(full_link)
    final_link = full_link[3].split('?')
    print(final_link)
    api.download_script_json(final_link[0])

    with open(f'script_{final_link[0]}.json', 'r', encoding='UTF-8') as f:
        json_data = json.load(f)

    script_data = []

    for item in json_data:
        temp = {
            'text': item['text'],
            'start': item['start']
        }
        script_data.append(temp)

    return render(request, 'index2.html', {'youtube_link': full_link[3], 'data': script_data})