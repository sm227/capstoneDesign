import os

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

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model, update_session_auth_hash

from django.conf import settings


@csrf_exempt
# @login_required(login_url='common:login')
def index(request):
    logging.basicConfig(level=logging.DEBUG)
    if request.user.is_authenticated:
        recent_data = Video.objects.filter(user=request.user).order_by('-id')[:8]
    # recent_data = Video.objects.order_by('-id')[:3]

        if request.method == 'POST':
            youtube_link = request.POST.get('youtube_link')
            full_link = youtube_link.split('/')
            return render(request, 'index2.html', {'youtube_link': youtube_link, 'full': full_link[2]})


        return render(request, 'index.html', {'data': recent_data})
    return render(request, 'index.html')

video_pk = 0

def video_prompt(real_id, summary_data):
    s = open(f'summary_{real_id}.txt', 'w', encoding='UTF-8')

    for element2 in summary_data:
        if type(element2) != 'str':
            element2 = str(element2)
        s.write(element2 + '\n')

    s.write('\n')
    # w.write('위 내용을 소제목과 내용으로 간단하게 요약해서 마크다운으로 작성해줘')

    s.write("""
        'minutes' 는 분, 'seconds' 는 초.
        들여 쓰기, 단락 구분 보기 좋게 잘 해 주세요.
        다른 내용 마다 단락 구분 해주세요.
        내용을 주제 별로 나눠서 소제목을 적어주세요. 그리고 소제목 옆 괄호에 몇 분 몇 초 사이의 내용 인지를 적어주세요. 시간은 소제목 옆에만 적어주세요.
        내용은 시간 순서대로 작성하세요.
        들여 쓰기하고 내용을 요약해주세요.
        단락 구분을 잘 해주세요. 들여 쓰기를 잘 해주세요.
        중요한 내용은 글씨를 굵게 해주세요.

        짧은 영상(5분 이하)은 영상의 핵심 주제와 가장 중요한 정보를 5문장 이하로 요약해주세요.
        중간 길이 영상(5-20분)은 영상의 주요 포인트를 20문장 이하로 요약하고, 각 포인트별로 핵심적인 세부 사항을 추가해주세요.
        긴 영상(20분 이상)은 영상을 여러 주제으로 나누고 각 주제의 핵심 요약을 제공해주세요. 또한 전체적인 주제와 결론을 포함하는 종합 요약을 추가해주세요.

        각 주제에 어울리는 이모티콘을 하나씩 추가해주세요.ㅑㅜㅇ

        교육적 내용은 영상에서 다루는 주요 교훈이나 학습 포인트를 강조하여 요약해주세요.
        엔터테인먼트 내용은 영상의 주요 이벤트, 등장인물, 그리고 주요 전환점을 요약해주세요. 감정적인 반응이나 흥미로운 순간도 강조해주세요.
        뉴스/시사 내용은 영상에서 다루는 주요 사건, 관련된 인물, 그리고 영향을 요약해주세요. 중요한 날짜나 위치 정보도 포함해주세요.
        인터뷰 형식은 인터뷰에서 논의된 주요 주제들과 각각에 대한 인터뷰이의 주요 의견을 요약해주세요. 중요한 질문과 그에 대한 답변도 강조해주세요.
        튜토리얼/가이드 내용은 영상에서 제공하는 주요 지침이나 단계들을 순서대로 요약해주세요. 중요한 팁이나 주의사항도 포함해주세요.
        리뷰/평가 내용은 제품이나 서비스의 주요 특징, 장단점, 그리고 최종 평가를 요약해주세요. 리뷰어의 개인적인 의견이나 경험도 포함할 수 있습니다.
        """)

    s.close()

@login_required(login_url='common:login')
def index2(request):
    # https://youtu.be/CdJyI0dNN3o?si=bISh9uGFcpiUve_D
    youtube_link = request.GET.get('youtube_link')
    full_link = youtube_link.split('/')
    print(full_link)
    final_link = full_link[3].split('?')
    real_id = final_link[0]
    print(final_link)
    print(final_link)
    api.download_script_json(final_link[0])

    user_id = request.user.id
    # --------
    # API 키와 API 버전 지정
    # 유튜브 api key 로컬 환경 변수에 넣어야 함.
    youtube_api_key = settings.YOUTUBE_API_KEY
    api_service_name = 'youtube'
    api_version = 'v3'

    # YouTube API 클라이언트 생성
    youtube = build(api_service_name, api_version, developerKey=youtube_api_key)

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
    link = Video(user=user, text=video_title, thumbnail=video_thumbnail, video_key=real_id)
    link.save()
    global video_pk
    video_pk = link.id
    print(f"현재 동영상의 id : {video_pk}")
    print(type(video_pk))
    print("ok")

    # link.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())

    with open(f'script_{real_id}.json', 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
    script_data = []
    text_data = []
    summary_data = []

    for item in json_data:
        minutes = item['start'] // 60
        seconds = item['start'] % 60

        temp = {
            'text': item['text'],
            'start': item['start'],
            # round 는 소수점 반올림 함수
            'minutes': round(minutes),  # 분
            'seconds': round(seconds)  # 초
        }
        text_data.append(item['text'])

        summary_data.append({
            'minutes': round(minutes),  # 분
            'seconds': round(seconds),  # 초
            'text': item['text']
        })

        script_data.append(temp)

    result_list = ['aaa', 'Hello', 123]
    w = open(f'script_{real_id}.txt', 'w', encoding='UTF-8')

    for element in text_data:
        # element 가 문자형이 아니면 문자형으로 변환
        if type(element) != 'str':
            element = str(element)
        # 텍스트 입력시 마지막에 줄바꿈 문자도 함께 포함
        w.write(element + '\n')

    # w.close() 를 해줘야 텍스트 파일에 저장됨
    w.write('\n')
    w.close()

    video_prompt(real_id, summary_data)

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

    gemini_key = os.environ.get('gemini_api_key')
    print("your api : ", gemini_key)
    print("ok")

    # 본인 api key 삽입
    genai.configure(api_key=gemini_key)
    # model = genai.GenerativeModel('gemini-pro-1.5-pro-latest', safety_settings=safety_settings)
    model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)
    with open(f'summary_{final_link[0]}.txt', "r", encoding='UTF8') as f:
        example = f.read()

    # txt, json 삭제.
    os.remove(f'script_{final_link[0]}.txt')
    os.remove(f'script_{final_link[0]}.json')

    response = model.generate_content(example)

    a = "<h1>aa</h1>"
    return render(request, 'index2.html',
                  {'youtube_link': final_link[0], 'data': script_data, 'script': response.text, 'script2': a})


@login_required(login_url='common:login')
def history(request, videoo_id):
    # https://youtu.be/CdJyI0dNN3o?si=bISh9uGFcpiUve_D

    temp = Video.objects.get(id=videoo_id)
    real_id = temp.video_key

    api.download_script_json(real_id)

    user_id = request.user.id
    # --------
    # API 키와 API 버전 지정
    youtube_api_key = settings.YOUTUBE_API_KEY
    api_service_name = 'youtube'
    api_version = 'v3'

    # YouTube API 클라이언트 생성
    youtube = build(api_service_name, api_version, developerKey=youtube_api_key);

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

    global video_pk
    video_pk = videoo_id
    print(f"현재 동영상의 id : {video_pk}")
    print(type(video_pk))
    print("ok")

    # link.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())

    with open(f'script_{real_id}.json', 'r', encoding='UTF-8') as f:
        json_data = json.load(f)
    script_data = []
    text_data = []
    summary_data = []

    for item in json_data:
        minutes = item['start'] // 60
        seconds = item['start'] % 60

        temp = {
            'text': item['text'],
            'start': item['start'],
            # round 는 소수점 반올림 함수
            'minutes': round(minutes),  # 분
            'seconds': round(seconds)  # 초
        }
        text_data.append(item['text'])

        summary_data.append({
            'minutes': round(minutes),  # 분
            'seconds': round(seconds),  # 초
            'text': item['text']
        })

        script_data.append(temp)

    result_list = ['aaa', 'Hello', 123]
    w = open(f'script_{real_id}.txt', 'w', encoding='UTF-8')

    for element in text_data:
        # element 가 문자형이 아니면 문자형으로 변환
        if type(element) != 'str':
            element = str(element)
        # 텍스트 입력시 마지막에 줄바꿈 문자도 함께 포함
        w.write(element + '\n')

    # w.close() 를 해줘야 텍스트 파일에 저장됨
    w.write('\n')
    w.close()

    video_prompt(real_id, summary_data)

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

    gemini_key = os.environ.get('gemini_api_key')
    print("your api : ", gemini_key)
    print("ok")

    # 본인 api key 삽입
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)
    with open(f'summary_{real_id}.txt', "r", encoding='UTF8') as f:
        example = f.read()

    response = model.generate_content(example)

    # txt, json 삭제.
    os.remove(f'script_{real_id}.txt')
    os.remove(f'script_{real_id}.json')
    os.remove(f'summary_{real_id}.txt')

    a = "<h1>aa</h1>"
    return render(request, 'index2.html',
                  {'youtube_link': real_id, 'data': script_data, 'script': response.text, 'script2': a})



def delete_history(request, videoo_id):
    global video_pk
    video_pk = videoo_id

    data = Video.objects.get(id=videoo_id)
    data.delete()

    recent_data = Video.objects.filter(user=request.user).order_by('-id')[:8]
    # recent_data = Video.objects.order_by('-id')[:3]

    return redirect('main_page')
    # if request.method == 'POST':
    #     youtube_link = request.POST.get('youtube_link')
    #     full_link = youtube_link.split('/')
    #     return render(request, 'index2.html', {'youtube_link': youtube_link, 'full': full_link[2]})
    #
    # return render(request, 'index.html', {'data': recent_data})


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
        text = request.POST.get('text')

        memo = Memo.objects.create(text=text, user=request.user, video_id=video_pk)

        return render(request, 'memo.html')
    return JsonResponse({'error': 'Bad request,'}, status=400)


# views.py

def delete_memo(request):
    if request.method == 'POST':
        memo_id = request.POST.get('memo_id')
        print("Delete request received for memo ID:", memo_id)  # 로그 추가
        try:
            memo = Memo.objects.get(id=memo_id)
            memo.delete()

            remaining_memos = Memo.objects.filter(user=request.user).values('id', 'text')
            print("Memo successfully deleted.")  # 로그 추가
            return JsonResponse({'message': '메모가 성공적으로 삭제되었습니다.', 'items': list(remaining_memos)})
        except Memo.DoesNotExist:
            print("Memo with ID", memo_id, "does not exist.")  # 로그 추가
            return JsonResponse({'error': '해당 ID의 메모를 찾을 수 없습니다.'}, status=404)
        except Exception as e:
            print("An error occurred while deleting memo:", str(e))  # 로그 추가
            return JsonResponse({'error': str(e)}, status=500)
    else:
        print("POST 요청이 필요합니다.")  # 로그 추가
        return JsonResponse({'error': 'POST 요청이 필요합니다.'}, status=400)


def edit_memo(request):
    if request.method == "POST":
        global video_pk
        memo_id = request.POST.get('memo_id')
        edited_text = request.POST.get('text')

        try:
            memo = Memo.objects.get(id=memo_id, video_id=video_pk)
            memo.text = edited_text
            memo.save()
            data_list = Memo.objects.filter(user=request.user, video_id=video_pk).values('id', 'text').order_by('id')
            return JsonResponse({'items': list(data_list)})
        except Memo.DoesNotExist:
            return JsonResponse({'success': False, 'message': '해당 메모를 찾을 수 없습니다.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})


#memo 보기 탭
def list_memo(request):
    # 예제 데이터 리스트
    # data_list = ['사과', '바나나', '체리']
    global video_pk

    data_list = Memo.objects.filter(user=request.user, video_id=video_pk).values('id', 'text').order_by('id')
    print(data_list)
    print("ok")

    # print(data_list)
    # JsonResponse를 사용하여 데이터를 JSON 형태로 반환
    return JsonResponse({'items': list(data_list)})


# def update_password(request, user_id):
#     User = get_user_model()
#     user = User.objects.get(pk=user_id)
#
#     if request.method == "POST":
#         form = SetPasswordForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, user)
#             return redirect('common:login')
#     else:
#         form = SetPasswordForm(user)
#
#     context = {'form': form}
#     return render(request, 'update_password.html', context)

def update_password(request, user_id):
    User = get_user_model()
    user = User.objects.get(pk=user_id)

    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect('common:login')
    else:
        form = PasswordChangeForm(user)

    context = {'form': form}
    return render(request, 'update_password.html', context)
