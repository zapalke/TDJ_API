from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RequestLog, ApiKeys
from .serializers import InputDataSerializer
from django.utils import timezone
from django.conf import settings

class ValidateDataView(APIView):
    RATE_LIMIT = 3

    def post(self, request):
        now = timezone.now()
        ip_address = self.get_client_ip(request)
        api_key = ApiKeys.objects.filter(api_key=request.headers.get('apikey'), valid_from__lte=now).first()

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
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
