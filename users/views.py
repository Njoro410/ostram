import email
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from users.models import Account, Loans
from .serializers import AccountSerializer, LoanSerilizer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
# Create your views here.

@csrf_exempt
@api_view(['POST'])
def Register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def Login(request):
    username = request.data['username']
    password = request.data['password']

    user = User.objects.filter(username=username).first()

    if user is None:
        raise AuthenticationFailed('Account not found')

    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password')

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token,
                        httponly=True,samesite='none',secure=True)

    response.data = {
        'jwt': token
    }

    return response

@csrf_exempt
@api_view(['GET'])
def UserData(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthorized')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)

    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def GetAccountDetails(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthorized')
    
    details = Account.objects.filter(user_id=payload['id']).first()
    serializer = AccountSerializer(details)
    
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def GetLoanDetails(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthorized')
    
    loan = Loans.objects.filter(user_id=payload['id']).first()
    serializer = LoanSerilizer(loan)
    
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def Logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        "message": "success"
    }
    return response
