from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from .forms import PostForm, CommentForm
from .models import Post, Comment

# Display name mapping
DISPLAY_NAMES = {
    'iverson09': 'Iverson',
    'iverson10': 'Vanessa',
}

@login_required
def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    comment_form = CommentForm()

    # Build display names for each post's likes
    post_likes_map = {
        post.id: [DISPLAY_NAMES.get(user.username, user.username) for user in post.likes.all()]
        for post in posts
    }

    if request.method == 'POST' and 'post_id' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=request.POST.get('post_id'))
            comment.name = DISPLAY_NAMES.get(request.user.username, request.user.username)

            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id).first()
                if parent_comment:
                    comment.parent = parent_comment

            comment.save()
            return redirect('home')

    return render(request, 'posts/home.html', {
        'posts': posts,
        'comment_form': comment_form,
        'current_user': request.user,
        'user_display_name': DISPLAY_NAMES.get(request.user.username, request.user.username),
        'post_likes_map': post_likes_map,
        'display_names': DISPLAY_NAMES,  # ✅ Needed for template tag filter
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'posts/delete_post.html', {'post': post})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.name != DISPLAY_NAMES.get(request.user.username, request.user.username):
        return HttpResponseForbidden("You can only edit your own comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)

    return render(request, 'posts/edit_comment.html', {'form': form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.name != DISPLAY_NAMES.get(request.user.username, request.user.username):
        return HttpResponseForbidden("You can only delete your own comment.")

    if request.method == 'POST':
        comment.delete()
        return redirect('home')

    return render(request, 'posts/delete_comment.html', {'comment': comment})


# ❤️ Toggle Like (Heart React)
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes(),
        'likers': [DISPLAY_NAMES.get(user.username, user.username) for user in post.likes.all()],
    })
