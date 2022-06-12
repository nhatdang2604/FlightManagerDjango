from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

#Account infc
class Customer(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 200, null = True)
    identity_code = models.CharField(max_length = 200, null = True)
    profile_pic = models.ImageField(default = "blank.jpg", null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        if self.name is not None:
            return self.name
        return 'Unamed Customer'
    
    def is_in_group(self, group_name : str) -> bool:
        return self.user.groups.filter(name = group_name).exists()

class Manager(Customer):
    def __str__(self):
        return self.name

class Admin(Manager):
    def __str__(self):
        return self.name

class Airport(models.Model):
    name = models.CharField(max_length = 200, null = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    
    class Meta:
        '''Paginator requires explicitly ordering definition
        in order to sort Airports correctly.
        '''
        ordering = ('-id',)

class Flight(models.Model):
    departure_airport = models.ForeignKey(Airport, null = True, on_delete = models.CASCADE, related_name = "departure_airport")
    arrival_airport = models.ForeignKey(Airport, null = True, on_delete = models.CASCADE, related_name = "arrival_airport")
    date_time = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self) -> str:
        return f'Flight {self.id}'
    
    @property
    def total_seats(self) -> int:
        '''Return total seats of this Flight.
        '''
        try:
            result = self.flightdetail.first_class_seat_size + self.flightdetail.second_class_seat_size
            return result
        except TypeError:
            return 0

    @property
    def is_departed(self) -> bool:
        return self.date_time <= now()
    
    @property
    def is_bookable(self) -> bool:
        return not self.is_departed and self.total_tickets < self.total_seats
    
    @property
    def total_tickets(self) -> bool:
        return self.ticket_set.count()

    @property
    def total_tickets_sold(self) -> int:
        return self.ticket_set.filter(is_booked = True).count()
    
    @property
    def ticket_sold_percentage(self) -> float:
        try:
            return self.total_tickets_sold * 100 / self.total_seats
        except ZeroDivisionError:
            return 0

    class Meta:
        '''Paginator requires explicitly ordering definition
        in order to sort Airports correctly.
        '''
        ordering = ('date_time',)

class FlightDetail(models.Model):
    flight = models.OneToOneField(Flight, null = True, blank = True, on_delete = models.CASCADE)
    flight_time =  models.IntegerField(null = True)
    first_class_seat_size = models.IntegerField(null = True)
    first_class_ticket_price = models.IntegerField(null = True)
    second_class_seat_size = models.IntegerField(null = True)
    second_class_ticket_price = models.IntegerField(null = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return f'Detail of {self.flight}'

class TransitionAirport(models.Model):
    airport = models.ForeignKey(Airport, null = True, on_delete = models.CASCADE)
    flight = models.ForeignKey(Flight, null = True, on_delete = models.CASCADE)
    transition_time =  models.IntegerField(null = True) #minutes
    note = models.CharField(max_length = 200, null = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return f'Transition Airport {self.id}'

class TicketClass(models.Model):
    name = models.CharField(max_length = 200, null = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    customer = models.ForeignKey(Customer, null = True, on_delete = models.CASCADE)
    flight = models.ForeignKey(Flight, null = True, on_delete = models.CASCADE)
    ticket_class = models.ForeignKey(TicketClass, null = True, on_delete = models.CASCADE)

    #name of the person own the ticket
    name = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 200, null = True)
    identity_code = models.CharField(max_length = 200, null = True)

    is_booked = models.BooleanField(null = True, default = False)
    price = models.IntegerField(null = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return f'{self.flight} ticket booked by {self.customer}'

    @property
    def can_update(self) -> bool:
        '''Can only update Tickets with Flight non-departed and unpaid.
        '''
        return not self.flight.is_departed and not self.is_booked

    @property
    def is_canceled(self) -> bool:
        '''Tickets are canceled automatically when flight taken off and still unpaid.
        '''
        return self.flight.is_departed and not self.is_booked

    class Meta:
        '''Paginator requires explicitly ordering definition
        in order to sort Tickets correctly.
        '''
        ordering = ('-date_created',)

class Reservation(models.Model):
    ticket = models.OneToOneField(Ticket, null = True, blank = True, on_delete = models.CASCADE)
    date_booked = models.DateField()
    date_created = models.DateTimeField(auto_now_add = True)

class Policy(models.Model):
    name = models.CharField(max_length = 200, null = True)
    datatype = models.CharField(max_length = 200, null = True)
    value = models.IntegerField(null = True)
    is_applied = models.BooleanField(null = True, default = False)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name