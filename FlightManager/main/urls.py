from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomepageView.as_view(), name = 'home'),

    # Authentication
    path('register/', views.RegisterView.as_view(), name = 'auth.signup'),
    path('login/', views.LoginView.as_view(), name = 'auth.signin'),
    path('logout/', views.auth_logout, name = 'auth.signout'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name = 'profile.view'),
    path('profile/update', views.UpdateProfileView.as_view(), name = 'profile.update_information'),
    path('profile/update/password', views.UpdatePasswordView.as_view(), name= 'profile.update_password'),

    # Airport
    path('airport/', views.ListAirportView.as_view(), name = 'airport.list'),
    path('airport/create/', views.CreateAirportView.as_view(), name = 'airport.create'),
    path('airport/update/<str:pk>/', views.UpdateAirportView.as_view(), name = 'airport.update'),
    path('airport/delete/<str:pk>/', views.DeleteAirportView.as_view(), name = 'airport.delete'),

    # Flight
    path('flight/', views.ListFlightView.as_view(), name = 'flight.list'),
    path('flight/create/', views.CreateFlightView.as_view(), name = 'flight.create'),
    path('flight/update/<str:pk>/', views.UpdateFlightView.as_view(), name = 'flight.update'),
    path('flight/delete/<str:pk>/', views.DeleteFlightView.as_view(), name = 'flight.delete'),

    # Flight Detail
    path('flight/detail/<str:pk>/', views.DetailFlightView.as_view(), name = 'flight.detail'),
    path('flight/detail/<str:pk>/update', views.UpdateFlightDetailView.as_view(), name = 'flight.detail.update'),   #update flight detail

    # Flight search (Filter)
    path('flight/search', views.FlightSearchView.as_view(), name = 'flight.search'),

    # Transition Airport
    path("flight/detail/<str:pk>/transition/create", views.CreateTransitionAirportView.as_view(), name = 'flight.transition.create'),
    path("airport/transition/<str:pk>/update", views.UpdateTransitionAirportView.as_view(), name = 'flight.transition.update'),
    path("airport/transition/<str:pk>/delete", views.DeleteTransitionAirportView.as_view(), name = 'flight.transition.delete'),

    # Booking
    path('flight/<str:pk>/reservation/create', views.CreateFlightTicketView.as_view(), name = 'flight.reservation.create'),
    path('reservation/list', views.ListFlightTicketView.as_view(), name = 'flight.reservation.list'),
    path('reservation/detail/<str:pk>/', views.DetailFlightTicketView.as_view(), name = 'flight.reservation.detail'),
    path('reservation/detail/<str:pk>/update', views.UpdateFlightTicketView.as_view(), name = 'flight.reservation.update'),
    path('reservation/detail/<str:pk>/delete', views.DeleteFlightTicketView.as_view(), name = 'flight.reservation.delete'),
    path('reservation/payment/<str:pk>/', views.PayFlightTicketView.as_view(), name = 'flight.reservation.payment'),

    # Report
    path('report/general', views.ListFlightReportGeneralView.as_view(), name = 'report.general'),
    path('report/yearly', views.ListFlightReportYearlyView.as_view(), name = 'report.yearly'),
]