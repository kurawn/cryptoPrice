from django.urls import path

from .views import index, get_prices, PairAutocomplete

urlpatterns = [
    path('', index, name='index'),
    path('api/prices/', get_prices, name='get_prices'),
    path('autocomplete/pairs/', PairAutocomplete.as_view(), name='pair-autocomplete'),
]
