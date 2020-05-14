from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .python_module.TextAnalysiser import TextAnalysiser

def index(request):
    if request.method == "POST":
        inputText = request.POST.get("input_text","")
        textAnalysiser = TextAnalysiser()
        responeData = textAnalysiser.analysis(inputText)
        return JsonResponse(responeData)

    else:
        return HttpResponse("get method isn't valid !!!")

    
    

