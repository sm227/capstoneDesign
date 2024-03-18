from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import logging
import capstoneDesign.script as api
import json
import google.generativeai as genai


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
    text_data = []

    for item in json_data:
        temp = {
            'text': item['text'],
            'start': item['start'],
            # round 는 소수점 반올림 함수
            'minutes': round(item['start'] // 60),  # 분
            'seconds': round(item['start'] % 60)  # 초
        }
        text_data.append(item['text'])
        print(item['text'])
        script_data.append(temp)




    result_list = ['aaa', 'Hello', 123]
    w = open(f'script_{final_link[0]}.txt', 'w' ,encoding='UTF-8')

    for element in text_data:
        # element 가 문자형이 아니면 문자형으로 변환
        if type(element) != 'str':
            element = str(element)
        # 텍스트 입력시 마지막에 줄바꿈 문자도 함께 포함
        w.write(element + '\n')

    # w.close() 를 해줘야 텍스트 파일에 저장됨
    w.close()
    print(script_data)


    # 유해성 조정
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    # 본인 api key 삽입
    genai.configure(api_key="AIzaSyB842rnY66Om_-2SwSnh-R98c7v_OWiB9Q")
    model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)
    with open(f'script_{final_link[0]}.txt', "r", encoding='UTF8') as f:
        example = f.read()

    response = model.generate_content(example)
    print(response.text)
    return render(request, 'index2.html', {'youtube_link': final_link[0], 'data': script_data, 'script' : response.text})


@login_required(login_url='common:login')
def test(request):
    return render(request, 'test.html')
