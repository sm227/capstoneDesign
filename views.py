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
# 주석 추가
    script_data = []

    for item in json_data:
        temp = {
            'text': item['text'],
            'start': item['start'],
            # round 는 소수점 반올림 함수
            'minutes': round(item['start'] // 60), # 분
            'seconds': round(item['start'] % 60)    # 초
        }

        script_data.append(temp)

    return render(request, 'index2.html', {'youtube_link': final_link[0], 'data': script_data})


@login_required(login_url='common:login')
def test(request):
    return render(request, 'test.html')