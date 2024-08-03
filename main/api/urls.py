from django.urls import path
from .views import ValidateDataView

urlpatterns = [
    path('validate/', ValidateDataView.as_view(), name='validate-data'),
]