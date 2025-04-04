from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import json
from django.http import JsonResponse
from django.conf import settings
import logging
import requests
from datetime import datetime, timedelta
import openai
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# 获取日志记录器
logger = logging.getLogger('api')

def stocksjson(request):
    logger.debug(f"Received request with params: {request.GET}")
 
    filename = request.GET.get('filename')
    if not filename:
        return JsonResponse({"code": 400, "error": "Missing filename"}, status=400)


    print(f"Looking for file: {filename}")

    file_path = os.path.join(settings.BASE_DIR, 'data/stock_JSON', f"{filename}.json")
    print(f"Full path: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")

    try:
       
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

     
        return JsonResponse({"code": 200, "data": data})

    except FileNotFoundError:
        print(f"File not found: {file_path}") 
        return JsonResponse({"code": 999, "error": f"No such file: {filename}.json"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"code": 500, "error": "Invalid JSON format"}, status=500)
    except Exception as e:
        print(f"Error: {str(e)}")  
        return JsonResponse({"code": 500, "error": str(e)}, status=500)

def company_news(request):
    symbol = request.GET.get('symbol')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    logger.info(f"Company News Request - Symbol: {symbol}, From: {from_date}, To: {to_date}")
    
    if not symbol:
        logger.warning("Company News Request Failed - Missing symbol")
        return JsonResponse({"code": 400, "error": "Missing symbol"}, status=400)

    # Get date range from request parameters or use default (7 days)
    end_date = datetime.strptime(
        request.GET.get('to_date', datetime.now().strftime('%Y-%m-%d')),
        '%Y-%m-%d'
    )
    
    if request.GET.get('from_date'):
        start_date = datetime.strptime(request.GET.get('from_date'), '%Y-%m-%d')
    else:
        start_date = end_date - timedelta(days=7)
    
    # Format dates as YYYY-MM-DD
    from_date = start_date.strftime('%Y-%m-%d')
    to_date = end_date.strftime('%Y-%m-%d')

    # Finnhub API endpoint
    url = f"https://finnhub.io/api/v1/company-news"
    
    try:
        logger.info(f"Calling Finnhub API - Symbol: {symbol}, From: {from_date}, To: {to_date}")
        response = requests.get(url, params={
            'symbol': symbol,
            'from': from_date,
            'to': to_date,
            'token': 'cuptivpr01qk8dnmbkd0cuptivpr01qk8dnmbkdg'
        })
        
        if response.status_code == 200:
            news_data = response.json()
            # Limit to 5 most recent news items and format them
            formatted_news = []
            for news in news_data[:5]:
                formatted_news.append({
                    'headline': news.get('headline'),
                    'summary': news.get('summary'),
                    'url': news.get('url'),
                    'datetime': datetime.fromtimestamp(news.get('datetime')).strftime('%Y-%m-%d %H:%M')
                })
            
            logger.info(f"Company News Success - Symbol: {symbol}, Found {len(formatted_news)} news items")
            return JsonResponse({"code": 200, "data": formatted_news})
        else:
            logger.error(f"Finnhub API Error - Symbol: {symbol}, Status: {response.status_code}")
            return JsonResponse(
                {"code": response.status_code, "error": "Failed to fetch news"}, 
                status=response.status_code
            )
            
    except Exception as e:
        logger.error(f"Company News Error - Symbol: {symbol}, Error: {str(e)}")
        return JsonResponse({"code": 500, "error": str(e)}, status=500)

class InvestmentAdviceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
    
        logger.info(f"Investment Advice Request - User: {request.user.email}, Data: {request.data}")
        
        try:
  
            stock_info = request.data.get('stock_info', {})

     
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

            user = request.user

            current_date = datetime.now()
    
            age = current_date.year - user.date_of_birth.year

            age = age 
            occupation = user.occupation
            annual_income = user.annual_income
            investment_experience = user.investment_experience
            risk_level = user.risk_level
            preferred_sectors = user.preferred_sectors

      
            company_name = stock_info['company_name']
            stock_industry = stock_info['stock_industry']
            stock_description = stock_info['stock_description']
            other_stock_data = stock_info['other_stock_data']
            if stock_info.get('stock_news_summary') is None:
                stock_news_summary = 'currently no news'
            else:
                stock_news_summary = stock_info['stock_news_summary']

      
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional investment advisor."},
                    {"role": "user", "content": f"""
                    User Profile:
                    - Age: {age}
                    - Occupation: {occupation}
                    - Annual Income: {annual_income}
                    - Investment Experience: {investment_experience}
                    - Risk Tolerance: {risk_level}
                    - Preferred Sectors: {preferred_sectors}

                    Stock Information:
                    - Company Name: {company_name}
                    - Industry: {stock_industry}
                    - Company Description: {stock_description}
                    - News: {stock_news_summary}
                    - Additional Information: {other_stock_data}

                    Please provide an investment analysis for this stock based on the above information. Format your response as follows:

                    1. Company Overview
                    2. Industry and Risk Analysis
                    3. Management Team Analysis
                    4. Investment Preference Match
                    5. Key Considerations
                    6. Summary

                    Note: Please maintain a neutral tone in your analysis. Avoid using absolute terms like "recommend" or "not recommend". 
                    Provide balanced insights to help the user make their own informed investment decision.
                    """}
                ]
            )
            
        
            advice = response.choices[0].message.content
            

            logger.info(f"OpenAI Response for {request.user.email} - Stock: {company_name}")
            
 
            logger.info(f"Investment Advice Success - User: {request.user.email}, Stock: {company_name}")
            return Response({
                'success': True,
                'data': advice
            })
            
        except Exception as e:
         
            logger.error(f"Investment Advice Error - User: {request.user.email}, Error: {str(e)}")
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)