from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from rest_framework import viewsets
from .serializers import PostSerializer
from django.http import HttpResponse
from django.http import JsonResponse  
from django.core.paginator import Paginator 
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer




def post_list_api(request):
    posts = Post.objects.all().values()  # 获取所有博客数据
    return JsonResponse(list(posts), safe=False)


def list_images(request):
    posts = Post.objects.all().values()  # 查询所有 Post 数据
    return JsonResponse(list(posts), safe=False)


def post_list_paginated_api(request):
    user_id = request.GET.get('user_id')  # 获取用户 ID 参数
    page = request.GET.get('page', 1)  # 获取页码，默认显示第 1 页

    # 过滤数据
    if user_id:
        posts = Post.objects.filter(author__id=user_id)  # 根据用户 ID 过滤
    else:
        posts = Post.objects.all()  # 获取所有博客

    # 分页处理
    paginator = Paginator(posts, 5)  # 每页显示 5 条数据
    page_obj = paginator.get_page(page)

    # 转换为字典格式并返回 JSON 数据
    data = list(page_obj.object_list.values())
    response = {
        "page": page_obj.number,  # 当前页码
        "total_pages": paginator.num_pages,  # 总页数
        "data": data  # 当前页的数据
    }
    return JsonResponse(response, safe=False)





def list_images_paginated(request):
    user_id = request.GET.get('user_id')  # 获取用户 ID 参数
    page = request.GET.get('page', 1)     # 获取页码，默认为 1

    # 过滤数据
    if user_id:
        blogs = ImageBlog.objects.filter(user_id=user_id)
    else:
        blogs = ImageBlog.objects.all()

    # 分页处理
    paginator = Paginator(blogs, 5)  # 每页显示 5 条数据
    page_obj = paginator.get_page(page)

    # 返回分页数据
    data = list(page_obj.object_list.values())  # 转换为字典列表
    response = {
        "page": page_obj.number,  # 当前页码
        "total_pages": paginator.num_pages,  # 总页数
        "data": data  # 当前页的数据
    }
    return JsonResponse(response, safe=False)



class CustomPagination(PageNumberPagination):
    page_size = 5  # 每页显示 5 条数据
    page_size_query_param = 'page_size'
    max_page_size = 10

@api_view(['GET'])
def paginated_image_list(request):
    """
    返回分页和过滤后的图像博客列表
    GET 参数：
    - user_id: 按用户过滤
    - page: 页码
    """
    user_id = request.GET.get('user_id')
    posts = Post.objects.all()
    
    # 过滤用户
    if user_id:
        posts = posts.filter(author__id=user_id)

    # 分页
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)





def js_test(request):
    return HttpResponse("This is a test view for js_test.")




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


class BlogImages(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer