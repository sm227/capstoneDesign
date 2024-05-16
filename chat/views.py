# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html')

# room.html을 보여주는 함수 추가
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})