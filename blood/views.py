from django.shortcuts import render
from utils.functions import is_login


@is_login
def analyze(request):
    """血缘分析"""
    return render(request, "blood/analyze.html") 