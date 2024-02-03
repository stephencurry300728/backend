"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, re_path

# rest_framework 板块
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from upload.views import (
    Assessment09A02ViewSet,
    Assessment09A0304ViewSet,
    Assessment10A01ViewSet,
    Assessment10A02ViewSet,
    AssessmentBaseViewSet,
)

from upload.views import UserInfoViewSet,LogoutView,AssessmentUploadView

router = DefaultRouter()
'''
There are two mandatory arguments to the register() method:
1. prefix - The URL prefix to use for this set of routes.
2. viewset - The viewset class.
3. basename - The base to use for the URL names that are created.
'''
# 主路由
'''
basename='assessment09a02'告诉Django REST Framework（DRF）为Assessment09A02ViewSet生成的所有URL添加前缀assessment-09a02
当序列化 reverse('assessment09a02-detail', ...)时，Django知道这应该匹配到Assessment09A02ViewSet的详情 -detail 视图的URL 
'''
router.register(r'assessment-base', AssessmentBaseViewSet, basename='assessmentbase')
router.register(r'assessment-09a02', Assessment09A02ViewSet, basename='assessment09a02')
router.register(r'assessment-09a0304', Assessment09A0304ViewSet, basename='assessment09a0304')
router.register(r'assessment-10a01', Assessment10A01ViewSet, basename='assessment10a01')
router.register(r'assessment-10a02', Assessment10A02ViewSet, basename='assessment10a02')

# 前端路由守卫定义必须有登录的用户才能放行
router.register(prefix="info", viewset=UserInfoViewSet)

urlpatterns = [
    # 定义admin路径，连接到Django的管理后台
    path("admin/", admin.site.urls),
    # 定义api路径，包含由DRF router自动生成的URLs
    path("api/", include(router.urls)),
    # 接口文档
    path("docs/", include_docs_urls(title="API文档")),
    # 访问根目录重定向到api文档页面
    re_path(r'^$', lambda request: redirect('docs/', permanent=True)),
    # 定义用于获取 JWT 认证 token ("access")
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 定义用于刷新 JWT 认证 token ("refresh")
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 用户登出清除token
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    # 上传文件并写入数据库
    path("api/upload-assessment/", AssessmentUploadView.as_view(), name='upload-assessment'),
]
