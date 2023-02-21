from django.shortcuts import render, redirect ,HttpResponse ,  HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from .models import Addemployee, Leave_App, Event, Admin_Login , CompanySetup , Absent_emp , Leave_Policy
from .forms import AddemployeeForm, Admin_LoginForm, EventForm, Leave_AppForm , CompanySetupForm , Absent_empForm , Leave_PolicyForm

# from .models import Addemployee, Leave_App, Event, Admin_Login
# from .forms import AddemployeeForm, Admin_LoginForm, EventForm, Leave_AppForm 
from django.conf import settings
from django.core.mail import send_mail
from .filters import ConsumerFilter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime
from datetime import date
import os 
from django.db import connection
from django.db.models import Count 
from django.urls import reverse
from .utils import Calendar, Eventcal
import calendar
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from django.views import generic


def homePage(request):
    return render(request,"homePage.html")

def leavePolicySetting(request):
    Username = request.session['Username']
    if request.method == 'GET':
        try:
            leave = Leave_Policy.objects.get(Username=Username)
        except Leave_Policy.DoesNotExist:
            leave = None
        print(leave)
        
    if request.method == "POST":  
        form = Leave_PolicyForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()
                messages.success(request,"Successfully")  
                return redirect('/leavePolicySetting')  
            except:  
                pass  
    else:  
        form = Leave_PolicyForm()  
    return render(request,"leavePolicySetting.html",{'form':form,'leave':leave})

def leavePolicySetting_update(request):  
    
    Username = request.session['Username']
    leavepolicy = request.POST.get('leavepolicy')
    obj = Leave_Policy.objects.get(Username=Username)
    obj.leavepolicy = leavepolicy
    obj.save()
    messages.success(request, "Leave Policy Update...." )
    return redirect("/leavePolicySetting")




def adminLogin(request):   
    if request.method == 'POST':
        form = Admin_LoginForm(request.POST)  
        Username = request.POST['Username']
        Password = request.POST['Password']
         
        try:
            salary = Admin_Login.objects.get(Username = Username,Password=Password)
            request.session['Username'] = Username
        except Admin_Login.DoesNotExist:
            salary = None


        if salary is not None:
            return redirect('/adminDashboard')                                           
        else:
            messages.error(request,"Invalid Username or Password")
            return render(request,"adminLogin.html")

    return render(request,"adminLogin.html")

# def admin(request):
#     return render(request,'admin.html')
# def employeeDashboard(request):
#     return render(request,'employeeDashboard.html')
# def totalEmployees(request):
#     return render(request,'totalEmployees.html')
# def totalEmployeeDetails(request):
#     return render(request,'totalEmployeeDetails.html')
# def presentEmployees(request):
#     return render(request,'presentEmployees.html')
# def onLeave(request):
#     return render(request,'onLeave.html')
# def companySetup(request):
#     return render(request,'companySetup.html')
# def employeeProfile(request):
#     return render(request,'employeeProfile.html')

def companySetup(request):  
    
    Username = request.session['Username']
    if request.method == 'GET':
        try:
            company = CompanySetup.objects.get(Username=Username)
        except CompanySetup.DoesNotExist:
            company = None
        print(company)
        
        
    if request.method == "POST": 
        form = CompanySetupForm(request.POST)
        
        if form.is_valid(): 
                company_name = form.cleaned_data.get('company_name')
                email = form.cleaned_data.get('email') 
                website = form.cleaned_data.get('website')
                telephone = form.cleaned_data.get('telephone')
                telephone1 = form.cleaned_data.get('telephone1')
                telephone2 = form.cleaned_data.get('telephone2')
                Address = form.cleaned_data.get('Address')
                zip = form.cleaned_data.get('zip')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                country = form.cleaned_data.get('country')
                companyBranch = form.cleaned_data.get('companyBranch')
                department1 = form.cleaned_data.get('department1') 
                department2 = form.cleaned_data.get('department2') 
                department3 = form.cleaned_data.get('department3') 
                department4 = form.cleaned_data.get('department4') 
                department5 = form.cleaned_data.get('department5') 
                
                form.save() 
                print(form)
                return redirect('/totalEmployees')
                
    else: 
        form = CompanySetupForm()
        print(form.errors) 
    return render(request,'companySetup.html',{'form':form,'company':company})
    
def company_update(request):  


    Username = request.session['Username']
    company_name = request.POST.get('company_name')
    email = request.POST.get('email') 
    website = request.POST.get('website')
    telephone = request.POST.get('telephone')
    telephone1 = request.POST.get('telephone1')
    print(telephone1)
    telephone2 = request.POST.get('telephone2')
    print(telephone2) 
    Address = request.POST.get('Address')
    zip = request.POST.get('zip')
    city = request.POST.get('city')
    state = request.POST.get('state')
    country = request.POST.get('country')
    companyBranch = request.POST.get('companyBranch')
    department1 = request.POST.get('department1') 
    print(department1)
    department2 = request.POST.get('department2') 
    department3 = request.POST.get('department3') 
    department4 = request.POST.get('department4') 
    department5 = request.POST.get('department5') 
    obj = CompanySetup.objects.get(Username=Username)
    obj.company_name = company_name
    obj.email = email
    obj.website = website
    obj.telephone = telephone
    obj.telephone1 = telephone1
    obj.telephone2 = telephone2
    obj.Address = Address
    obj.zip = zip
    obj.city = city
    obj.state = state
    obj.country = country
    obj.companyBranch = companyBranch
    obj.department1 = department1
    obj.department2 = department2
    obj.department3 = department3
    obj.department4 = department4
    obj.department5 = department5
    obj.save()
    # messages.success(request, "company_name Update...." )
    return redirect("/companySetup")

def onLeave(request):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']

      
            admin_reg = Admin_Login.objects.get(Username=Username)
            # print(admin_reg)
            
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            # print(total_emp)
            
            current_date = 0 
            current_date = datetime.now().strftime('%Y-%m-%d')
            # print(current_date)  
        
            apply_leave = Leave_App.objects.filter(Date=current_date,leave_status=1).count()
            # print(today_leave)
            
            absent_leave = Leave_App.objects.filter(Date=current_date,leave_status = 3).count()
            
            today_leave = int(apply_leave)+int(absent_leave)
            # print(today_leave)
           
            present_today = int(total_emp)-int(today_leave)
            
            print(present_today)
            
            total_Leave = Leave_App.objects.filter(leave_status=0).count()
            # print(total_Leave)
            

        leaves = Leave_App.objects.raw("""SELECT leave."id",leave."Category",leave."From",leave."to",leave."leavedayCategory_From",leave."leavedayCategory_to",leave."Reason",leave."Emp_ID", add_Employee."Name",add_Employee."Contact",add_Employee."Address",add_Employee."D_O_B",add_Employee."Date_of_join",add_Employee."department",add_Employee."Designation",add_Employee."Reporting_Dept",add_Employee."Email",add_Employee."User_name",add_Employee."Password",add_Employee."Confirm_Password",add_Employee."Emp_ID",add_Employee."Image" FROM leave INNER JOIN add_Employee ON leave."Emp_ID" = add_Employee."Emp_ID" where leave.leave_status=1  AND leave."Date" = current_date """ )
        
        # leaves = Leave_App.objects.filter(Date=current_date,leave_status=1)
        
        if request.method == "POST":  
            form = Leave_AppForm(request.POST)  
            if form.is_valid():  
                try:  
                    form.save()  
                    return redirect('/onLeave')  
                except:  
                    pass  
        else:  
            form = Leave_AppForm() 
            
            absent_emps = Leave_App.objects.filter(Date=current_date,leave_status = 3)
            # print(absent_emps) 
            
            dic ={
                'form':form,
                'leaves':leaves,
                'absent_emps':absent_emps,
                'admin_reg':admin_reg,
                'total_emp':total_emp,
                'total_Leave':total_Leave,
                'today_leave':today_leave,   
                'apply_leave':apply_leave,
                'absent_leave':absent_leave,
                'present_today':present_today
                  
            }
            
        return render(request,'onLeave.html',dic) 
        


def employeeProfile(request,Emp_ID):
    emp = Addemployee.objects.get(Emp_ID=Emp_ID)  
    print(emp)
    return render(request,'employeeProfile.html', {'emp':emp})

def profilestatus(request):
    if request.method == 'POST':
            form = AddemployeeForm(request.POST)  
            Emp_ID = request.POST['Emp_ID']
            
            try:
                emp = Addemployee.objects.get(Emp_ID=Emp_ID) 
                # print(emp)
                request.session['Emp_ID'] = Emp_ID
                    
            except Addemployee.DoesNotExist:
                emp = None
                            
            if emp is not None:
                return redirect('/employeeProfile1')                                           
            else:
                return render(request, 'totalEmployees.html')
            
    #=========================================================
    
def employeeProfile1(request):
    if request.method == "GET": 
            Emp_ID = request.session['Emp_ID']
            emp = Addemployee.objects.get(Emp_ID=Emp_ID)  
              
            return render(request, 'employeeProfile1.html',{'emp' : emp})            
    else:
        return redirect('/adminLogin')
    
    
def totalEmployees(request):
    if request.session.has_key('Username'):
        
        if request.method == 'GET':
            Username = request.session['Username']
            
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            # print(total_emp)
            
            
            current_date = 0 
            current_date = datetime.now().strftime('%Y-%m-%d')
            # print(current_date)  
        
            apply_leave = Leave_App.objects.filter(Date=current_date,leave_status=1).count()
            # print(today_leave)
            
            absent_leave = Leave_App.objects.filter(Date=current_date,leave_status=3).count()
            
            today_leave = int(apply_leave)+int(absent_leave)
            # print(today_leave)
           
            present_today = int(total_emp)-int(today_leave)
            
            # print(present_today)
            
            total_Leave = Leave_App.objects.filter(leave_status=0).count()
            # print(total_Leave)

    #============================================================================
        
            
        try:
            company = CompanySetup.objects.get(Username=Username)
                
        except CompanySetup.DoesNotExist:
            company = None
            print(company)
            
        dep1 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department1" = company_setup."department1" """)
        
        a_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department1",add_Employee."department" AS dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department1" = add_Employee."department"  """)
        count_dep1 = len(list(a_count))
        print(count_dep1)
                    
        dep2 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department2" = company_setup."department2" """)
        
        b_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department2",add_Employee."department" AS count_dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department2" = add_Employee."department" """)
        count_dep2 = len(list(b_count))
        print(count_dep2)
        
        dep3 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department3" = company_setup."department3" """)
        
        c_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department3",add_Employee."department" AS count_dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department3" = add_Employee."department" """)
        count_dep3 = len(list(c_count))
        print(count_dep3)
        
        dep4 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department4" = company_setup."department4" """)
        
        d_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department4",add_Employee."department" AS count_dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department4" = add_Employee."department" """)
        count_dep4 = len(list(d_count))
        print(count_dep4)
        
        dep5 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department5" = company_setup."department5" """)
        
        e_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department5",add_Employee."department" AS count_dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department5" = add_Employee."department" """)
        count_dep5 = len(list(e_count))
        print(count_dep5)             

             #========================================================

            
        dic ={
            'total_emp':total_emp,
            'total_Leave':total_Leave,
            'present_today':present_today,
            'today_leave':today_leave,
            'dep1':dep1,
            'dep2':dep2,
            'dep3':dep3,
            'dep4':dep4,
            'dep5':dep5,
            'count_dep1':count_dep1,
            'count_dep2':count_dep2,
            'count_dep3':count_dep3,
            'count_dep4':count_dep4,
            'count_dep5':count_dep5,
     
        }
            
        return render(request,'totalEmployees.html',dic)   
    else:
        return redirect('/adminLogin')
    
    

    

def totalEmployeeDetails(request):
    if request.session.has_key('Username'):
           
        if request.method == 'GET':
            Username = request.session['Username']
            
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            # print(total_emp)

            
            current_date = 0 
            current_date = datetime.now().strftime('%Y-%m-%d')
            # print(current_date)  
        
            apply_leave = Leave_App.objects.filter(Date=current_date,leave_status=1).count()
            # print(today_leave)
            
            absent_leave = Leave_App.objects.filter(Date=current_date,leave_status=3).count()
            
            today_leave = int(apply_leave)+int(absent_leave)
            # print(today_leave)
           
            present_today = int(total_emp)-int(today_leave)
            
            print(present_today)
            
            total_Leave = Leave_App.objects.filter(leave_status=0).count()
            # print(total_Leave)

            #=============================================
            try:
                company = CompanySetup.objects.get(Username=Username)
                
            except CompanySetup.DoesNotExist:
                company = None
                print(company)
            
            dep1 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department1" = company_setup."department1" """)
        
            a_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department1",add_Employee."department" AS count_dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department1" = add_Employee."department" """)
            count_dep1 = len(list(a_count))
            print(a_count)
            
            dep1_emp_list = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department1",add_Employee.* FROM company_setup INNER JOIN add_Employee ON company_setup."department1" = add_Employee."department" """)
            print(dep1_emp_list)
            
            leaves = Leave_App.objects.filter(Date=current_date,leave_status = 3)
            
            
            
             #========================================================
            
        dic ={
            'total_emp':total_emp,
            'total_Leave':total_Leave,
            'present_today':present_today,
            'today_leave':today_leave,
            'dep1':dep1,
            'count_dep1':count_dep1,
            'dep1_emp_list':dep1_emp_list,
            'leaves':leaves
               
        }
            
        return render(request,'totalEmployeeDetails.html',dic)   
    else:
        return redirect('/adminLogin')


def totalEmployeeDetails_dep2(request):
    if request.session.has_key('Username'):
   
        if request.method == 'GET':
            Username = request.session['Username']
            
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            # print(total_emp)

            
            current_date = 0 
            current_date = datetime.now().strftime('%Y-%m-%d')
            # print(current_date)  
        
            apply_leave = Leave_App.objects.filter(Date=current_date,leave_status=1).count()
            # print(today_leave)
            
            absent_leave = Leave_App.objects.filter(Date=current_date,leave_status=3).count()
            
            today_leave = int(apply_leave)+int(absent_leave)
            # print(today_leave)
           
            present_today = int(total_emp)-int(today_leave)
            
            print(present_today)
            
            total_Leave = Leave_App.objects.filter(leave_status=0).count()
            # print(total_Leave)

            #=============================================
            try:
                company = CompanySetup.objects.get(Username=Username)
                
            except CompanySetup.DoesNotExist:
                company = None
                print(company)

                        
            dep2 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department2" = company_setup."department2" """)
            
            b_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department2",add_Employee."department" AS count_dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department2" = add_Employee."department" """)
            count_dep2 = len(list(b_count))
            
            dep2_emp_list = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department1",add_Employee.* FROM company_setup INNER JOIN add_Employee ON company_setup."department2" = add_Employee."department" """)
            print(dep2_emp_list)
            
             #========================================================
            
        dic ={
            'total_emp':total_emp,
            'total_Leave':total_Leave,
            'present_today':present_today,
            'today_leave':today_leave,
            'dep2':dep2,
            'count_dep2':count_dep2,
            'dep2_emp_list':dep2_emp_list
         
        
        }
            
        return render(request,'totalEmployeeDetails_dep2.html',dic)   
    else:
        return render(request,'totalEmployeeDetails_dep2.html')


def totalEmployeeDetails_dep3(request):
    if request.session.has_key('Username'):
       
            
            
        if request.method == 'GET':
            Username = request.session['Username']
            
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            # print(total_emp)

            
            current_date = 0 
            current_date = datetime.now().strftime('%Y-%m-%d')
            # print(current_date)  
        
            apply_leave = Leave_App.objects.filter(Date=current_date,leave_status=1).count()
            # print(today_leave)
            
            absent_leave = Leave_App.objects.filter(Date=current_date,leave_status=3).count()
            
            today_leave = int(apply_leave)+int(absent_leave)
            # print(today_leave)
           
            present_today = int(total_emp)-int(today_leave)
            
            print(present_today)
            
            total_Leave = Leave_App.objects.filter(leave_status=0).count()
            # print(total_Leave)

            #=============================================
            try:
                company = CompanySetup.objects.get(Username=Username)
                
            except CompanySetup.DoesNotExist:
                company = None
                print(company)

                        
            dep3 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department3" = company_setup."department3" """)
            
            c_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department3",add_Employee."department" AS count_dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department3" = add_Employee."department" """)
            count_dep3 = len(list(c_count))
            # print(count_dep3)
            
            dep3_emp_list = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department3",add_Employee.* FROM company_setup INNER JOIN add_Employee ON company_setup."department3" = add_Employee."department" """)
            print(dep3_emp_list)
            
             #========================================================
            
        dic ={
            'total_emp':total_emp,
            'total_Leave':total_Leave,
            'present_today':present_today,
            'today_leave':today_leave,
            'dep3':dep3,
            'count_dep3':count_dep3,
            'dep3_emp_list':dep3_emp_list
         
        
        }
            
        return render(request,'totalEmployeeDetails_dep3.html',dic)   
    else:
        return render(request,'totalEmployeeDetails_dep3.html')
    
    
def totalEmployeeDetails_dep4(request):
    if request.session.has_key('Username'):
            
            
        if request.method == 'GET':
            Username = request.session['Username']
            
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            # print(total_emp)

            
            current_date = 0 
            current_date = datetime.now().strftime('%Y-%m-%d')
            # print(current_date)  
        
            apply_leave = Leave_App.objects.filter(Date=current_date,leave_status=1).count()
            # print(today_leave)
            
            absent_leave = Leave_App.objects.filter(Date=current_date,leave_status=3).count()
            
            today_leave = int(apply_leave)+int(absent_leave)
            # print(today_leave)
           
            present_today = int(total_emp)-int(today_leave)
            
            print(present_today)
            
            total_Leave = Leave_App.objects.filter(leave_status=0).count()
            # print(total_Leave)

            #=============================================
            try:
                company = CompanySetup.objects.get(Username=Username)
                
            except CompanySetup.DoesNotExist:
                company = None
                print(company)

                        
            dep4 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department4" = company_setup."department4" """)
            
            d_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department4",add_Employee."department" AS count_dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department4" = add_Employee."department" """)
            count_dep4 = len(list(d_count))
            
            dep4_emp_list = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department4",add_Employee.* FROM company_setup INNER JOIN add_Employee ON company_setup."department4" = add_Employee."department" """)
            print(dep4_emp_list)
            
             #========================================================
            
        dic ={
            'total_emp':total_emp,
            'total_Leave':total_Leave,
            'present_today':present_today,
            'today_leave':today_leave,
            'dep4':dep4,
            'count_dep4':count_dep4,
            'dep4_emp_list':dep4_emp_list
         
        
        }
            
        return render(request,'totalEmployeeDetails_dep4.html',dic)   
    else:
        return render(request,'totalEmployeeDetails_dep4.html')
    
    
def totalEmployeeDetails_dep5(request):
    if request.session.has_key('Username'):
        
            
        if request.method == 'GET':
            Username = request.session['Username']
            
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            # print(total_emp)

            
            current_date = 0 
            current_date = datetime.now().strftime('%Y-%m-%d')
            # print(current_date)  
        
            apply_leave = Leave_App.objects.filter(Date=current_date,leave_status=1).count()
            # print(today_leave)
            
            absent_leave = Leave_App.objects.filter(Date=current_date,leave_status=3).count()
            
            today_leave = int(apply_leave)+int(absent_leave)
            # print(today_leave)
           
            present_today = int(total_emp)-int(today_leave)
            
            print(present_today)
            
            total_Leave = Leave_App.objects.filter(leave_status=0).count()
            # print(total_Leave)

            #=============================================
            try:
                company = CompanySetup.objects.get(Username=Username)
                
            except CompanySetup.DoesNotExist:
                company = None
                print(company)

                        
            dep5 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department5" = company_setup."department5" """)
            
            e_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department5",add_Employee."department" AS count_dep1 FROM company_setup INNER JOIN add_Employee ON company_setup."department5" = add_Employee."department" """)
            count_dep5 = len(list(e_count))
            
            dep5_emp_list = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department5",add_Employee.* FROM company_setup INNER JOIN add_Employee ON company_setup."department5" = add_Employee."department" """)
            print(dep5_emp_list)
            
             #========================================================
            
        dic ={
            'total_emp':total_emp,
            'total_Leave':total_Leave,
            'present_today':present_today,
            'today_leave':today_leave,
            'dep5':dep5,
            'count_dep5':count_dep5,
            'dep5_emp_list':dep5_emp_list
         
        
        }
            
        return render(request,'totalEmployeeDetails_dep5.html',dic)   
    else:
        return render(request,'totalEmployeeDetails_dep5.html')


def presentEmployees(request):
    if request.session.has_key('Username'):
        
            
        if request.method == 'GET':
            Username = request.session['Username']
            
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            # print(total_emp)

            current_date = 0 
            current_date = datetime.now().strftime('%Y-%m-%d')
            # print(current_date)  
            print(type(current_date))
        
            apply_leave = Leave_App.objects.filter(Date=current_date,leave_status=1).count()
            # print(today_leave)
            
            absent_leave = Leave_App.objects.filter(Date=current_date,leave_status=3).count()
            
            today_leave = int(apply_leave)+int(absent_leave)
            # print(today_leave)
           
            present_today = int(total_emp)-int(today_leave)
            
            # print(present_today)
            
            total_Leave = Leave_App.objects.filter(leave_status=0).count()
            # print(total_Leave)

            #============================================================================
              
            try:
                company = CompanySetup.objects.get(Username=Username)
                
            except CompanySetup.DoesNotExist:
                company = None
                # print(company)
            
            dep1 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department1" = company_setup."department1" """)
            
            a_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department1",add_Employee.*  FROM company_setup INNER JOIN add_Employee ON company_setup."department1" = add_Employee."department" """)
            count_dep1 = len(list(a_count))
            # print(count_dep1)
            
            a_absent_count=""
            a_absent_count = CompanySetup.objects.raw("""SELECT leave.* , company_setup.*,add_Employee.*
                FROM leave INNER JOIN company_setup
                ON leave."department" = company_setup."department1" inner join
                add_Employee ON leave."department" = add_Employee."department"
                where leave.leave_status = 1 or leave.leave_status = 3 AND leave."Date" = current_date AND leave."Emp_ID" = add_Employee."Emp_ID" """)
            absent_count_dep1 = len(list(a_absent_count))
            
            
            
                   
            dep2 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department2" = company_setup."department2" """)
            
            b_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department2",add_Employee.* FROM company_setup INNER JOIN add_Employee ON company_setup."department2" = add_Employee."department" """)
            count_dep2 = len(list(b_count))
            # print(count_dep2)
            
            b_absent_count = CompanySetup.objects.raw("""SELECT leave.* , company_setup.*,add_Employee.*
                FROM leave INNER JOIN company_setup
                ON leave."department" = company_setup."department2" inner join
                add_Employee ON leave."department" = add_Employee."department"
                where leave.leave_status = 1 or leave.leave_status = 3 AND leave."Date" = current_date AND leave."Emp_ID" = add_Employee."Emp_ID" """)
            absent_count_dep2 = len(list(b_absent_count))
            
            # cursor = connection.cursor()    
            # cursor.execute("""SELECT leave.* , company_setup.*,add_Employee.*
            #     FROM leave INNER JOIN company_setup
            #     ON leave."department" = company_setup."department2" inner join
            #     add_Employee ON leave."department" = add_Employee."department"
            #     where leave.leave_status = 1 or leave.leave_status = 3 AND leave."Date" = current_date AND leave."Emp_ID" = add_Employee."Emp_ID" """)
            # row = cursor.fetchall()
            # print(row)   
            
            dep3 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department3" = company_setup."department3" """)
            
            c_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department3",add_Employee.* FROM company_setup INNER JOIN add_Employee ON company_setup."department3" = add_Employee."department" """)
            count_dep3 = len(list(c_count))
            
            c_absent_count = CompanySetup.objects.raw("""SELECT leave.* , company_setup.*,add_Employee.*
                FROM leave INNER JOIN company_setup
                ON leave."department" = company_setup."department3" inner join
                add_Employee ON leave."department" = add_Employee."department"
                where leave.leave_status = 1 or leave.leave_status = 3 AND leave."Date" = current_date AND leave."Emp_ID" = add_Employee."Emp_ID" """)
            absent_count_dep3 = len(list(c_absent_count))
            
            dep4 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department4" = company_setup."department4" """)
            
            d_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department4",add_Employee.* FROM company_setup INNER JOIN add_Employee ON company_setup."department4" = add_Employee."department" """)
            count_dep4 = len(list(d_count))
            # print(count_dep4)
            
            d_absent_count = CompanySetup.objects.raw("""SELECT leave.* , company_setup.*,add_Employee.*
                FROM leave INNER JOIN company_setup
                ON leave."department" = company_setup."department4" inner join
                add_Employee ON leave."department" = add_Employee."department"
                where leave.leave_status = 1 or leave.leave_status = 3 AND leave."Date" = current_date AND leave."Emp_ID" = add_Employee."Emp_ID" """)
            absent_count_dep4 = len(list(d_absent_count))
            
            dep5 = CompanySetup.objects.raw("""SELECT * from company_setup where company_setup."department5" = company_setup."department5" """)
            
            e_count = CompanySetup.objects.raw("""SELECT company_setup."id",company_setup."department5",add_Employee.* FROM company_setup INNER JOIN add_Employee ON company_setup."department5" = add_Employee."department" """)
            count_dep5 = len(list(e_count))
            # print(count_dep5)  
            
            e_absent_count = CompanySetup.objects.raw("""SELECT leave.* , company_setup.*,add_Employee.*
                FROM leave INNER JOIN company_setup
                ON leave."department" = company_setup."department5" inner join
                add_Employee ON leave."department" = add_Employee."department"
                where leave.leave_status = 1 or leave.leave_status = 3 AND leave."Date" = current_date AND leave."Emp_ID" = add_Employee."Emp_ID" """)
            absent_count_dep5 = len(list(e_absent_count))         
            
            dic ={
                'total_emp':total_emp,
                'total_Leave':total_Leave,
                'present_today':present_today,
                'today_leave':today_leave,
                'dep1':dep1,
                'dep2':dep2,
                'dep3':dep3,
                'dep4':dep4,
                'dep5':dep5,
                'count_dep1':count_dep1,
                'count_dep2':count_dep2,
                'count_dep3':count_dep3,
                'count_dep4':count_dep4,
                'count_dep5':count_dep5,
                'a_count':a_count,
                'b_count':b_count,
                'c_count':c_count,
                'd_count':d_count,
                'e_count':e_count,
                'a_absent_count':a_absent_count,
                'absent_count_dep1':absent_count_dep1,
                'b_absent_count':b_absent_count,
                'absent_count_dep2':absent_count_dep2,
                'c_absent_count':c_absent_count,
                'absent_count_dep3':absent_count_dep3,
                
                'd_absent_count':d_absent_count,
                'absent_count_dep4':absent_count_dep4,
                'e_absent_count':e_absent_count,
                'absent_count_dep5':absent_count_dep5,
           
            }
            
        return render(request,'presentEmployees.html',dic)   
    else:
        return render(request,'presentEmployees.html')
    




def adminDashboard(request):
    # Username = request.session['Username']
    # print(Username)
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
            admin_reg = Admin_Login.objects.get(Username=Username)
            print(admin_reg)
            
            
            total_emp = Addemployee.objects.filter(Emp_status=0).count()
            print(total_emp)
            
            total_Leave = Leave_App.objects.count()
            print(total_Leave)
            present_today = int(total_emp)-int(total_Leave)
            print(present_today,'P')
            dic ={
                'admin_reg':admin_reg,
                'present_today':present_today,
                'total_emp':total_emp,
                'total_Leave':total_Leave
            }
            
            return render(request,'adminDashboard.html',dic)   
    return render(request,"adminDashboard.html")


class CalendarView(generic.ListView):
    
    model = Event
    template_name = 'adminDashboard.html'
    
    def dash(self):
        if self.request.session.has_key('Username'):
            if self.request.method == 'GET':
                Username = self.request.session['Username']
                total_emp = Addemployee.objects.filter(Emp_status=0).count()
                    # print(total_emp)

                current_date = 0 
                current_date = datetime.now().strftime('%Y-%m-%d')
                # print(current_date)  
            
                apply_leave = Leave_App.objects.filter(Date=current_date,leave_status=1).count()
                # print(today_leave)
                
                absent_leave = Leave_App.objects.filter(Date=current_date,leave_status=3).count()
                
                today_leave = int(apply_leave)+int(absent_leave)
                # print(today_leave)
                
                present_today = int(total_emp)-int(today_leave)
                
                # print(present_today)
                
                total_Leave = Leave_App.objects.filter(leave_status=0).count()
                    
                dic ={
                    'total_emp':total_emp,
                    'total_Leave':total_Leave,
                    'today_leave':today_leave,
                    'present_today':present_today
                }
                    
                return dic
        else:
            return redirect("/employeeLogin")
                
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        today = str(get_date(self.request.GET.get('day', None)))
        today_year, today_month, today_date = (int(x) for x in today.split('-'))

        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        cal = Calendar(d.year, d.month, today_date, today_month, today_year)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        event = Eventcal(d.year, d.month)
        html_event = event.formatmonth(withyear=True)
        context['event'] = mark_safe(html_event)
        
        context['dic']=self.dash()
        return context
    
class CalendarViewEmp(generic.ListView):
    
    model = Event
    template_name = 'sidebar.html'
    
    
    def dash(self):   
        Name = self.request.session['Name']
        Emp_ID = self.request.session['Emp_ID']
        Paid_leave = Leave_App.objects.filter(Emp_ID=Emp_ID,Category='Paid Leave').count()
        # print(Paid_leave)
 
        emp_reg = Addemployee.objects.get(Name=Name)
        print(emp_reg.Image)

            
        for leave_paid1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Total_Paid_Leave','Pending_Paid_Leave'):
            print(leave_paid1)
            x_paid=0
            x_paid = list(leave_paid1)
            print(x_paid)
            paidleave = [eval(i) for i in x_paid]
            print(paidleave)
            total_Paid_leave = int(paidleave[0])-int(paidleave[1])
            print(total_Paid_leave)
            
        for leave_sick1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Total_Sick_Leave','Pending_Sick_Leave'):
            print(leave_sick1)
            x_sick = 0
            x_sick = list(leave_sick1)
            print(x_sick)
            sickleave = [eval(i) for i in x_sick]
            print(sickleave)
            total_Sick_leave = int(sickleave[0])-int(sickleave[1])
            print(total_Sick_leave)
            
            
            
        for leave_halfday1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Total_HalfDay_Leave','Pending_HalfDay_Leave'):
            print(leave_halfday1)
            x_halfday = 0
            x_halfday = list(leave_halfday1)
            print(x_halfday)
            halfdayleave = [eval(i) for i in x_halfday]
            print(halfdayleave)
            total_halfday_leave = int(halfdayleave[0])-int(halfdayleave[1])
            print(total_halfday_leave)
            
            
            
        for leave_Unpaid1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Total_Unpaid_Leave','Pending_Unpaid_Leave'):
            print(leave_Unpaid1)
            x_Unpaid = 0
            x_Unpaid = list(leave_Unpaid1)
            print(x_Unpaid)
            Unpaidleave = [eval(i) for i in x_Unpaid]
            print(Unpaidleave)
            total_Unpaid_leave = int(Unpaidleave[0])-int(Unpaidleave[1])
            print(total_Unpaid_leave)
    
        
        
            
        dic ={
            'total_Paid_leave':total_Paid_leave,
            'total_Sick_leave':total_Sick_leave,
            'total_halfday_leave':total_halfday_leave,
            'total_Unpaid_leave':total_Unpaid_leave,
            'emp_reg':emp_reg,
        }
        
        return dic
    
        
    def get_context_data(self, **kwargs):
        print("h1")
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        today = str(get_date(self.request.GET.get('day', None)))
        print(today)
        today_year, today_month, today_date = (int(x) for x in today.split('-'))
        print(today_date)
        print(today_month)
        print(today_year)
        
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        cal = Calendar(d.year, d.month, today_date, today_month, today_year)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        event = Eventcal(d.year, d.month)
        html_event = event.formatmonth(withyear=True)
        context['event'] = mark_safe(html_event)
        
        context['dic']=self.dash()
        return context
    

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return date.today()


# Event add
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('adminDashboard'))
    return render(request, 'event.html', {'form': form})

def delete_event(request, event_id=None):
    instance = get_object_or_404(Event, pk=event_id)
    instance.delete()
    return redirect('adminDashboard')




def addEmployee(request):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
            admin_reg = Admin_Login.objects.get(Username=Username)
            print(admin_reg)
            
            return render(request,'addEmployee.html',{'admin_reg':admin_reg})
        
        
        if request.method == "POST":  
            form = AddemployeeForm(request.POST,request.FILES)  
            if form.is_valid():
                    Emp_ID = form.cleaned_data.get('Emp_ID')
                    Name = form.cleaned_data.get('Name')
                    User_name = form.cleaned_data.get('User_name')
                    Contact = form.cleaned_data.get('Contact')
                    Email = form.cleaned_data.get('Email')
                    Designation = form.cleaned_data.get('Designation')
                    D_O_B = form.cleaned_data.get('D_O_B')
                    Date_of_join = form.cleaned_data.get('Date_of_join')
                    Reporting_Dept = form.cleaned_data.get('Reporting_Dept')
                    Password = form.cleaned_data.get('Password')
                    Confirm_Password = form.cleaned_data.get('Confirm_Password')
                    Image = form.cleaned_data.get('Image')
                    Address = form.cleaned_data.get('Address')
                    department = form.cleaned_data.get('department')
                    # subject ="Your Account has been created" 
                    # send_mail(subject, f'Welcome Abord, your Account has been Activated \n\nUser_name:{User_name}\n\nPassword :{Password}\n\n Regards \n\n Apcosys Pvt Ltd ', 'settings.EMAIL_HOST_USER', [Email],fail_silently=False) 
                    
                    form.save()
                    messages.success(request,"Employee Registered SuccessFully")
                    return redirect('/addEmployee') 
            
        else:
            form = AddemployeeForm()  
            messages.error(request,"Employee Details is not Registered")
        return render(request,'addEmployee.html',{'form':form})
    return redirect("/employeeLogin")




def edit(request): 
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
       
            employees = Addemployee.objects.all()  
            paginator = Paginator(employees,5)

            page = request.GET.get('page')
            try:
                employees = paginator.page(page)
            except PageNotAnInteger:
                employees = paginator.page(1)
            except EmptyPage:
                employees = paginator.page(paginator.num_pages)

            return render(request, 'edit.html', {'employees': employees})
    else:    
        return redirect("/adminLogin")

def show_Emp_ID(request):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
            Emp_ID = request.POST['Emp_ID'] 
            employee = Addemployee.objects.filter(Emp_ID=Emp_ID)
            return render(request, 'edit.html',{'employees' : employee})
    else:    
        return redirect("/adminLogin")
   
        

def editEmployee(request,id):

    employee = Addemployee.objects.get(id=id)  
    return render(request,'editEmployee.html', {'employee':employee}) 
    # return render(request,"editEmployee.html")

def update(request, id):  
   
    employee = Addemployee.objects.get(id=id)  
    if len(employee.Image) > 0:
        os.remove(employee.Image.path)
        
    form = AddemployeeForm(request.POST,request.FILES, instance = employee)  
    if form.is_valid(): 
        form.save()  
        return redirect("/edit")  
    else:
        print(form.errors) 
    return render(request, 'editEmployee.html', {'employee': employee})  


def employees(request):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
            admin_reg = Admin_Login.objects.get(Username=Username)
            print(admin_reg)
            
            return render(request,'employees.html',{'admin_reg':admin_reg})
    else:    
        return redirect("/adminLogin")



def leaveApplicationDetails(request):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
        
            
            leaves = Leave_App.objects.raw("""SELECT leave."id",leave."Category",leave."From",leave."to",leave."leavedayCategory_From",leave."leavedayCategory_to",leave."Reason",leave."Emp_ID", add_Employee."Name",add_Employee."department" FROM leave INNER JOIN add_Employee ON leave."Emp_ID" = add_Employee."Emp_ID" where leave."leave_status" = 0 or  leave."leave_status" = 1 or leave."leave_status" = 2 ORDER BY leave."leave_status" ASC  """)
            paginator = Paginator(leaves,5)
            page = request.GET.get('page')
            try:
                leaves = paginator.page(page)
            except PageNotAnInteger:
                leaves = paginator.page(1)
            except EmptyPage:
                leaves = paginator.page(paginator.num_pages)


            return render(request,'leaveApplicationDetails.html',{'leaves':leaves,'Username':Username})
    else:    
        return redirect("/adminLogin")


def removeEmployees(request):
    employees = Addemployee.objects.all()  
    paginator = Paginator(employees,5)

    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
        
    return render(request,"removeEmployees.html",{'employees':employees})

def remove_Emp_ID(request):
    Emp_ID = request.POST['Emp_ID']
    employee = Addemployee.objects.filter(Emp_ID=Emp_ID)
    return render(request, 'removeEmployees.html',{'employees' : employee})

def destroy(request, id):
          
    employee = Addemployee.objects.get(id=id)  
    if len(employee.Image) > 0:
        os.remove(employee.Image.path)
    employee.delete()  
    return redirect("/removeEmployees") 



def reviewLeaveApplication(request,Emp_ID,id):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Username = request.session['Username']
            
            dic = {
                'Emp_ID' : Emp_ID,
                'id':id
            }
            leaves = Leave_App.objects.raw("""SELECT leave."id",leave."Category",leave."From",leave."to",leave."leavedayCategory_From",leave."leavedayCategory_to",leave."Reason",leave."Emp_ID", add_Employee."Name",add_Employee."Contact",add_Employee."Address",add_Employee."D_O_B",add_Employee."Date_of_join",add_Employee."department",add_Employee."Designation",add_Employee."Reporting_Dept",add_Employee."Email",add_Employee."User_name",add_Employee."Password",add_Employee."Confirm_Password",add_Employee."Emp_ID",add_Employee."Image" FROM leave INNER JOIN add_Employee ON leave."Emp_ID" = add_Employee."Emp_ID" where leave."Emp_ID" = %(Emp_ID)s and leave."id" = %(id)s """, dic)

           
            return render(request,'reviewLeaveApplication.html',{'leaves':leaves})
    else:    
        return redirect("/adminLogin")


def Approve_leave(request,Emp_ID,id):
    
    leave=Leave_App.objects.get(Emp_ID=Emp_ID,id=id)
    leave.leave_status=1
    leave.save()


    for leave_Paid1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Pending_Paid_Leave','Pending_Sick_Leave','Pending_HalfDay_Leave','Pending_Unpaid_Leave'):
        print(leave_Paid1)
        
        leave_Paid2 = list(leave_Paid1)
        pending_leave_Paid = [eval(i) for i in leave_Paid2]
        print(pending_leave_Paid)
        
      
    for Paid_leave_days in Leave_App.objects.all().filter(Emp_ID=Emp_ID,id=id,Category='Paid Leave').values_list('Leave_count_Category'):
        # print(Paid_leave_days)
        Paid_leave1 = list(Paid_leave_days)
        # print(Paid_leave1)  
        Paidleave_list = [eval(i) for i in Paid_leave1]
        # print("Modified list is: ", res)

        total = 0
        for val in Paidleave_list:
            total = total + val

        # print(total)

        zipped_lists = zip(pending_leave_Paid, Paidleave_list)

        sum = [x - y for (x, y) in zipped_lists]
        pending_Paid_Leave = sum[0]
        print(pending_Paid_Leave)
        
        
        Paid_leave = Addemployee.objects.get(Emp_ID=Emp_ID)
        Paid_leave.Pending_Paid_Leave= pending_Paid_Leave
        Paid_leave.save()
        print(Paid_leave)

# # ===============sick leave ===============================


 
    for leave_sick1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Pending_Sick_Leave'):
        print(leave_sick1)
        
        leave_sick2 = list(leave_sick1)
        pending_leave_sick = [eval(i) for i in leave_sick2]
        print(pending_leave_sick)
        
      
    for sick_leave_days in Leave_App.objects.all().filter(Emp_ID=Emp_ID,id=id,Category='Sick Leave').values_list('Leave_count_Category'):
        # print(Paid_leave_days)
        sick_leave1 = list(sick_leave_days)
        # print(Paid_leave1)  
        sickleave_list = [eval(i) for i in sick_leave1]
        # print("Modified list is: ", res)

        total = 0
        for val in sickleave_list:
            total = total + val

        # print(total)

        zipped_lists = zip(pending_leave_sick, sickleave_list)

        sum = [x - y for (x, y) in zipped_lists]
        pending_sick_Leave = sum[0]
        print(pending_sick_Leave)
        
        
        sick_leave = Addemployee.objects.get(Emp_ID=Emp_ID)
        sick_leave.Pending_Sick_Leave= pending_sick_Leave
        sick_leave.save()
        print(sick_leave)
        
# ================================================= HalfDay_Leave ==============================================
        
    for leave_HalfDay1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Pending_HalfDay_Leave'):
        print(leave_HalfDay1)
        
        leave_HalfDay2 = list(leave_HalfDay1)
        pending_leave_HalfDay = [eval(i) for i in leave_HalfDay2]
        print(pending_leave_HalfDay)
        
      
    for HalfDay_leave_days in Leave_App.objects.all().filter(Emp_ID=Emp_ID,id=id,Category='Half DayLeave').values_list('Leave_count_Category'):
        # print(Paid_leave_days)
        HalfDay_leave1 = list(HalfDay_leave_days)
        # print(Paid_leave1)  
        HalfDayleave_list = [eval(i) for i in HalfDay_leave1]
        # print("Modified list is: ", res)

        total = 0
        for val in HalfDayleave_list:
            total = total + val

        # print(total)

        zipped_lists = zip(pending_leave_HalfDay, HalfDayleave_list)

        sum = [x - y for (x, y) in zipped_lists]
        pending_HalfDay_Leave = sum[0]
        print(pending_HalfDay_Leave)
        
        
        HalfDay_leave = Addemployee.objects.get(Emp_ID=Emp_ID)
        HalfDay_leave.Pending_HalfDay_Leave= pending_HalfDay_Leave
        HalfDay_leave.save()
        print(HalfDay_leave)


# ================================================= HalfDay_Leave ==============================================
        
    for leave_Unpaid1 in  Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('Pending_Unpaid_Leave'):
        print(leave_Unpaid1)
        
        leave_Unpaid2 = list(leave_Unpaid1)
        pending_leave_Unpaid = [eval(i) for i in leave_Unpaid2]
        print(pending_leave_Unpaid)
        
      
    for Unpaid_leave_days in Leave_App.objects.all().filter(Emp_ID=Emp_ID,id=id,Category='Unpaid Leave').values_list('Leave_count_Category'):
        # print(Paid_leave_days)
        Unpaid_leave1 = list(Unpaid_leave_days)
        # print(Paid_leave1)  
        Unpaidleave_list = [eval(i) for i in Unpaid_leave1]
        # print("Modified list is: ", res)

        total = 0
        for val in Unpaidleave_list:
            total = total + val

        # print(total)

        zipped_lists = zip(pending_leave_Unpaid, Unpaidleave_list)

        sum = [x - y for (x, y) in zipped_lists]
        pending_Unpaid_Leave = sum[0]
        print(pending_Unpaid_Leave)
        
        
        Unpaid_leave = Addemployee.objects.get(Emp_ID=Emp_ID)
        Unpaid_leave.Pending_Unpaid_Leave= pending_Unpaid_Leave
        Unpaid_leave.save()
        print(Unpaid_leave)
    
    return redirect("/leaveApplicationDetails")
    
        


    

def Reject_leave(request,Emp_ID,id):
    comments = request.POST.get('comments')
    print(comments)
    leave=Leave_App.objects.get(Emp_ID=Emp_ID,id=id)
    leave.leave_status=2
    leave.comments = comments
    leave.save()

    return redirect("/leaveApplicationDetails")
            

def deactive_emp(request,Emp_ID,id):
    emp=Addemployee.objects.get(Emp_ID=Emp_ID,id=id)
    emp.Emp_status=1
    emp.save()

    return redirect("/removeEmployees")


def active_emp(request,Emp_ID,id):
    emp=Addemployee.objects.get(Emp_ID=Emp_ID,id=id)
    emp.Emp_status=0
    emp.save()
    return redirect("/removeEmployees")


def adminlogout(request):
    try:
      del request.session['Username']
    except:
        return redirect("/adminLogin")
    return redirect("/adminLogin")


#=============================================================================================








def employeeLogin(request):
    if request.method == 'POST':
        form = AddemployeeForm(request.POST)  
        User_name = request.POST['User_name']
        Password = request.POST['Password']
         
        try:
            emp = Addemployee.objects.get(User_name = User_name,Password=Password)
            print(emp.Emp_status)
            request.session['User_name'] = User_name
            
            
            for employee in Addemployee.objects.all().filter(User_name=User_name).values_list('id','Name','Emp_ID','Image'):
                request.session['id'] = employee[0]
                request.session['Name'] = employee[1]
                request.session['Emp_ID'] = employee[2]
                request.session['Image'] = employee[3]
                
                # print(employee[0],employee[1],employee[2])

                if emp.Emp_status != 1:
                    return redirect('/sidebar')                                           
                else:
                    messages.error(request,"Your Account is Deactivate")
                    return render(request,"employeeLogin.html")

        except Addemployee.DoesNotExist:
            emp = None


        if emp is not None:
            return redirect('/sidebar')                                           
        else:
            messages.error(request,"Invalid Username or Password")
            return render(request,"employeeLogin.html")

    return render(request,"employeeLogin.html")







def profileSetting(request):
    if request.session.has_key('Name'):
        if request.method == 'GET':
            Name = request.session['Name']
            emp_reg = Addemployee.objects.get(Name=Name)
            print(emp_reg)
            
            return render(request,'profileSetting.html',{'emp_reg':emp_reg,'Name':Name})        
    return redirect("/employeeLogin")


def leaveSection(request):
    if request.session.has_key('Name'):
        if request.method == 'GET':
            Name = request.session['Name']
            emp_reg = Addemployee.objects.get(Name=Name)
            # print(emp_reg)
            leave = Leave_Policy.objects.all()
            print(leave)
            
            return render(request,'leaveSection.html',{'emp_reg':emp_reg,'Name':Name,'leave':leave})        
    return redirect("/employeeLogin")

def leaveApplication(request):
    if request.session.has_key('Name'):
        Name = request.session['Name']
        
        emp_reg = Addemployee.objects.get(Name=Name)
        print(emp_reg.Pending_Sick_Leave)
                
        current_date = datetime.now().strftime('%m %d %Y')
        print(current_date)      
        if request.method == "POST": 
            
            form = Leave_AppForm(request.POST)  
            
            # if emp_reg.Pending_Sick_Leave > "0" or emp_reg.Pending_Paid_Leave > "0" :  
                
            if form.is_valid():
                print(form)
                Date = form.cleaned_data.get('Date')
                Category = form.cleaned_data.get('Category') 
                From = form.cleaned_data.get('From')
                to = form.cleaned_data.get('to')
                leavedayCategory_From = form.cleaned_data.get('leavedayCategory_From')
                leavedayCategory_to = form.cleaned_data.get('leavedayCategory_to')
                Reason = form.cleaned_data.get('Reason')
                Emp_ID = form.cleaned_data.get('Emp_ID')
                department = form.cleaned_data.get('department')
                Name = form.cleaned_data.get('Name')
                Designation = form.cleaned_data.get('Designation')
                Leave_count_Category = form.cleaned_data.get('Leave_count_Category')
                
                    
                try:  
                    form.save()  
                    return redirect('/approvalStatus')  
                
                except:  
                    print(form.errors)
                    pass 
            
                # else:
                
                #     print("cant apply this leave")
        else:
                
            form = Leave_AppForm()  
            print("cant apply this leave")
            
        con ={
            'form':form,
            'Name':Name,
            'emp_reg':emp_reg,
            'current_date':current_date,
        }
        return render(request,'leaveApplication.html',con)

        

def leavePolicy(request):
    if request.session.has_key('Name'):
        if request.method == 'GET':
            Name = request.session['Name']
            
            emp_reg = Addemployee.objects.get(Name=Name)
            print(emp_reg)
            
            Username = request.session['Username']
    
            try:
                leave = Leave_Policy.objects.get(Username=Username)
            except Leave_Policy.DoesNotExist:
                leave = None
            print(leave)
            
            
            return render(request,'leavePolicy.html',{'emp_reg':emp_reg,'Name':Name,'leave':leave})        
    return redirect("/employeeLogin")



def howToUse(request):
    if request.session.has_key('Name'):
            Name = request.session['Name']
            Emp_ID = request.session['Emp_ID']
            emp_reg = Addemployee.objects.get(Name=Name,Emp_ID=Emp_ID)
            print(emp_reg)
            return render(request,"howToUse.html",{'emp_reg' : emp_reg})
    else:
    
        return redirect("/employeeLogin")

def leaveBasket(request): 
  
    if request.session.has_key('Name'):
            Name = request.session['Name']
            Emp_ID = request.session['Emp_ID']
            emp_reg = Addemployee.objects.get(Name=Name,Emp_ID=Emp_ID)
            print(emp_reg)
            return render(request, 'leaveBasket.html',{'emp_reg' : emp_reg})   

    else:
    
        return redirect("/employeeLogin")
    
    
def approvalStatus(request):
    if request.session.has_key('Name'):
        if request.method == 'GET':
            Name = request.session['Name']
            Emp_ID = request.session['Emp_ID']
            for employee in Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('department','Image'):
                
                department = employee[0]
                
            emp_reg = Addemployee.objects.get(Name=Name,Emp_ID=Emp_ID)
            print(emp_reg)
            
            leave = Leave_App.objects.filter(Emp_ID=Emp_ID).order_by('leave_status').values()
            print(leave)

            paginator = Paginator(leave,5)
            page = request.GET.get('page')
            try:
                leave = paginator.page(page)
            except PageNotAnInteger:
                leave = paginator.page(1)
            except EmptyPage:
                leave = paginator.page(paginator.num_pages)
           
            con = {
                'leaves':leave,
                'Name':Name,
                'Emp_ID':Emp_ID,
                'department':department,
                'emp_reg':emp_reg,
                
            }
            
            return render(request,'approvalStatus.html',con)
    
    return redirect("/employeeLogin")


def reviewEmployeeApplication(request,Emp_ID,id):
    if request.session.has_key('Username'):
        if request.method == 'GET':
            Name = request.session['Name']
            
            emp_reg = Addemployee.objects.get(Name=Name,Emp_ID=Emp_ID)
            print(emp_reg)
            
            dic = {
                'Emp_ID' : Emp_ID,
                'id':id,
                
            }
            leaves = Leave_App.objects.raw("""SELECT leave."id",leave."Category",leave."From",leave."to",leave."leavedayCategory_From",leave."leavedayCategory_to",leave."Reason",leave."Emp_ID", add_Employee."Name",add_Employee."Contact",add_Employee."Address",add_Employee."D_O_B",add_Employee."Date_of_join",add_Employee."department",add_Employee."Designation",add_Employee."Reporting_Dept",add_Employee."Email",add_Employee."User_name",add_Employee."Password",add_Employee."Confirm_Password",add_Employee."Emp_ID",add_Employee."Image" FROM leave INNER JOIN add_Employee ON leave."Emp_ID" = add_Employee."Emp_ID" where leave."Emp_ID" = %(Emp_ID)s and leave."id" = %(id)s """, dic)

           
            # cursor = connection.cursor()    
            # cursor.execute("""SELECT leave."id",leave."Category",leave."From",leave."to",leave."leavedayCategory_From",leave."leavedayCategory_to",leave."Reason",leave."Emp_ID", add_Employee."Name",add_Employee."Contact",add_Employee."Address",add_Employee."D_O_B",add_Employee."Date_of_join",add_Employee."department",add_Employee."Designation",add_Employee."Reporting_Dept",add_Employee."Email",add_Employee."User_name",add_Employee."Password",add_Employee."Confirm_Password",add_Employee."Emp_ID",add_Employee."Image" FROM leave INNER JOIN add_Employee ON leave."Emp_ID" = add_Employee."Emp_ID"  """ )
            # row = cursor.fetchall()
            # print(row)
           
            return render(request,'reviewEmployeeApplication.html',{'leaves':leaves,'emp_reg':emp_reg})
        
    return redirect("/employeeLogin")
 
    # if request.session.has_key('Name'):
    #     if request.method == 'GET':
    #         Name = request.session['Name']
    #         Emp_ID = request.session['Emp_ID']
    #         for employee in Addemployee.objects.all().filter(Emp_ID=Emp_ID).values_list('department'):
    
    #              department = employee[0]
    #              print(department)
    #         for leave in Leave_App.objects.all().filter(Emp_ID=Emp_ID).values_list('Category','From','to','leavedayCategory_From','leavedayCategory_to','Reason','Emp_ID','Leave_count_Category'):
    #             From = leave[1]
    #             to = leave[2]
    #             print(From,to)
    #             print(leave)
    #         # leave = Leave_App.objects.get(Emp_ID=Emp_ID)
    #         # print(leave)
    #         From_date = str(From)
    #         From_date = datetime.strptime(From_date, '%Y-%m-%d')
    #         From_date = From_date.strftime("%d")
            
    #         # # print(From_date)

    #         to_date = str(to)
    #         to_date = datetime.strptime(to_date, '%Y-%m-%d')
    #         to_date = to_date.strftime("%d")
            
    #         # # print(to_date) 

    #         date = int(to_date) - int(From_date)
    #         # print(date)
        
    #         con = {
    #             'leave':leave,
    #             'Name':Name,                            
    #             'From' : From,
    #             'Emp_ID':Emp_ID,
    #             'department':department,
    #             'date':date,
                
    #         }
            
    #         return render(request,'approvalStatus.html',con)
    
    # return render(request,'approvalStatus.html')

def employeelogout(request):
    try:
      del request.session['Name']
    except:
        return redirect("/employeeLogin")
    return redirect("/employeeLogin")



