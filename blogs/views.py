# blogs/views.py

from django.shortcuts import render, redirect
from .forms import BlogPostForm
from .models import BlogPost
# blogs/views.py

from django.shortcuts import get_object_or_404

def blog_post_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_post_detail.html', {'blog_post': blog_post})


def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user  # Assign the logged-in user as the author
            blog_post.save()
            return redirect('blog_post_list')
    else:
        form = BlogPostForm()
    return render(request, 'create_blog_post.html', {'form': form})

def blog_post_list(request):
    blog_posts = BlogPost.objects.filter(is_draft=False)  # Only show published posts
    return render(request, 'blog_post_list.html', {'blog_posts': blog_posts})

def my_blog_posts(request):
    blog_posts = BlogPost.objects.filter(author=request.user)  # Get posts by the logged-in user
    return render(request, 'my_blog_posts.html', {'blog_posts': blog_posts})
