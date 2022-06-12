from django import forms
from django_filters import DateFromToRangeFilter, ModelChoiceFilter, DateTimeFilter
from django_filters import FilterSet, widgets
import datetime

# Models
from .models import *

# Forms
from .forms import *

class FlightFilter(FilterSet):
    departure_airport = ModelChoiceFilter(
        queryset = Airport.objects,
        widget = forms.Select(
            attrs = {
                'class' : 'form-control',
            },
        ),
        label = 'Departure'
    )
    arrival_airport = ModelChoiceFilter(
        queryset = Airport.objects,
        widget = forms.Select(
            attrs = {
                'class' : 'form-control',
            },
        ),
        label = 'Destination'
    )
    date_time = DateFromToRangeFilter(
        widget = widgets.RangeWidget(
            attrs = {
                'class' : 'form-control',
                'type' : 'date',
            }
        ),
        label = 'Depart in range',
    )

    class Meta:
        model = Flight
        fields = [
            'departure_airport',
            'arrival_airport',
            'date_time'
        ]
        order_by = 'date_time',

class FlightReportGeneralFilter(FilterSet):
    date_time = DateFromToRangeFilter(
        widget = widgets.RangeWidget(
            attrs = {
                'class' : 'form-control',
                'type' : 'date',
            }
        ),
        label = 'Data range',
    )

    class Meta:
        model = Flight
        fields = [
            'date_time'
        ]

class FlightReportYearlyFilter(FilterSet):
    class Meta:
        model = Flight
        fields = [
            'date_time'
        ]