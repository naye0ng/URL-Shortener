from django.shortcuts import render, get_object_or_404, redirect
from .models import URL as URL_Model

def index(request) :
    if request.method == 'POST' :
        # TODO : https://, http:// 붙는거 제거해서 저장
        url = request.POST.get("url").strip()
        shortURL = makeShortURL(url) 
        return render(request, 'index.html',{'longURL':url,'shortURL':shortURL})

    return render(request, 'index.html',{'longURL':'Enter the link here','shortURL':''})


def makeShortURL(URL) :
    # 중복 체크
    obj = URL_Model.objects.filter(url = URL).first() or False
    if not obj :
        newURL = URL_Model.objects.create(url = URL)
        shortURL = encoding62(newURL.id)

        newURL.shortURL = shortURL
        newURL.save()
    else :
        shortURL = obj.shortURL 

    return shortURL


# [참고] https://blog.siyeol.com/26
def encoding62(index) :
    words = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
                'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 
                'w', 'x', 'y', 'z']
    result = ""
    # 62 진수 만들기
    while index % 62 > 0 or result == "" :
        result += words[index % 62]
        index = index//62

    return result.zfill(8)

def redirectPath(request, shortURL) :
    # 방문 로그 수집
    url = get_object_or_404(URL_Model, shortURL = shortURL)
    return redirect(to=url.url)
    

