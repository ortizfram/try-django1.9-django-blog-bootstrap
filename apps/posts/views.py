# apps/posts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.urls import reverse

from .models import Post
from .forms import PostForm

from django.core.paginator import Paginator

from urllib.parse import quote_plus
from django.db.models import Q

from django.utils import timezone


# Create your views here.

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser: # change in /admin/
        raise Http404
    # make fields requested or POST
    form = PostForm(request.POST or None, request.FILES or None) #from forms.py
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, slug): # retrieve
    #=> drafts can be seen by 'staff or superuser', and annon only if publish < today. else 404
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date(): 
        if not request.user.is_staff or not request.user.is_superuser: # change in /admin/
            raise Http404
    # instance.user = request.user #-> require auth to see
    share_string = quote_plus(instance.content)
    context = {
        "title" : instance.title,
        "instance" : instance,
        "slug": instance.slug,
        'share_string': share_string,
    }
    return render(request, "post_detail.html", context)

def post_list(request): #list items
    #=> staff and superuser can see drafts 
    today = timezone.now().date()
    queryset_list = Post.objects.active() #all() -->not to see 404 on drafts from model  #.filter(draft=False).order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all() 
        
    query = request.GET.get("q") #input name of searchbar
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) 
        ).distinct()
    paginator = Paginator(queryset_list, 6)  # Show 6 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "object_list" : page_obj,
        "title" : "List",
        "today":today,
    }
    return render(request, "post_list.html", context)


def post_update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance ) #from forms.py
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Item Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title" : instance.title,
        "instance": instance,
        "form": form,
        "slug": instance.slug,
    }
    return render(request, "post_form.html", context)

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect(reverse('list'))
