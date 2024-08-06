from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RequestLog, ApiKeys
from .serializers import InputDataSerializer
from django.utils import timezone
from django.conf import settings

class ValidateDataView(APIView):
    """
    API view to validate input data that should be in format of list of dicts where
    key is number and attribute is text.

    Attributes:
        RATE_LIMIT (int): The maximum number of allowed requests per minute per IP address
                          when the API key is invalid or missing. Default is 3.
    """
    RATE_LIMIT = 3

    def post(self, request):
        """
        Handles POST requests to validate input data.

        Steps:
        1. Get the current time and client IP address.
        2. Check for a valid API key in the request headers.
        3. Apply rate limiting if the API key is missing or invalid.
        4. Log the request in the RequestLog model.
        5. Validate each item in the request data using the InputDataSerializer.
        6. Respond with the count of valid and invalid items.

        Args:
            request: The request object containing the data to be validated and headers.

        Returns:
            Response: A Response object containing the counts of valid and invalid items,
                      or an error message if the rate limit is exceeded.
        """
        now = timezone.now()
        ip_address = self.get_client_ip(request)
        api_key = ApiKeys.objects.filter(api_key=request.headers.get('apikey'), valid_from__lte=now, valid_to__gte=now).first()

        recent_requests = RequestLog.objects.filter(ip=ip_address, request_time__gt=now - timezone.timedelta(minutes=1))
        if not api_key:
            if recent_requests.count() >= self.RATE_LIMIT:
                return Response({"error": "Rate limit exceeded"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        RequestLog.objects.create(ip=ip_address, api_key=api_key)
        
        valid_count = 0
        invalid_count = 0
        for item in request.data:
            serializer = InputDataSerializer(data=item)
            if serializer.is_valid():
                valid_count += 1
            else:
                invalid_count += 1

        return Response({"valid": valid_count, "invalid": invalid_count}, status=status.HTTP_200_OK)

    def get_client_ip(self, request):
        """
        Helper method to get the client's IP address from the request.

        Args:
            request: The request object.

        Returns:
            str: The client's IP address.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # set by proxies or load balancers to indicate the original IP address of the client making the request
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')                    # reflects the direct connection to the server
        return ip
