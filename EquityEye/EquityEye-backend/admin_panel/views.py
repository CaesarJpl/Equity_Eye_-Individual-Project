from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
from django.db.models import Q

class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        """获取用户列表，支持搜索"""
        try:
            search = request.GET.get('search', '')
            
            # 构建查询
            users = User.objects.filter(
                Q(email__icontains=search) |
                Q(occupation__icontains=search)
            ).values(
                'id', 
                'email', 
                'date_of_birth',
                'occupation',
                'annual_income',
                'risk_level',
                'created_at'
            ).order_by('-created_at')

            return Response({
                'success': True,
                'data': list(users)
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 