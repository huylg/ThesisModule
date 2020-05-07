from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .python_module.TextAnalysiser import TextAnalysiser

def index(request):
    if request.method == "POST":
        inputText = request.POST.get("input_text","")
        textAnalysiser = TextAnalysiser(inputText)
        aslcIndex = TextAnalysiser.calculateASLC(textAnalysiser.sentenceList,textAnalysiser.charList)
        awlcIndex = TextAnalysiser.calculateAWLC(textAnalysiser.wordList,textAnalysiser.charList)
        pdwIndex = TextAnalysiser.calculatePDW(textAnalysiser.wordList,textAnalysiser.commonWordSet)
        
        LAVFomulaValue = TextAnalysiser.calculateLAVFomula(aslcIndex,awlcIndex,pdwIndex)
        NH1982FomulaValue = TextAnalysiser.calculateNH1982(aslcIndex,awlcIndex)
        NH1985FomulaValue = TextAnalysiser.calculateNH1985(aslcIndex,pdwIndex)

        responeData = {
            'aslw' : TextAnalysiser.calculateASLW(textAnalysiser.sentenceList,textAnalysiser.wordList),
            'asls' : TextAnalysiser.calculateASLS(textAnalysiser.sentenceList,textAnalysiser.syllableList),
            'aslc' : aslcIndex,
            'awlc' : awlcIndex,
            'awls' : TextAnalysiser.calculateAWLS(textAnalysiser.wordList,textAnalysiser.syllableList),
            'pds' : TextAnalysiser.calculatePDS(textAnalysiser.syllableList,textAnalysiser.commonSyllableSet),
            'pdw' : pdwIndex,
            'psvw' : TextAnalysiser.calculatePSVW(textAnalysiser.wordList,textAnalysiser.sinoVietWordSet),
            'PDiaW' :  TextAnalysiser.calculatePDiaW(textAnalysiser.wordList,textAnalysiser.dialectWordSet),
            'LAVFomula' : LAVFomulaValue,
            'NH1982' : NH1982FomulaValue,
            'NH1985': NH1985FomulaValue

        }
        return JsonResponse(responeData)

    else:
        return HttpResponse("get method isn't valid !!!")

    
    

