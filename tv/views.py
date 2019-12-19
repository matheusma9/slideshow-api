from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Create your views here.
def test(request, tv):
    return render(request, 'tv/test.html',  {'tv':mark_safe(json.dumps(tv))})