# stockChart/urls.py
from django.urls import path
from .views import stocksjson, company_news, InvestmentAdviceView

urlpatterns = [
    path("stocksjson", stocksjson, name="stocksjson"),
    path("company-news", company_news, name="company-news"),
    path('investment-advice/', InvestmentAdviceView.as_view(), name='investment-advice'),
    # 注意：没有斜杠
]