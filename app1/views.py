from django.shortcuts import render, redirect
from newsapi import NewsApiClient
import subprocess, psycopg2
import datetime
from app1.models import Posts
from app1.models import Likes
from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def is_logged_in(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

def home(request):
    context = Posts.objects.order_by('-datetime')[:10]
    return render(request, 'home.html', {'articles': context, 'logged_in': is_logged_in(request)})

def sports(request):
    context = Posts.objects.filter(category='sports').order_by('-datetime')[:10]
    return render(request, 'sports.html', {'articles': context, 'logged_in': is_logged_in(request)})

def politics(request):
    context = Posts.objects.filter(category='politics').order_by('-datetime')[:10]
    return render(request, 'politics.html', {'articles': context, 'logged_in': is_logged_in(request)})

def business(request):
    context = Posts.objects.filter(category='business').order_by('-datetime')[:10]
    return render(request, 'business.html', {'articles': context, 'logged_in': is_logged_in(request)})

@login_required(login_url="/accounts/signin")
def profile(request):
    user = User.objects.get(username=request.user.username)
    likes = Likes.objects.filter(user_id=user.id, dislike_id=None)
    dislikes = Likes.objects.filter(user_id=user.id, like_id=None)
    context = Posts.objects.none()
    for l in likes:
        context |= Posts.objects.filter(id=l.like_id)
    for l in dislikes:
        context |= Posts.objects.filter(id=l.dislike_id)
    context = context.order_by('-datetime')[:10]
    return render(request, 'profile.html', {'articles': context, 'logged_in': is_logged_in(request)})

def post_like(request, pk):
    print(request.get_full_path())
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        print(user.id, user.username)
        post = Posts.objects.get(id=pk)
        is_liked = len(Likes.objects.filter(user_id=user.id, like_id=post.id))
        is_disliked = len(Likes.objects.filter(user_id=user.id, dislike_id=post.id))

        print(is_liked, is_disliked)
        if is_liked == 0 and is_disliked == 0:
            post.likes += 1
            post.save()

            a_like = Likes(user_id=user.id,
                like_id=post.id,
                dislike_id=None) # pk? #0 or not include or null?
            a_like.save()
        elif is_liked == 0 and is_disliked != 0:
            post.likes += 1
            post.dislikes -= 1
            post.save()

            un_dislike = Likes.objects.get(user_id=user.id, dislike_id=post.id)
            un_dislike.like_id = post.id
            un_dislike.dislike_id = None
            un_dislike.save()
    #return redirect(source)
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page != None:
        return redirect(previous_page)
    else:
        return redirect('home')
    # if request.is_ajax():
    #     print("hi")
    # post = Posts.objects.get(id=pk)
    #return JsonResponse({'likes':post.likes})
    #return HttpResponseRedirect(reverse('business.html', args=[pk]))

def post_dislike(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        print(user.id, user.username)
        post = Posts.objects.get(id=pk)
        is_liked = len(Likes.objects.filter(user_id=user.id, like_id=post.id))
        is_disliked = len(Likes.objects.filter(user_id=user.id, dislike_id=post.id))

        print(is_liked, is_disliked)
        if is_liked == 0 and is_disliked == 0:
            post.dislikes += 1
            post.save()

            a_dislike = Likes(user_id=user.id,
                like_id=None,
                dislike_id=post.id) # pk? #0 or not include or null?
            a_dislike.save()
        elif is_liked != 0 and is_disliked == 0:
            post.dislikes += 1
            post.likes -= 1
            post.save()

            un_like = Likes.objects.get(user_id=user.id, like_id=post.id)
            un_like.dislike_id = post.id
            un_like.like_id = None
            un_like.save()
    #return redirect(source)
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page != None:
        return redirect(previous_page)
    else:
        return redirect('home')
    #return HttpResponseRedirect(reverse('business.html', args=[pk]))

def user_search(request):
    template = 'home.html'
    query = request.GET.get('q')
    test = request.GET.get('date')
    print(test)
    print(query)
    context = Posts.objects.filter(title__icontains=query) | Posts.objects.filter(description__icontains=query)
    if test == 'likes':
        context = Posts.objects.filter(title__icontains=query) | Posts.objects.filter(description__icontains=query).order_by('-likes')
    elif test == 'date':
        context = Posts.objects.filter(title__icontains=query) | Posts.objects.filter(description__icontains=query).order_by('-datetime')
    if len(context) > 10:
        return render(request, template, {'articles': context[:10], 'logged_in': is_logged_in(request)})
    else:
        return render(request, template, {'articles': context, 'logged_in': is_logged_in(request)})