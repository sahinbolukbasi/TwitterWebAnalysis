from django.shortcuts import render, redirect,get_object_or_404
import requests
from .models import *
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from firstApp.forms import EmpForm,AnlysForm
import tweepy 
import pandas as pd
import csv
@login_required(login_url='/login/')
def IndexView(request):
    template_name='index.html'
    return render(request,template_name)

@login_required(login_url='/login/')
def HesapView(request):
    template_name='hesap.html'
    return render(request,template_name)

@login_required(login_url='/login/')
def ContactView(request):
    template_name='contact.html'
    contact = Contact.objects.filter(alıcı=request.user)
    cntfrm = EmpForm(request.POST or None)  
    if cntfrm.is_valid():
        message = cntfrm.save(commit=False)
        message.user = request.user
        message.save()
        return redirect('contact')
    return render(request,template_name,{'contact':contact,'form':cntfrm})


def ClearContact(requst,id):
    secilen=get_object_or_404(Contact,id=id)
    secilen.delete()
    return redirect('contact')

def TweetGetir(request):
    consumer_key =''
    consumer_secret =''
    access_token =''
    access_token_secret =''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api=tweepy.API(auth)
    gelenVeri=request.GET.get('gelenVeri',default = 'None')
    if gelenVeri is not None and gelenVeri != '':
            tweets = api.search(q = gelenVeri,lang = "tr", count=10)
            data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['text'])
            for i in range(len(data)):
                tweet=Tweets()
                tweet.tweet=data.loc[i]['text']
                tweet.user=request.user
                tweet.hastag=gelenVeri
                tweet.userName=""
                tweet.userAvatar=""
                tweet.save()
            return redirect('tweets')
    else:
        return redirect('tweets')


def FilterTweet(request,hastag):
    template_name='tweets.html'
    tweet_all= Tweets.objects.values('hastag').filter(user=request.user).annotate(total=Count('hastag'))
    tweet = Tweets.objects.filter(hastag=hastag)
    return render(request,template_name,{'tweet':tweet,'tweet_all':tweet_all})



@login_required(login_url='/login/')
def TweetView(request):
    template_name='tweets.html'
    tweet_all= Tweets.objects.values('hastag').filter(user=request.user).annotate(total=Count('hastag'))
    tweet = Tweets.objects.filter(user=request.user) 
    contex={
        'tweet':tweet,'tweet_all':tweet_all
    } 
    return render(request,template_name,contex)


@login_required(login_url='/login/')
def AnalizIstekView(request):
    template_name='analizistek.html'
    anlzfrm = AnlysForm(request.POST or None)  
    if anlzfrm.is_valid():
        message = anlzfrm.save(commit=False)
        message.Auser = request.user
        message.Aalıci_id = 1
        message.save()
        return redirect('analizistek')
    return render(request,template_name,{'form':anlzfrm})

@login_required(login_url='/login/')
def AnalizView(request):  
    if not request.user.is_authenticated:
       return redirect('index')
    post = Post.objects.filter(user=request.user )
    dosya=request.GET.get('durum',default = 'None')
    print(dosya)
    if dosya == 'None':
        dosya=str(329)
    kf= pd.read_csv('media/'+dosya+'.csv', encoding='utf_8')  
    ld = pd.read_csv('media/'+dosya+'_LD.csv', encoding='utf_8')
    tk= pd.read_csv('media/'+dosya+'_TK.csv', encoding='utf_8')
    gd= pd.read_csv('media/'+dosya+'_GD.csv', encoding='utf_8')
    contex={
        'post':post,
        'kelimefrekans': kf.to_dict('records'),      
        'gundagilimi': gd.to_dict('records'),
        'tweetkaynak': tk.to_dict('records'),
        'lokasyondagilimi': ld.to_dict('records'),
    }
    return render(request,'analiz.html',contex)
    



