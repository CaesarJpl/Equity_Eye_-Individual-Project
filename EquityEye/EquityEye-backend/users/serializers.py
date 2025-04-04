from rest_framework import serializers
from .models import User, FavoriteStock, Investment

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 
            'password',
            'date_of_birth',
            'occupation',
            'annual_income',
            'risk_level',
            'loss_tolerance',
            'market_reaction',
            'preferred_sectors',
            'investment_experience'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'date_of_birth': {'required': True},
            'occupation': {'required': True},
            'annual_income': {'required': True},
            'risk_level': {'required': True},
            'loss_tolerance': {'required': True},
            'market_reaction': {'required': True},
            'preferred_sectors': {'required': True},
            'investment_experience': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data.get('date_of_birth'),
            occupation=validated_data.get('occupation'),
            annual_income=validated_data.get('annual_income'),
            risk_level=validated_data.get('risk_level'),
            loss_tolerance=validated_data.get('loss_tolerance'),
            market_reaction=validated_data.get('market_reaction'),
            preferred_sectors=validated_data.get('preferred_sectors'),
            investment_experience=validated_data.get('investment_experience')
        )
        return user

class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('date_of_birth', 'occupation', 'annual_income')

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('risk_level', 'loss_tolerance', 'market_reaction', 
                 'preferred_assets', 'investment_experience')

class FavoriteStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteStock
        fields = ('symbol', 'name', 'added_at')

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ('symbol', 'quantity', 'price', 'total', 'date') 