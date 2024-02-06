from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from .models import Assessment_Base,NewUser

# 自定义用户管理界面
class NewUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email','first_name','last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions','roles',)}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )

    list_display = ('id','username', 'roles', 'email', 'is_active','last_login')
    list_display_links = ('id','username','roles','email','last_login')
    search_fields = ('username', 'email')

# 自定义评估基类管理界面
class AssessmentBaseAdmin(admin.ModelAdmin):
    # 设置整数型字段的输入框大小
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size':'20'})},
    }
    # 设置显示字段
    list_display = ('id','record_date','crew_group','name','train_model','assessment_item','assessment_result','file_name')
    list_display_links = ('id','record_date','crew_group','name','train_model','assessment_item','assessment_result')
    search_fields = ('record_date','crew_group','name','train_model','assessment_item','assessment_result','file_name')

admin.site.register(NewUser,NewUserAdmin)
admin.site.register(Assessment_Base, AssessmentBaseAdmin)