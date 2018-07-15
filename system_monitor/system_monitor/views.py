from django.shortcuts import render, redirect


def welcome(request):
    if request.user.is_authenticated:
        return redirect('app_details')
    else:
        return render(request, 'index.html')