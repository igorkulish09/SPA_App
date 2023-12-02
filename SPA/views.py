from django.shortcuts import render, get_object_or_404
from .models import Comment
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def comment_list(request):
    comments = Comment.objects.filter(parent_comment__isnull=True).order_by('-created_at')
    paginator = Paginator(comments, 25)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request, 'SPA/comment_list.html', {'comments': comments})


def add_comment(request, parent_comment_id=None):
    parent_comment = None
    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent_comment = parent_comment
            comment.save()
    else:
        form = CommentForm()

    return render(request, 'SPA/add_comment.html', {'form': form, 'parent_comment': parent_comment})
