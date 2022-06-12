from django.db import IntegrityError
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group, Permission

from .models import *
from .service import *

def populate_models(sender, **kwargs):
    '''Create and assign permissions to group.
    '''
    # Create groups
    try:
        customer_group = Group.objects.create(name = 'Customer')
        manager_group = Group.objects.create(name = 'Manager')
        print('Created groups')

        '''We don't need all permissions on all models,
        since some permissions overlaps or inside another permission.
        '''

        customer_permissions = [
            'view_flight',
            'add_ticket',
            'change_ticket',
            'delete_ticket',
            'view_ticket',
            'add_reservation',
            'change_reservation',
            'delete_reservation',
            'view_reservation',
        ]

        manager_permission = [
            'view_flight',
            'add_flight',
            'change_flight',
            'delete_flight',
            'view_airport',
            'add_airport',
            'change_airport',
            'delete_airport',
            'add_ticket',
            'change_ticket',
            'delete_ticket',
            'view_ticket',
            'add_reservation',
            'change_reservation',
            'delete_reservation',
            'view_reservation',
        ]

        # Assign permissions to groups
        for permission_codename in customer_permissions:
            print(f'Adding {permission_codename} for customer')
            customer_group.permissions.add(Permission.objects.get(codename = permission_codename))

        for permission_codename in manager_permission:
            print(f'Adding {permission_codename} for manager')
            manager_group.permissions.add(Permission.objects.get(codename = permission_codename))

        print('Added permissions')
    except IntegrityError:
        print('Permission groups already existed, skipping..')
    
    # Adding default ticket classes
    first_class_object = TicketClass.objects.get_or_create(name = 'First')
    print(f'Created {first_class_object}')

    second_class_object = TicketClass.objects.get_or_create(name = 'Economy')
    print(f'Created {second_class_object}')

def customer_profile(sender, instance, created, **kwargs):
    '''Create a Customer profile when a new User is created.
    '''
    if created:
        # Add to group later
        user = instance
        customer_group = Group.objects.get(name = 'Customer')
        customer_group.user_set.add(user)

        # Create a new Customer and link it with the newly-created User.
        new_customer = Customer(user = user)

        # Using Service (wth?) to create.
        customer_service = CustomerService()
        customer_service.createCustomer(new_customer)

def flight_detail(sender, instance, created, **kwargs):
    '''Create a Detail when a new Flight is created
    '''
    if created:
        new_flight_detail = FlightDetail(flight = instance)

        new_flight_detail.save()

post_save.connect(customer_profile, sender = User)
post_save.connect(flight_detail, sender = Flight)