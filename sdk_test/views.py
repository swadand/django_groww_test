import requests
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sdk_test.types import EXCHANGE, ORDER, PRODUCT, SEGMENT, TRANSACTION, VALIDITY
from .models import UserToken
from growwapi import GrowwAPI
from django.conf import settings
import pyotp

@api_view(["POST"])
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    try:
        totp_gen = pyotp.TOTP(settings.GROWW_SECRET_KEY)
        totp = totp_gen.now()
    
        access_token = GrowwAPI.get_access_token(api_key=settings.GROWW_KEY, totp=totp)
        
        UserToken.objects.update_or_create(
            user=user,
            defaults={"access_token": access_token}
        )
    except:
        return Response({"error": "External login failed"}, status=400)
    
    return Response({"message": "Login successful"}, status=200)


def get_user_token(user):
    try:
        return user.token.access_token
    except UserToken.DoesNotExist:
        return None

### Place Order
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request):
    symbol = request.GET.get('symbol', None)
    quantity = request.GET.get('quantity', 1)
    validity = request.GET.get('validity', 'day')
    exchange = request.GET.get('exchange', 'nse')
    segment = request.GET.get('segment', 'cash')
    product = request.GET.get('product', 'cnc')
    order_type = request.GET.get('order_type', 'limit')
    transaction_type = request.GET.get('transaction_type', 'buy')
    
    access_token = get_user_token(request.user)
    
    if symbol is None:
        return Response({"error": "Symbol is Required for an order."}, status=403)
    if not access_token:
        return Response({"error": "No access token found"}, status=403)

    try:
        growwapi = GrowwAPI(access_token)
        
        place_order_response = growwapi.place_order(
        trading_symbol=symbol,
        quantity=quantity,
        validity=VALIDITY[validity],
        exchange=EXCHANGE[exchange],
        segment=SEGMENT[segment],
        product=PRODUCT[product],
        order_type=ORDER[order_type],
        transaction_type=TRANSACTION[transaction_type],
        # price=250,               # Optional: Price of the stock (for Limit orders)
        # trigger_price=245,       # Optional: Trigger price (if applicable)
        #     order_reference_id="Ab-654321234-1628190"  # Optional: User provided 8 to 20 length alphanumeric reference ID to track the order
        )
    except:
        return Response({"error": "Order Placement Failed."}, status=400)
    
    return Response(place_order_response.json(), status=place_order_response.status_code)


### Historical Data
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_historical_data(request):
    symbol = request.GET.get('symbol', 'RELIANCE')
    segment = request.GET.get('segment', 'cash')
    exchange = request.GET.get('exchange', 'nse')
    start_time = request.GET.get('start_t', '2025-02-27 10:00:00')
    end_time = request.GET.get('end_t', '2025-02-27 14:00:00')
    
    
    access_token = get_user_token(request.user)
    if not access_token:
        return Response({"error": "No access token found"}, status=403)

    try:
        growwapi = GrowwAPI(access_token)
        
        # end_time_in_millis = int(time.time() * 1000)
        # start_time_in_millis = end_time_in_millis - (24 * 60 * 60 * 1000)
            
        historical_data_response = growwapi.get_historical_candle_data(
            trading_symbol=symbol,
            exchange=EXCHANGE[exchange],
            segment=SEGMENT[segment],
            start_time=start_time,
            end_time=end_time,
            interval_in_minutes=5
        )
    except:
        return Response({"error": "Fetching Holdings Failed."}, status=400)
    
    return Response(historical_data_response.json(), status=historical_data_response.status_code)

### PORTFOLIO APIS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_holdings(request):
    access_token = get_user_token(request.user)
    if not access_token:
        return Response({"error": "No access token found"}, status=403)

    try:
        growwapi = GrowwAPI(access_token)
        holdings_response = growwapi.get_holdings_for_user()
    except:
        return Response({"error": "Fetching Holdings Failed."}, status=400)
    
    return Response(holdings_response.json(), status=holdings_response.status_code)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_positions(request):
    segment = request.GET.get('segment', 'cash')
    access_token = get_user_token(request.user)
    
    if not access_token:
        return Response({"error": "No access token found"}, status=403)

    try:
        growwapi = GrowwAPI(access_token)
        positions_response = growwapi.get_positions_for_user(segment=SEGMENT[segment])
    except:
        return Response({"error": "Fetching Holdings Failed."}, status=400)
    
    return Response(positions_response.json(), status=positions_response.status_code)
