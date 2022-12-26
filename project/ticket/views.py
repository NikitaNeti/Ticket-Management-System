from django.shortcuts import render
from .forms import SignupForm, TicketForm
from .models import CustomUserModel,Ticket
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib import messages
from django.views import View
from django.views.generic import FormView, RedirectView,TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy,reverse
import datetime
from django.contrib.auth.hashers import make_password
import random
from django.db.models import Count
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class RegisterationView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('home')
   
    def form_valid(self,form):
        user = form.save(commit=False)
            # auto_pass = request.POST.get('first_name').capitalize()+'@'+str(random.randint(1111, 9999)) 
        if self.request.POST.get('role')=='Subadmin':
            user.is_staff = True

        if self.request.POST.get('role')=='Agent':
            user.is_active = True

        if self.request.POST.get('role')=='User':
            user.is_active = False
                
        auto_pass = 'User'+'@'+'1234'
        hash_pass = make_password(auto_pass)
        user.password = hash_pass
        user.save()
        
        return super(RegisterationView, self).form_valid(form)


class CustomerLoginView(View):
    
    def get(self,*args,**kwargs):
        form = AuthenticationForm()
        return render(self.request, 'login.html',{'form':form})

    def post(self,request,*args,**kwargs):
        fm = AuthenticationForm(request, data=request.POST)
        # umail = request.POST.get('username')
        # upass = request.POST.get('password')
        # user = authenticate(username=umail,password=upass)
        # print(user,'&&&&&&&&&&&&&&&&')
     
        if fm.is_valid():
            umail = fm.cleaned_data.get('username')
            upass = fm.cleaned_data.get('password')
            user = authenticate(username=umail,password=upass)

            if user is not None or user.is_active==True or user.is_superuser==True or user.is_staff==True:
                login(self.request, user)
                return redirect('home')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        return render(request, 'login.html',{'form':fm})
        

# def logoutuser(request):
#     logout(request)
#     return redirect('home')

class LogoutView(RedirectView):
    url = '/'
    def get(self, request):
        logout(request) 
        return super(LogoutView, self).get(request)


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs) 
        today = datetime.date.today()
        context = {
        'active_ticket' : Ticket.objects.filter(created_at=today).count(),
        'closed_ticket' : Ticket.objects.filter(ticketstatus='Closed').count(),
        'resolved_ticket' : Ticket.objects.filter(updated_at=today,ticketstatus='Dispatched').count(),
        'agents_count' : Ticket.objects.values('assigned_to').annotate(Count('assigned_to')).count()
               }
        return context


def ViewAllTicketView(request):
    ticket = Ticket.objects.all()
    return render(request, 'ticket_report.html',{'ticket':ticket})
    

class CreateTicketView(LoginRequiredMixin,CreateView):
    form_class = TicketForm
    template_name = 'newticket.html'
    login_url = 'login'
    redirect_field_name = 'login'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ReportView(LoginRequiredMixin,ListView):
    model = Ticket
    template_name = 'report.html'
    login_url = 'login'
    redirect_field_name = 'login'
    context_object_name = 'tickets'
    paginate_by = 2

    
    def post(self,request):
        search_term = request.POST.get('search', None)
        froms = parse_date(request.POST.get('from-date'))
        to = parse_date(request.POST.get('to-date'))
        status = request.POST.get('status')
        priority = request.POST.get('priority')


        if search_term:
            tickets =Ticket.objects.filter(user__first_name__icontains=search_term)
        
        elif status:
            tickets =Ticket.objects.filter(ticketstatus__icontains=status)
            
        elif froms and to:
            tickets = Ticket.objects.filter(created_at__range=(froms, to))

        elif froms and to and status and priority:
            tickets = Ticket.objects.filter(created_at__range=(froms, to),ticketstatus=status,priority=priority)    
        
        else: 
            tickets = Ticket.objects.all()

        return render(request, 'report.html',{'tickets':tickets})
        

def get_user_mobile(request):
    id = request.GET['id']
    user = CustomUserModel.objects.get(id=id)
    data = {'mobile':user.mobile}
    return JsonResponse(data)
        

@login_required(login_url='login')
def assigned_tickets(request):
    tickets = Ticket.objects.filter(assigned_to =request.user)
    return render(request, 'assigned_tickets.html',{'tickets':tickets})


@login_required(login_url='login')
def update_ticket_status(request,id):
    ticket_obj = Ticket.objects.get(id=id)
    ticket_obj.ticketstatus = request.POST.get('status')
    ticket_obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



# def CreateTicketView(request):
#     form = TicketForm()
    
#     if request.method == 'POST':
#         form = TicketForm(request.POST)
#         form.save()
#         # messages.success(request,'ticket created successfully')
#         return redirect('home')

#     return render(request, 'newticket.html',{'form':form})



# def RegisterationView(request):

#     form = SignupForm()
#     if request.method == 'POST':  
#         form = SignupForm(request.POST,request.FILES or None)
#         if form.is_valid():

#             user = form.save(commit=False)
#             # auto_pass = request.POST.get('first_name').capitalize()+'@'+str(random.randint(1111, 9999)) 
#             if request.POST.get('role')=='Subadmin':
#                 user.is_staff = True

#             if request.POST.get('role')=='Agent':
#                 user.is_active = True

#             if request.POST.get('role')=='User':
#                 user.is_active = False
                
#             # auto_pass = request.POST.get('first_name').capitalize()+'@'+'1234'
#             auto_pass = 'User'+'@'+'1234'
#             hash_pass = make_password(auto_pass)
#             user.password = hash_pass
#             user.save()

#             return redirect('home')

#     return render(request, 'signup.html',{'form':form})

