from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')

def index2(request):
    if request.method == 'POST':
        input_value = request.POST.get('input_value')
        return render(request, 'index2.html', {'input_value': input_value})
    else:
        return redirect('index')
