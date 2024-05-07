from django.shortcuts import render

from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from common.forms import UserForm, UserForm2

from django.http import JsonResponse, HttpResponse
from .models import Memo
from django.views.decorators.csrf import csrf_exempt

def logout_view(request):
    logout(request)
    return redirect('common:login')


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('common:login')
    else:
        form = UserForm()
    return render(request, 'common/login.html', {'form': form})


def signup2(request):
    return render(request, 'common/login.html')

# def add_memo(request):
#     if request.method == 'POST':
#         text = request.POST.get('text') # aaaaa
#         memo = Memo.objects.create(text=text)
#         # return HttpResponse("<script>console.log(dd);</script>")
#         return redirect("common:memo")
#     return JsonResponse({'error': 'Bad request,'}, status=400)



def update(request):
    if request.method == "POST":
        form = UserForm2(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('common:login')
    else:
        form = UserForm2(instance=request.user)
    return render(request, 'common/update.html', {'form': form})

# def update_password(request):
#     if request.method == "POST":
#         form = PasswordChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             return redirect('common:login')
#     else:
#         form = PasswordChangeForm(instance=request.user)
#     return render(request, 'common/update_password.html', {'form': form})