from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.settings import EMAIL_HOST_USER
from .serializers import UserRegisterSerializer, PersonalInfoSerializer, KYCSerializer, FavoriteStockSerializer, InvestmentSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import FavoriteStock, Investment
import re
from django.core.mail import send_mail
import random
import string
from django.core.cache import cache
from decimal import Decimal
import logging

User = get_user_model()

logger = logging.getLogger('api')

class RegisterView(APIView):
    def post(self, request):
   
        logger.info(f"Register Request - Email: {request.data.get('email')}")
        
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        

        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            logger.warning(f"Register Failed - Invalid email format: {email}")
            return Response({
                'success': False,
                'field': 'email',
                'message': 'Invalid email format'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not (len(password) >= 7 and 
                any(c.isdigit() for c in password) and
                any(c.isupper() for c in password) and
                any(c.islower() for c in password)):
            logger.warning(f"Register Failed - Invalid password format for email: {email}")
            return Response({
                'success': False,
                'field': 'password',
                'message': 'Password does not meet requirements'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.save()
                logger.info(f"Register Success - User: {email}")
                return Response({'success': True}, status=status.HTTP_201_CREATED)
            
            logger.warning(f"Register Failed - Invalid data for email: {email}, errors: {serializer.errors}")
            return Response({
                'success': False,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Register Error - Email: {email}, Error: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PersonalInfoView(APIView):
    def put(self, request, user_id):
        logger.info(f"Update Personal Info Request - User ID: {user_id}, Data: {request.data}")
        try:
            user = User.objects.get(id=user_id)
            serializer = PersonalInfoSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Update Personal Info Success - User ID: {user_id}")
                return Response({'success': True})
            
            logger.warning(f"Update Personal Info Failed - User ID: {user_id}, errors: {serializer.errors}")
            return Response({
                'success': False,
                'message': 'Invalid data'
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error(f"Update Personal Info Failed - User ID {user_id} not found")
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

class KYCView(APIView):
    def put(self, request, user_id):
        logger.info(f"Update KYC Request - User ID: {user_id}, Data: {request.data}")
        try:
            user = User.objects.get(id=user_id)
            serializer = KYCSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Update KYC Success - User ID: {user_id}")
                return Response({'success': True})
            
            logger.warning(f"Update KYC Failed - User ID: {user_id}, errors: {serializer.errors}")
            return Response({
                'success': False,
                'message': 'Invalid data'
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error(f"Update KYC Failed - User ID {user_id} not found")
            return Response({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    def post(self, request):
    
        logger.info(f"Login Request - Email: {request.data.get('email')}")
        
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            logger.warning(f"Login Failed - Missing credentials for email: {email}")
            return Response({
                'success': False,
                'field': 'email' if not email else 'password',
                'message': 'Please provide both email and password.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if not user:
            logger.warning(f"Login Failed - Invalid credentials for email: {email}")
            return Response({
                'success': False,
                'field': 'password',
                'message': 'Invalid email or password.'
            }, status=status.HTTP_401_UNAUTHORIZED)

  
        logger.info(f"Login Success - User: {email}")
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'is_staff': user.is_staff
            }
        })

class FavoriteStockView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Add Favorite Stock Request - User: {request.user.email}, Data: {request.data}")
        
        """add stock"""
        symbol = request.data.get('symbol')
        name = request.data.get('name')
        
        if not symbol or not name:
            return Response({
                'success': False,
                'message': 'Symbol and name are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
        
            favorite, created = FavoriteStock.objects.get_or_create(
                user=request.user,
                symbol=symbol,
                defaults={'name': name}
            )
            
            if not created:
                return Response({
                    'success': False,
                    'message': 'Stock already in favorites'
                }, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Add Favorite Stock Success - User: {request.user.email}, Symbol: {symbol}")
            return Response({
                'success': True,
                'message': 'Stock added to favorites'
            })

        except Exception as e:
            logger.error(f"Add Favorite Stock Error - User: {request.user.email}, Error: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Gets a list of stock favorites from the user"""
        favorites = FavoriteStock.objects.filter(user=request.user)
        serializer = FavoriteStockSerializer(favorites, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def delete(self, request):
        """Stock cancellation"""
        symbol = request.query_params.get('symbol')
        if not symbol:
            return Response({
                'success': False,
                'message': 'Symbol is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite = FavoriteStock.objects.get(user=request.user, symbol=symbol)
            favorite.delete()
            return Response({
                'success': True,
                'message': 'Stock removed from favorites'
            })
        except FavoriteStock.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Stock not found in favorites'
            }, status=status.HTTP_404_NOT_FOUND)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        logger.info(f"Forgot Password Request - Email: {email}")
        
        try:
            user = User.objects.get(email=email)
            code = ''.join(random.choices(string.digits, k=6))
            cache.set(f'reset_password_{email}', code, 600)
            
        
            send_mail(
                'Reset Your Password',
                f'Your verification code is: {code}',
                EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            logger.info(f"Forgot Password - Verification code sent to: {email}")
            return Response({
                'success': True,
                'message': 'Verification code has been sent to your email'
            })
        except User.DoesNotExist:
            logger.warning(f"Forgot Password Failed - No user found with email: {email}")
            return Response({
                'success': False,
                'message': 'No user found with this email'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Forgot Password Error - Email: {email}, Error: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        logger.info(f"Reset Password Request - Email: {email}")
        
        cached_code = cache.get(f'reset_password_{email}')
        if not cached_code or cached_code != code:
            logger.warning(f"Reset Password Failed - Invalid code for email: {email}")
            return Response({
                'success': False,
                'message': 'Invalid or expired verification code'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            user.set_password(request.data.get('new_password'))
            user.save()
            
            cache.delete(f'reset_password_{email}')
            logger.info(f"Reset Password Success - User: {email}")
            
            return Response({
                'success': True,
                'message': 'Password has been reset successfully'
            })
        except User.DoesNotExist:
            logger.error(f"Reset Password Failed - No user found with email: {email}")
            return Response({
                'success': False,
                'message': 'No user found with this email'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Reset Password Error - Email: {email}, Error: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InvestmentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"Get Investments Request - User: {request.user.email}")
        try:
            investments = Investment.objects.filter(user=request.user)
            
       
            merged_investments = {}
            for inv in investments:
                if inv.symbol in merged_investments:
             
                    merged_investments[inv.symbol]['quantity'] = merged_investments[inv.symbol]['quantity'] + inv.quantity
                    merged_investments[inv.symbol]['total'] = merged_investments[inv.symbol]['total'] + inv.total
              
                    if merged_investments[inv.symbol]['quantity'] != 0:
                        merged_investments[inv.symbol]['price'] = round(
                            merged_investments[inv.symbol]['total'] / merged_investments[inv.symbol]['quantity'],
                            2
                        )
          
                    if inv.created_at > merged_investments[inv.symbol]['created_at']:
                        merged_investments[inv.symbol]['created_at'] = inv.created_at
                else:
            
                    merged_investments[inv.symbol] = {
                        'symbol': inv.symbol,
                        'quantity': inv.quantity,
                        'price': inv.price,
                        'total': inv.total,
                        'created_at': inv.created_at
                    }


            result = []
            for investment in merged_investments.values():
                if investment['quantity'] > 0:  
                    result.append({
                        'symbol': investment['symbol'],
                        'quantity': float(investment['quantity']),
                        'price': float(investment['price']),
                        'total': float(investment['total']),
                        'created_at': investment['created_at']
                    })
            
            logger.info(f"Get Investments Success - User: {request.user.email}")
            return Response({
                'success': True,
                'data': result
            })
        except Exception as e:
            logger.error(f"Get Investments Error - User: {request.user.email}, Error: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=500)

    def post(self, request):
        logger.info(f"Add Investment Request - User: {request.user.email}, Data: {request.data}")
        try:
            data = request.data
            action = data.get('action', 'buy')
            quantity = Decimal(str(data.get('quantity')))
            price = Decimal(str(data.get('price')))
            symbol = data.get('symbol')
            
            if action == 'sell':
          
                investments = Investment.objects.filter(user=request.user, symbol=symbol)
                total_quantity = sum(inv.quantity for inv in investments)
                
                if total_quantity < quantity:
                    return Response({
                        'success': False,
                        'message': f'Insufficient shares. You only have {total_quantity} shares.'
                    }, status=400)
                
          
                quantity = -quantity
            
            total = quantity * price
            
            investment = Investment.objects.create(
                user=request.user,
                symbol=symbol,
                quantity=quantity,
                price=price,
                total=total
            )

            logger.info(f"Add Investment Success - User: {request.user.email}, Symbol: {data.get('symbol')}")
            return Response({
                'success': True,
                'data': {
                    'id': investment.id,
                    'symbol': investment.symbol,
                    'quantity': float(investment.quantity),
                    'price': float(investment.price),
                    'total': float(investment.total),
                }
            })
        except Exception as e:
            logger.error(f"Add Investment Error - User: {request.user.email}, Error: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=400)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Gets user configuration information, including preferred sectors"""
        logger.info(f"Get User Profile Request - User: {request.user.email}")
        try:
            user = request.user
            response_data = {
                'success': True,
                'data': {
                    'preferred_sectors': user.preferred_sectors or []
                }
            }
            logger.info(f"Get User Profile Success - User: {request.user.email}")
            return Response(response_data)
        except Exception as e:
            logger.error(f"Get User Profile Error - User: {request.user.email}, Error: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=500) 