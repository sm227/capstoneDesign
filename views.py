from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        youtube_link = request.POST.get('youtube_link')
        return render(request, 'index2.html', {'youtube_link': youtube_link})
    return render(request, 'index.html')

def index2(request):
    youtube_link = request.GET.get('youtube_link')
    return render(request, 'index2.html', {'youtube_link': youtube_link})