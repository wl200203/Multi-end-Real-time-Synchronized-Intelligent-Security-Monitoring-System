from django.urls import path, include
from . import views
from rest_framework import routers

router=routers.DefaultRouter()
router.register('Post', views.BlogImages)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('js_test/', views.js_test, name='js_test'),
    path('api_root/', include(router.urls)),
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls')),
    path('api/posts/', views.post_list_api, name='post_list_api'),  # 2-3 功能：返回所有博客
    path('api/posts_paginated/', views.post_list_paginated_api, name='post_list_paginated_api'),  # 2-4 功能：分页和过滤
    path('api/images/', views.list_images, name='list_images'),
    path('api/images_paginated/', views.list_images_paginated, name='list_images_paginated'),
    path('api/images_paginated/', views.paginated_image_list, name='paginated_image_list'),
]



# urlpatterns = [
#     # API endpoints
#     path('api/posts/', views.paginated_image_list, name='paginated_image_list'),
#     path('api/posts/simple/', views.post_list_api, name='post_list_api'),
#     path('api/posts/paginated/', views.post_list_paginated_api, name='post_list_paginated_api'),
# ]
