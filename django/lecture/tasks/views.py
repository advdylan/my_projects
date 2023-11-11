from django.shortcuts import render

# Create your views here.

tasks = ["foo", "bar", "baz"]

def index(request):
    return render(request, "tesks/index.html",{
        "tasks": tasks

    })

