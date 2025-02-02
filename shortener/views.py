from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import URL as URL_Model
import requests
from bs4 import BeautifulSoup

def index(request) :
    if request.method == 'POST' and request.POST.get("url"):
        url = request.POST.get("url").replace("https://","").replace("http://","").strip()
        shortURL = makeShortURL(url) 
        return JsonResponse({'shortURL' : shortURL}, json_dumps_params = {'ensure_ascii': True})
    
    return render(request, 'main.html',{'longURL':'Enter the link here'})


def makeShortURL(URL) :
    # 중복 체크
    obj = URL_Model.objects.filter(url = URL).first() or False

    if not obj :
        newURL = URL_Model.objects.create(url = URL)
        shortURL = encoding62(newURL.id)

        # 크롤링해서 페이지 정보 가져오기
        req = requests.get('http://'+URL)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select('title')[0].text or ''

        newURL.title  = title 
        newURL.shortURL = shortURL
        newURL.save()
    else :
        shortURL = obj.shortURL 
    return shortURL


# [참고] https://blog.siyeol.com/26
def encoding62(index) :
    words = ['r', 'u', 'j', 'l', '5', 'W', 'e', 'O', 'C', 'R', '0', 
                'A', 'w', 'H', 'S', 't', 'D', '3', 'n', 'G', '7', 'm', 
                '6', 'E', 'P', 'J', 'o', 'K', 'Z', 'I', 'z', 'x', 'b', 
                '2', '8', 'T', 'd', 's', 'Q', 'f', 'p', 'k', 'B', 'y', 
                'v', 'X', '1', 'Y', 'c', '9', 'M', 'V', '4', 'N', 'U', 
                'L', 'i', 'h', 'a', 'F', 'q', 'g']
                
    result = ""
    # 62 진수 만들기
    while index % 62 > 0 or result == "" :
        result += words[index % 62]
        index = index//62
    # result.zfill(8)
    return result

def redirectPath(request, shortURL) :
    url = get_object_or_404(URL_Model, shortURL = shortURL)
    # 방문 로그 수집
    url.visited += 1
    url.save()
    return redirect(to='http://'+url.url)

def copy(requests,shortURL) :
    url = get_object_or_404(URL_Model, shortURL = shortURL)
    # 복사 횟수 추가
    url.copied += 1
    url.save()
    return JsonResponse({'shortURL' : shortURL}, json_dumps_params = {'ensure_ascii': True})

def rank(request) :
    visited_rank = URL_Model.objects.all().order_by('-visited')[:5]
    copied_rank = URL_Model.objects.all().order_by('-copied')[:5]

    return render(request, 'rank.html',{'visited_rank':visited_rank,'copied_rank':copied_rank})
    
