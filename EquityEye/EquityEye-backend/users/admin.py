from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import AdminSite

User = get_user_model()

# 自定义管理站点
class CustomAdminSite(AdminSite):
    site_header = 'User Management'  # 更改标题
    site_title = 'User Management'   # 更改浏览器标签标题
    index_title = 'User Management'  # 更改首页标题
    
    def get_app_list(self, request):
        """只显示用户管理相关的应用"""
        app_list = super().get_app_list(request)
        # 只保留 users 应用
        return [app for app in app_list if app['app_label'] == 'users']

# 创建自定义管理站点实例
admin_site = CustomAdminSite(name='custom_admin')

# 移除装饰器，只使用 register 方法
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'date_of_birth', 'occupation', 'annual_income', 'risk_level', 'created_at', 'is_staff')
    search_fields = ('email',)
    
    # 简化编辑表单
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'occupation', 'annual_income')}),
        ('Investment Profile', {'fields': ('risk_level', 'loss_tolerance', 'market_reaction', 'preferred_assets', 'investment_experience')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    
    # 简化添加用户表单
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    filter_horizontal = ()
    filter_vertical = ()

    def get_queryset(self, request):
        """默认显示用户列表"""
        return super().get_queryset(request)

    def has_module_permission(self, request):
        """始终显示用户模块"""
        return True

# 只使用一次注册
admin_site.register(User, CustomUserAdmin) 