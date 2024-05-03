from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import logging
import capstoneDesign.script as api
import json
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt

from common.models import Memo, Video
from django.contrib.auth.models import User as authUser

from googleapiclient.discovery import build



# from capstoneDesign.models import Memo


@csrf_exempt
@login_required(login_url='common:login')
def index(request):


    logging.basicConfig(level=logging.DEBUG)

    recent_data = Video.objects.filter(user=request.user).order_by('-id')[:8]
    # recent_data = Video.objects.order_by('-id')[:3]

    if request.method == 'POST':
        youtube_link = request.POST.get('youtube_link')
        full_link = youtube_link.split('/')
        return render(request, 'index2.html', {'youtube_link': youtube_link, 'full': full_link[2]})

    return render(request, 'index.html' , {'data': recent_data})

video_pk = 0

@login_required(login_url='common:login')
def index2(request, user_id):
    # https://youtu.be/CdJyI0dNN3o?si=bISh9uGFcpiUve_D
    youtube_link = request.GET.get('youtube_link')
    full_link = youtube_link.split('/')
    print(full_link)
    final_link = full_link[3].split('?')
    real_id = final_link[0]
    # print(youtube_id[1])
    # print(youtube_id[1])
    print(final_link)
    print(final_link)
    api.download_script_json(final_link[0])

    # --------
    # API 키와 API 버전 지정
    api_key = 'AIzaSyB1ZzrTmFpdSNc2gHmF9n9S11A4vgHrKbc'
    api_service_name = 'youtube'
    api_version = 'v3'

    # YouTube API 클라이언트 생성
    youtube = build(api_service_name, api_version, developerKey=api_key)

    # 동영상 ID 지정
    video_id = real_id

    # videos.list API를 호출하여 동영상 정보 가져오기
    requestt = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    responsee = requestt.execute()
    print(responsee)

    # # 동영상 제목 추출
    video_title = responsee['items'][0]['snippet']['title']
    video_thumbnail = responsee['items'][0]['snippet']['thumbnails']['high']['url']
    print("동영상 제목:", video_title)

    # --------------

    user = get_object_or_404(authUser, id=user_id)
    link = Video(user=user, text=video_title, thumbnail=video_thumbnail)
    link.save()
    global video_pk
    video_pk = link.id
    print(f"현재 동영상의 id : {video_pk}")
    print(type(video_pk))
    print("ok")

    # link.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())

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
        # print(item['text'])
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
    w.write('\n')
    w.write('위 내용을 소제목과 내용으로 간단하게 요약해서 마크다운으로 작성해줘')

    w.close()
    # print(script_data)


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
    #response = model.generate_content("보기 좋게 요약해줘.", example)

    # print(response.text)
    a = "<h1>aa</h1>"
    return render(request, 'index2.html', {'youtube_link': final_link[0], 'data': script_data, 'script' : response.text, 'script2': a})


@login_required(login_url='common:login')
def test(request):
    return render(request, 'test.html')

def sign_up(request):
    return render(request, 'common/signup.html')

def sign_up_complete(request):
    return redirect('common:login')

def add_memo(request):
    if request.method == 'POST':
        global video_pk
        text = request.POST.get('text') # aaaaa
        # user = get_object_or_404(authUser, id=user_id)
        memo = Memo.objects.create(text=text, user=request.user, video_id=video_pk)

        # return HttpResponse("<script>console.log(dd);</script>")
        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        # memoList = Memo.objects.all().values('text')
        return render(request, 'memo.html')
    return JsonResponse({'error': 'Bad request,'}, status=400)

# views.py

# def my_ajax_view(request):
#     # 예제 데이터 리스트
#     # data_list = ['사과', '바나나', '체리']
#     global video_pk
#     data_list = Memo.objects.filter(user=request.user, video_id=video_pk).values('text')
#     print(data_list)
#     print("ok")
#
#     # print(data_list)
#     # JsonResponse를 사용하여 데이터를 JSON 형태로 반환
#     return JsonResponse({'items': list(data_list)})

def my_ajax_view(request):
    global video_pk
    # 사용자와 비디오 ID에 해당하는 메모들을 필터링
    memos = Memo.objects.filter(user=request.user, video_id=video_pk).values('id', 'text')
    print(memos)
    print("ok")

    # JsonResponse를 사용하여 데이터를 JSON 형태로 반환
    return JsonResponse({'items': list(memos)})
