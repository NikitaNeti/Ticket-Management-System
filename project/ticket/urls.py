from django.contrib import admin
from django.urls import path
from ticket.views import *



urlpatterns = [

    path('', HomeView.as_view(),name='home'),
    # path('register', RegisterationView, name='register'),
    path('register', RegisterationView.as_view(), name='register'),
    path('login', CustomerLoginView.as_view(),name='login'),
    path('logout', LogoutView.as_view(),name='logout'),
    # path('logout', logoutuser,name='logout'),
    path('test', get_user_mobile,name='test'),
    path('newticket', CreateTicketView.as_view(),name='newticket'),
    # path('newticket', CreateTicketView,name='newticket'),
    path('ticketlist', ViewAllTicketView,name='ticketlist'),
    path('assigned_tickets', assigned_tickets,name='assigned_tickets'),
    path('update_ticket_status/<int:id>/', update_ticket_status,name='update_ticket_status'),
    path('report', ReportView.as_view(),name='report'),
    # path('report', report,name='report'),



]



#    {{form.user}} <br>    

#            <label for="">Mobile</label>
#             {{form.mobile}}<br><br>
#            <label for="">Assets</label>
#             {{form.assets}}<br><br>
#            <label for="">Priority</label>
#             {{form.priority}}<br><br>
#            <label for="">Serial No.</label>
#             {{form.serial_no}}<br><br>
#            <label for="">Model No</label>
#             {{form.model_no}}<br><br>
#            <label for="">Tcketstatus</label>
#             {{form.ticketstatus}} <br> <br>
#             <label for="">Assign To</label>
#             {{form.assigned_to}}