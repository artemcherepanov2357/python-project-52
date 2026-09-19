from django.shortcuts import render


def index(request):
    raise Exception("Test error for Bugsink")  # временная строка
    return render(request, 'index.html')