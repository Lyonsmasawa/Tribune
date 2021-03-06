import re
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import datetime as dt
from .models import Article, NewsLetterRecipient
from django.core.exceptions import ObjectDoesNotExist
from .forms import NewsletterForm
from .email import send_welcome_email

# Create your views here.================


def news_today(request):
    date = dt.date.today()
    # day = convert_dates(date)
    news = Article.today_news()

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipient(name = name, email = email)
            recipient.save()
            send_welcome_email(name, email)            

            return redirect(news_today)

    else:
        form = NewsletterForm()

    return render(request, 'all-news/today-news.html', {"date":date, "news":news, "letterform":form,})

def past_days_news(request, past_date):
    
    try:
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        raise Http404()

    if date == dt.date.today():
        return redirect(news_today)
    # day = convert_dates(date)
    news = Article.days_news(date)

    return render(request, 'all-news/past-news.html', {"date":date, "news":news})

def convert_dates(dates):
    day_number = dt.date.weekday(dates)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    day = days[day_number]

    return day
    
def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request, "all-news/article.html", {"article":article})