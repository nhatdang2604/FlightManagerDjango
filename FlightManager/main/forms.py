from django.forms import ModelForm, ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

from .models import *
import re

# Authentication forms
class LoginForm(AuthenticationForm):
    '''Login form

    Required fields:
        - username
        - password
    '''
    username = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Your username',
        }
    ))
    password = forms.CharField(widget = forms.PasswordInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Your password',
        }
    ))

    class Meta:
        model = User,
        fields = [
            'username',
            'password'
        ]

class RegisterForm(UserCreationForm):
    '''Register form

    Required fields:
        - username (unique)
        - password1
        - password2 (must match with password1)
        - email (valid email)
    '''
    username = forms.CharField(widget = forms.TextInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Your username',
        }
    ))
    email = forms.CharField(widget = forms.EmailInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Your email',
        },
    ))
    password1 = forms.CharField(widget = forms.PasswordInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Your password',
        },
    ), label = 'Your password')
    password2 = forms.CharField(widget = forms.PasswordInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Confirm your password',
        }
    ), label = 'Confirm your password')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

class ChangePasswordForm(PasswordChangeForm):
    '''ChangePasswordForm

    Required fields:
    - old_password
    - new_password1
    - new_password2
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget = forms.PasswordInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Your current password'
        })
        self.fields['new_password1'].widget = forms.PasswordInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Your new password',
        })
        self.fields['new_password2'].widget = forms.PasswordInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Confirm your new password',
        })

# Flight forms
class FlightForm(ModelForm):
    '''Flight form

    Required fields:
    - departure_airport
    - arrival_airport
    - date_time
    - transition_airports (multiple)
    '''
    class Meta:
        model = Flight
        fields = [
            'departure_airport',
            'arrival_airport',
            'date_time',
        ]

        widgets = {
            'departure_airport' : forms.Select(attrs = {
                'class' : 'form-control',
            }),
            'arrival_airport' : forms.Select(attrs = {
                'class' : 'form-control',
            }),
            'date_time' : forms.TextInput(attrs = {
                'class' : 'form-control',
                'type' : 'datetime-local',
            }),
        }
    
    def clean(self):
        '''Custom form validation:

        - Departure Airports cannot be the same as Arrival Airport
        '''
        departure_airport = self.cleaned_data.get('departure_airport')
        arrival_airport = self.cleaned_data.get('arrival_airport')

        if departure_airport == arrival_airport:
            raise ValidationError({
                'departure_airport' : 'Departure and Arrival Airport must not be the same.',
                'arrival_airport' : 'Departure and Arrival Airport must not be the same.'
            })
        
class FlightDetailForm(ModelForm):
    '''FlightDetailForm

    Required fields:
    - flight_time
    - first_class_seat_size
    - second_class_seat_size
    - first_class_ticket_price
    - second_class_ticket_price
    '''

    '''Integers defined here
    '''
    flight_time = forms.DecimalField(
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Flight time (in minutes)',
        })
    )
    first_class_seat_size = forms.DecimalField(
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Total first class seats',
        }),
    )
    second_class_seat_size = forms.DecimalField(
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Total economy class seats',
        }),
    )
    first_class_ticket_price = forms.DecimalField(
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Price for a First Class ticket',
        }),
    )
    second_class_ticket_price = forms.DecimalField(
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Price for a Economy Class ticket',
        }),
    )

    class Meta:
        model = FlightDetail
        fields = '__all__'
        exclude = ['flight']

    def clean(self):
        '''Custom form validation:

        - Flight time must be > 0
        - First class seats & Economy class seats must be >= 0
        '''
        flight_time = self.cleaned_data.get('flight_time')
        first_class_seat_size = self.cleaned_data.get('first_class_seat_size')
        second_class_seat_size = self.cleaned_data.get('second_class_seat_size')
        first_class_ticket_price = self.cleaned_data.get('first_class_ticket_price')
        second_class_ticket_price = self.cleaned_data.get('second_class_ticket_price')

        if flight_time <= 0:
            raise ValidationError({
                'flight_time' : 'Flight time cannot be negative or zero minutes.'
            })
        
        if first_class_seat_size < 0:
            raise ValidationError({
                'first_class_seat_size' : 'First class seats cannot be a negative.'
            })

        if second_class_seat_size < 0:
            raise ValidationError({
                'second_class_seat_size' : 'Economy class seats cannot be a negative.'
            })
        
        if first_class_ticket_price < 0:
            raise ValidationError({
                'first_class_ticket_price' : 'First class ticket price cannot be negative.'
            })
        
        if second_class_ticket_price < 0:
            raise ValidationError({
                'second_class_ticket_price' : 'Economy class ticket price cannot be negative.'
            })

# Airport forms
class AirportForm(ModelForm):
    '''Airport Form

    Required fields:
    - name
    '''
    class Meta:
        model = Airport
        fields = '__all__'

        widgets = {
            'name' : forms.TextInput(attrs = {
                'class' : 'form-control',
                'placeholder' : 'New Airport name'
            }),
        }

class TransitionAirportForm(ModelForm):
    '''TransitionAirport Form

    Required fields:
    - airport
    - transition_time
    - note
    '''

    '''Integers defined here
    '''
    transition_time = forms.DecimalField(
        widget = forms.NumberInput(attrs = {
            'class' : 'form-control',
            'placeholder' : 'Transition time',
        }),
    )
    note = forms.CharField(
        widget = forms.Textarea(attrs = {
            'class' : 'form-control',
            'rows' : 3,
            'placeholder' : 'Note (optional)'
        }),
        required = False,
    )

    def __init__(self, *args, **kwargs) -> None:
        self.route_airports = kwargs.pop('route_airports')
        super().__init__(*args, **kwargs)

    class Meta:
        model = TransitionAirport
        fields = '__all__'
        exclude = [
            'flight',
        ]

        widgets = {
            'airport' : forms.Select(attrs = {
                'class' : 'form-control',
            }),
        }
    
    def clean(self):
        '''Custom form validation:

        - transition_time must be > 0.
        '''
        transition_time = self.cleaned_data.get('transition_time')
        airport = self.cleaned_data.get('airport')

        if transition_time <= 0:
            raise ValidationError({
                'transition_time' : 'Transition time cannot be negative or zero minutes!'
            })

        if airport in self.route_airports:
            raise ValidationError({
                'airport' : 'This airport existed in flight route, please double-check.'
            })

# Ticket forms
class FlightTicketForm(ModelForm):
    '''FlightTicketForm

    Required fields:
    - name
    - phone
    - identity_code
    - ticket_class
    '''

    '''Change default order of fields
    '''
    field_order = (
        'name',
        'phone',
        'identity_code',
        'ticket_class',
    )

    def __init__(self, *args, **kwargs) -> None:
        self.flight = kwargs.pop('flight', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        ticket_class = self.cleaned_data.get('ticket_class')

        ticket_class_condition_check = True

        '''This is a complete hell, but we don't have time to make a dynamically loaded ticket-class validation.
        '''

        if ticket_class.name == "First":
            ticket_class_condition_check = self.flight.flightdetail.first_class_seat_size > self.flight.ticket_set.filter(ticket_class = ticket_class).count()

        elif ticket_class.name == "Economy":
            ticket_class_condition_check = self.flight.flightdetail.second_class_seat_size > self.flight.ticket_set.filter(ticket_class = ticket_class).count()

        if not ticket_class_condition_check:
            raise ValidationError({
                'ticket_class' : 'This class is out of seats, please choose another class.'
            })
        
        '''Phone and Identity Code should be numeric only.
        '''
        phone = self.cleaned_data.get('phone')
        identity_code = self.cleaned_data.get('identity_code')

        if not re.match(r'\d', phone):
            raise ValidationError({
                'phone' : 'Phone should contains numeric characters only.'
            })
        
        if not re.match(r'\d', identity_code):
            raise ValidationError({
                'identity_code' : 'Identity Code should contains numeric characters only.'
            })

    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = [
            'customer',
            'flight',
            'is_booked',
            'price'
        ]

        widgets = {
            'ticket_class' : forms.Select(
                attrs = {
                    'class' : 'form-control'
                }
            ),
            'name' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'Your name',
                }
            ),
            'phone' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'Your phone',
                }
            ),
            'identity_code' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'Your Identity Code',
                }
            ),
        }

# Customer forms
class CustomerForm(ModelForm):
    '''Customer Form

    Required fields:
    - name
    - phone
    - identity_code
    '''
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = [
            'user',
        ]
    
        widgets = {
            'name' : forms.TextInput(attrs = {
                'class' : 'form-control',
                'placeholder' : 'Your name',
            }),
            'phone' : forms.TextInput(attrs = {
                'class' : 'form-control',
                'placeholder' : 'Your phone',
            }),
            'identity_code' : forms.TextInput(attrs = {
                'class' : 'form-control',
                'placeholder' : 'Your ID',
            }),
        }
    
    def clean(self):
        '''Data validation.
        '''

        '''Phone and Identity Code should be numeric only.
        '''
        phone = self.cleaned_data.get('phone')
        identity_code = self.cleaned_data.get('identity_code')

        if not re.match(r'\d', phone):
            raise ValidationError({
                'phone' : 'Phone should contains numeric characters only.'
            })
        
        if not re.match(r'\d', identity_code):
            raise ValidationError({
                'identity_code' : 'Identity Code should contains numeric characters only.'
            })