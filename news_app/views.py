from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin, HitCountDetailView

from accaunts.models import Profile
from news_project.custom_permissions import OnlyLoggedSuperUser
from .models import Category,News
from .forms import ContctForm, CommentForm
from django.http import HttpResponseBadRequest

# Create your views here.
def news_list(request):
    news_list1=News.published.all()
    # news_list=News.objects.filter(status=News.Status.Published)
    context={
        'news_list1':news_list1
    }
    return render(request,template_name='news/news_list.html',context=context)


# def news_detail(request, news):
#     news=get_object_or_404(News,slug=news,status=News.Status.Published)
#     categories = Category.objects.all()
#     comments=news.comments.filter(active=True)
#     new_comment=None
#     if request.method =='POST':
#         comment_form=CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment=comment_form.save(commit=False)
#             new_comment.news=news
#             new_comment.user=request.user
#             new_comment.save()
#         return redirect('news_detail_page', news=news.slug)
#     else:
#         comment_form=CommentForm()
#     context={
#         'news':news,
#         'categories':categories,
#         'comments':comments,
#         'new_comment':new_comment,
#         'comment_form':comment_form,
#     }
#     return render(request,template_name='news/single_page.html',context=context)



def news_detail(request, news_slug):
    news_article = get_object_or_404(News, slug=news_slug, status=News.Status.Published)
    latest_post = News.published.all().order_by('-publish_time').first()
    categories = Category.objects.all()
    comments = news_article.comments.filter(active=True)
    comment_count=comments.count()
    context={}
    hit_count = get_hitcount_model().objects.get_for_object(news_article)
    hits=hit_count.hits
    hitcontext=context['hitcount']={'pk':hit_count.pk}
    hit_count_response=HitCountMixin.hit_count(request,hit_count)
    if hit_count_response.hit_counted:
        hits=hits + 1
        hitcontext['hit_counted']=hit_count_response.hit_counted
        hitcontext['hit_message']=hit_count_response.hit_message
        hitcontext['total_hits']=hits
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news_article
            new_comment.user = request.user
            new_comment.save()
            return redirect('news_detail_page', news_slug=news_slug)
    else:
        comment_form = CommentForm()
    popular_posts = sorted(News.objects.all(), key=lambda x: x.get_hit_count, reverse=True)[:3]
    context = {
        'news': news_article,
        'categories': categories,
        'comments': comments,
        'comment_count':comment_count,
        'comment_form': comment_form,
        'popular_posts':popular_posts,
        'latest_post':latest_post,
    }

    return render(request, 'news/single_page.html', context=context)


#
# def homePageView(request):
#     news_list=News.published.all().order_by('-publish_time')[:4]
#     categories=Category.objects.all()
#     # local_one=News.published.filter(category__name='Mahalliy').order_by('publish_time')[:1]
#     local_news=News.published.all().filter(category__name='Mahalliy').order_by('publish_time')[:5]
#     sport_news=News.published.all().filter(category__name='Sport').order_by('publish_time')[:5]
#     texnalogiya_news=News.published.all().filter(category__name='Texnalogiya').order_by('publish_time')[:5]
#     xorij_news=News.published.all().filter(category__name='Xorij').order_by('publish_time')[:5]
#
#     contaxt={
#         'news_list':news_list,
#         # 'local_one':local_one,
#         'mahalliy_xabarlar':local_news,
#         'categories':categories,
#         'xorij_xabarlar':xorij_news,
#         'texnalogiya_xabarlar':texnalogiya_news,
#         'sport_xabarlar':sport_news
#     }
#
#     return render(request,template_name='news/index.html',context=contaxt)
# def homePageView(request):
#     news_list = News.published.all().order_by('-publish_time')[:4]
#     categories = Category.objects.all()
#     local_news = News.published.all().filter(category__name='Mahalliy').order_by('publish_time')[:5]
#     sport_news = News.published.all().filter(category__name='Sport').order_by('publish_time')[:5]
#     texnalogiya_news = News.published.all().filter(category__name='Texnalogiya').order_by('publish_time')[:5]
#     xorij_news = News.published.all().filter(category__name='Xorij').order_by('publish_time')[:5]
#
#     # Get popular posts based on hit counts
#     most_viewed_posts = News.objects.all().order_by('-get_hit_count')[3]
#
#     context = {
#         'news_list': news_list,
#         'mahalliy_xabarlar': local_news,
#         'categories': categories,
#         'xorij_xabarlar': xorij_news,
#         'texnalogiya_xabarlar': texnalogiya_news,
#         'sport_xabarlar': sport_news,
#         'popular_posts': most_viewed_posts,  # Add popular posts to context
#     }
#
#     return render(request, template_name='news/index.html', context=context)
# views.py



def homePageView(request):
    news_list = News.published.all().order_by('-publish_time')[:4]
    categories = Category.objects.all()
    local_news = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[:5]
    sport_news = News.published.all().filter(category__name='Sport').order_by('-publish_time')[:5]
    texnalogiya_news = News.published.all().filter(category__name='Texnalogiya').order_by('-publish_time')[:5]
    xorij_news = News.published.all().filter(category__name='Xorij').order_by('-publish_time')[:5]
    latest_post = News.published.all().order_by('-publish_time').first()

    # Get popular posts based on hit counts
    popular_posts = sorted(News.objects.all(), key=lambda x: x.get_hit_count, reverse=True)[:3]

    context = {
        'news_list': news_list,
        'mahalliy_xabarlar': local_news,
        'categories': categories,
        'xorij_xabarlar': xorij_news,
        'texnalogiya_xabarlar': texnalogiya_news,
        'sport_xabarlar': sport_news,
        'popular_posts': popular_posts,  # Add popular posts to context
        'latest_post':latest_post
    }

    return render(request, template_name='news/index.html', context=context)





def contactPageView(request):
    form=ContctForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse('Biz bilan bog\'langaningiz uchun tashakkur!')
    popular_posts = sorted(News.objects.all(), key=lambda x: x.get_hit_count, reverse=True)[:3]
    context={
        'form':form,
        'popular_posts':popular_posts,

    }

    return render(request,'news/contact.html' ,context)

def Error_PageView(request):
    popular_posts = sorted(News.objects.all(), key=lambda x: x.get_hit_count, reverse=True)[:3]
    conttext={
        'popular_posts': popular_posts,
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

class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ('title','body','image','category','status',)
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser,CreateView):
    model = News
    fields = ('title','slug', 'body','image','category','status',)
    template_name = 'crud/news_create.html'

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users=User.objects.filter(is_superuser=True)
    profile_admins=Profile.objects.filter(user__is_superuser=True)
    context={
        'admin_users':admin_users,
        'profile_admins':profile_admins,
    }
    return render(request,template_name='pages/admin_page.html',context=context)




class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            return News.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )
        else:
            # Return an empty queryset or handle the case however you prefer
            return News.objects.none()

    # def dispatch(self, request, *args, **kwargs):
    #     if 'q' not in request.GET:
    #         return HttpResponseBadRequest("Missing 'q' parameter in the request.")
    #     return super().dispatch(request, *args, **kwargs)



# class CategoryNewsView(ListView):
#     model = Category
#     template_name = 'news/category_news.html'
#     context_object_name = 'category_news_list'
#
#     def get_queryset(self):
#         category_slug = self.kwargs['category_slug']
#         category = Category.objects.get(slug=category_slug)
#         return News.objects.filter(category=category).order_by('-publish_time')





