# apps/posts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from .models import Post
from .forms import PostForm

from django.core.paginator import Paginator

from urllib.parse import quote_plus


# Create your views here.

def post_create(request):
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
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    context = {
        "title" : instance.title,
        "instance" : instance,
        "slug": instance.slug,
        'share_string': share_string,
    }
    return render(request, "post_detail.html", context)

def post_list(request): #list items
    queryset_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 6)  # Show 6 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "object_list" : page_obj,
        "title" : "List",
    }
    return render(request, "post_list.html", context)


def post_update(request, slug):
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
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect(reverse('list'))
