from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def blog_list(request):
    if request.GET.get("q"):
        posts = Post.objects.filter(
            Q(title__contains=request.GET.get("q"))
            | Q(contents__contains=request.GET.get("q"))
        ).distinct()
    else:
        posts = Post.objects.all()
    context = {"object_list": posts}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {"object": post}
    print(request.user.is_authenticated)
    print(request.user)
    print(post.author)
    return render(request, "blog/blog_detail.html", context)


def blog_create(request):
    if request.method == "GET":
        form = PostForm()
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("blog_list")
        else:
            context = {
                "form": form,
                "error": "입력이 잘못되었습니다. 알맞은 형식으로 다시 입력해주세요!",
            }
            return render(request, "blog/blog_create.html", context)


def blog_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {"form": form, "pk": pk}
        return render(request, "blog/blog_update.html", context)


def blog_delete(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    print(post)
    if request.method == "POST":
        post.delete()
    return redirect("blog_list")


@login_required
def test(request):
    posts = Post.objects.all()
    context = {"object_list": posts}
    return render(request, "blog/blog_list.html", context)
