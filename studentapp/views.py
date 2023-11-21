from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    blogs = Article.objects.all()

    context = {"blog": blogs}

    return render(request, "home.html", context)


@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        tt = request.POST.get("name")
        cc = request.POST.get("class")
        pr = request.POST.get('division')
        dv = request.POST.get('rollno')
        image = request.FILES.get("cover_image")
        Article.objects.create(
            Name=tt,
            Class=cc,
            Division = pr,
            RollNo = dv,
            cover_image=image, 
            author=request.user
        )
        return redirect("home")
    return render(request, "create.html")


@login_required(login_url="login")
def details(request, id):
    content = Article.objects.get(id=id)
    comments = Comment.objects.filter(article=content)

    context = {"blog": content, "comments": comments}
    return render(request, "details.html", context)


@login_required(login_url="login")
def edit(request, id):
    edits = Article.objects.get(id=id)
    context = {"blog": edits}
    if request.method == "POST":
        if edits.author != request.user:
            return HttpResponse("You are not Authorize to edit this page")
        name = request.POST.get("name")
        clss = request.POST.get("class")
        divi = request.POST.get('division')
        roll = request.POST.get('rollno')

        edits.Name = name
        edits.Class = clss
        edits.Division = divi
        edits.RollNo = roll
        edits.save()

        return redirect("details", id)

    return render(request, "edit.html", context)


@login_required(login_url="login")
def delete(request, id):
    article = Article.objects.get(id=id)
    if article.author != request.user:
        return HttpResponse("You are not Authorize to delete this page")
    if request.method == "POST":
        article.delete()
        return redirect("home")

    context = {"blog": article}

    return render(request, "delete.html", context)


def comment_post(requset, article_id):
    article = Article.objects.get(id=article_id)
    if requset.method == "POST":
        comments = requset.POST.get("comment")
        Comment.objects.create(
            text=comments, comment_author=requset.user, article=article
        )
    return redirect("details", article_id)

def comment_delete(request,id):
    comment = Comment.objects.get(id=id)
    article_id = comment.article.id
    comment.delete()
    return redirect('details',article_id)

 
def comment_edit(request,id):
    comment = Comment.objects.get(id=id)
    blog = comment.article
    if request.method == 'POST':
        text = request.POST.get('comment')
        comment.text = text
        comment.save()
        return redirect('details',blog.id)
    comments = Comment.objects.filter(article = blog)
    context = {
        'blog':blog,
        'comments':comments,
        'cmd':comment,
        'edit':True
    }
    return render(request,'details.html',context)

