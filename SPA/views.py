from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
import os


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
            return redirect('comment_list')
    else:
        form = CommentForm()

    return render(request, 'SPA/add_comment.html', {'form': form})
    # return render(request, 'SPA/add_comment.html', {'form': form, 'parent_comment': parent_comment})


from django.http import JsonResponse

def upload_file_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        # Перевірка типу файлу (зображення)
        if not uploaded_file.content_type.startswith('image'):
            return JsonResponse({'error': 'File type not supported'}, status=400)

        # Визначення шляху для збереження файлу
        save_path = 'path/to/save/'

        # Якщо папка не існує, створити її
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Складання шляху для збереження файлу
        file_path = os.path.join(save_path, uploaded_file.name)

        # Отримання розширення файлу
        _, file_extension = os.path.splitext(uploaded_file.name)

        # Збереження файлу
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Якщо це зображення та його розміри перевищують 320x240, зменшіть його
        if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            image = Image.open(file_path)
            max_size = (320, 240)
            image.thumbnail(max_size)
            image.save(file_path)

        # Тут можна повернути URL або іншу інформацію про збережений файл
        file_url = f'/media/{uploaded_file.name}'
        return JsonResponse({'file_url': file_url})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

