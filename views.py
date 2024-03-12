from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import logging
import capstoneDesign.script as api

@login_required(login_url='common:login')
def index(request):
    logging.basicConfig(level=logging.DEBUG)

    if request.method == 'POST':
        youtube_link = request.POST.get('youtube_link')
        full_link = youtube_link.split('/')
        # print(full_link)
        # logging.debug(full_link)
        return render(request, 'index2.html', {'youtube_link': youtube_link, 'full':full_link[2]})
        # return print(full_link)

    return render(request, 'index.html')

@login_required(login_url='common:login')
def index2(request):
    youtube_link = request.GET.get('youtube_link')
    full_link = youtube_link.split('/')
    print(full_link)
    final_link = full_link[3].split('?')
    print(final_link)
    api.download_script_json(final_link[0])
    # capstoneDesign.scrpit_api()
    return render(request, 'index2.html', {'youtube_link': full_link[3]})

