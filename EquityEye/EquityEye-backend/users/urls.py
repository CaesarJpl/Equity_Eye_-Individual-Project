from django.urls import path
from .views import RegisterView, LoginView, PersonalInfoView, KYCView, FavoriteStockView, ForgotPasswordView, ResetPasswordView, InvestmentView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view() ),
    path('login/', LoginView.as_view(), name='login'),
    path('personal-info/<int:user_id>/', PersonalInfoView.as_view(), name='personal-info'),
    path('kyc/<int:user_id>/', KYCView.as_view(), name='kyc'),
    path('users/favorites/', FavoriteStockView.as_view(), name='favorites'),
    path('users/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('users/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('users/investments/', InvestmentView.as_view(), name='investments'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
] 