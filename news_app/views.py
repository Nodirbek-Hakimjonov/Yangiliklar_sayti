from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Category,News
from .forms import ContctForm
# Create your views here.
def news_list(request):
    news_list1=News.published.all()
    # news_list=News.objects.filter(status=News.Status.Published)
    context={
        'news_list1':news_list1
    }
    return render(request,template_name='news/news_list.html',context=context)
def news_detail(request, news):
    news=get_object_or_404(News,slug=news,status=News.Status.Published)
    categories = Category.objects.all()
    context={
        'news':news,
        'categories':categories,
    }
    return render(request,template_name='news/single_page.html',context=context)



def homePageView(request):
    news_list=News.published.all().order_by('-publish_time')[:5]
    categories=Category.objects.all()
    # local_one=News.published.filter(category__name='Mahalliy').order_by('publish_time')[:1]
    local_news=News.published.all().filter(category__name='Mahalliy').order_by('publish_time')[:5]
    sport_news=News.published.all().filter(category__name='Sport').order_by('publish_time')[:5]
    texnalogiya_news=News.published.all().filter(category__name='Texnalogiya').order_by('publish_time')[:5]
    xorij_news=News.published.all().filter(category__name='Xorij').order_by('publish_time')[:5]

    contaxt={
        'news_list':news_list,
        # 'local_one':local_one,
        'mahalliy_xabarlar':local_news,
        'categories':categories,
        'xorij_xabarlar':xorij_news,
        'texnalogiya_xabarlar':texnalogiya_news,
        'sport_xabarlar':sport_news
    }

    return render(request,template_name='news/index.html',context=contaxt)


def contactPageView(request):
    form=ContctForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse('Biz bilan bog\'langaningiz uchun tashakkur!')
    context={
        'form':form

    }
    return render(request,'news/contact.html' ,context)

def Error_PageView(request):
    conttext={

    }
    return render(request,template_name='news/404.html',context=conttext)

class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklari'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Mahalliy')
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklari'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Xorij')
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnalogiya.html'
    context_object_name = 'texnalogiya_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnalogiya')
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news

