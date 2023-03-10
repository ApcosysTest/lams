from django.db import models
from django.urls import reverse

class Admin_Login(models.Model):
    Username = models.CharField(max_length=20)
    Password = models.CharField(max_length=20) 
    
    class Meta:  
        # managed = False
        db_table = "admin_Login"
        
# Create your models here.

class CompanySetup(models.Model):
    Username = models.CharField(max_length=20,blank = True,null=True)
    company_name = models.CharField(max_length=500,blank = True,null=True)
    email = models.EmailField(max_length=500,blank=True,unique=True) 
    website = models.CharField(max_length=500,blank = True,null=True)
    telephone = models.CharField(max_length=500,blank=True,null=True)
    telephone1 = models.CharField(max_length=500,blank=True,null=True)
    telephone2 = models.CharField(max_length=500,blank=True,null=True)
    Address = models.CharField(max_length=500,blank = True,null=True)
    zip = models.CharField(max_length=500,blank = True,null=True)
    city = models.CharField(max_length=500,blank = True,null=True)
    state = models.CharField(max_length=500,blank = True,null=True)
    country = models.CharField(max_length=500,blank = True,null=True)
    companyBranch = models.CharField(max_length=500,blank = True,null=True)
    department1 = models.CharField(max_length=500,blank = True,null=True)
    department2 = models.CharField(max_length=500,blank = True,null=True)
    department3 = models.CharField(max_length=500,blank = True,null=True)
    department4 = models.CharField(max_length=500,blank = True,null=True)
    department5 = models.CharField(max_length=500,blank = True,null=True)
    company_status = models.IntegerField(default=1,blank=True,null=True)
    
    class Meta:
        db_table = 'company_setup'
        
class Addemployee(models.Model):
    Name = models.CharField(max_length=200)
    Contact = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    D_O_B = models.DateField(blank = True,null=True)
    Date_of_join = models.DateField(blank = True,null=True)
    department = models.CharField(max_length=200)
    Designation = models.CharField(max_length=200)
    Reporting_Dept = models.CharField(max_length=200)
    Email = models.EmailField(max_length=70,blank=True,unique=True) 
    User_name = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)
    Confirm_Password = models.CharField(max_length=200)
    Emp_ID = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='images/')
    Emp_status = models.IntegerField(default=0,blank = True,null=True)
    
        
    Total_Paid_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Total_Sick_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Total_HalfDay_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Total_Unpaid_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    
    Pending_Paid_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Pending_Sick_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Pending_HalfDay_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    Pending_Unpaid_Leave = models.CharField(max_length=10,default="15",blank = True,null=True)
    
    class Meta:  
        db_table = "add_employee" 
         
    @staticmethod
    def get_customer_by_email(User_name):
        try:
            return Addemployee.objects.get(User_name=User_name)
        except:
            return False

    def isExists(self):
        if Addemployee.objects.filter(User_name = self.User_name):
            return True

        return  False

     
        
class Leave_App(models.Model):
    Date = models.DateField(auto_now=True,blank = True,null=True)
    Name = models.CharField(max_length=200,blank = True,null=True)
    Category = models.CharField(max_length=200,blank = True,null=True)          
    From = models.CharField(max_length=200,blank = True,null=True) 
    to = models.CharField(max_length=200,blank = True,null=True)
    leavedayCategory_From = models.CharField(max_length=200,blank = True,null=True)  
    leavedayCategory_to = models.CharField(max_length=200,blank = True,null=True)  
    Reason = models.CharField(max_length=250,blank = True,null=True)
    Emp_ID = models.CharField(max_length=200,blank = True,null=True) 
    Leave_count_Category = models.CharField(max_length=2,blank = True,null=True) 
    leave_status = models.IntegerField(default=0,blank = True,null=True)
    department = models.CharField(max_length=200,blank = True,null=True)
    Designation = models.CharField(max_length=200,blank = True,null=True)
    comments = models.CharField(max_length=500,blank = True,null=True)
    # Absentemp_status = models.IntegerField(default=1,blank = True,null=True) 
    

    
    
    
    class Meta:  
        db_table = "leave"  



class Leave_Policy(models.Model):
    Username = models.CharField(max_length=20,blank = True,null=True)
    leavepolicy = models.CharField(max_length=50000)
    paidleave =  models.IntegerField(default=00,blank = True,null=True)   
    unpaidleave =  models.IntegerField(default=00,blank = True,null=True)   
    medicalleave =  models.IntegerField(default=00,blank = True,null=True) 
    deputation =    models.IntegerField(default=00,blank = True,null=True)
    compleave =  models.IntegerField(default=00,blank = True,null=True)   
    otherleave =  models.IntegerField(default=00,blank = True,null=True)   
    leave_status =  models.IntegerField(default=1,blank = True,null=True)   
    
    class Meta:  
        db_table = "leavepolicy"  
        
        
class Absent_emp(models.Model):
    Date = models.DateField(auto_now=True)
    Name = models.CharField(max_length=200) 
    Emp_ID = models.CharField(max_length=200,blank = True,null=True)          
    department = models.CharField(max_length=200)
    Designation = models.CharField(max_length=200)
      
    class Meta:  
        db_table = "absent_emp"
        
class Event(models.Model):
    CATEGORY_CHOICES = [ ('Birthday', 'Birthday'), ('Public Holiday', 'Public Holiday'), ('Event', 'Event'), ('Others', 'Others'),]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()
    @property
    def get_event_description(self):
          
        des =Event.objects.get(id = self.id,description = self.description) 
        try:
            des =Event.objects.get(id = self.id,description = self.description)
            return des.description
        except:
            return False
     
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> <span class ="options" style="  margin-top:1px;color:#707070;  " > <img class="img1"style="width:20px; height:20px;" src="../static/assets/img/edit.png" alt="edit"/> </span></a><br> '
    @property
    def deleteEvent(self):  
        urls = reverse('event_delete', args=(self.id,))
        return f'<br><a href="{urls}"> <span class ="options"id = "options"  > <img class="img2"style="width:20px; margin-top:10px;color:#707070;"src="../static/assets/img/delete.png" alt="delete"/> </span></a>'
        # return f'<br><button id="primaryButton{cot}" href="{urls}" ></button>' 
        # return f'<br> <a data-bs-toggle="modal" data-bs-target="#sureModal"> <span class ="options" style="  margin-top:20px;color:#707070;" > <img class="img2"style="width:20px; margin-top:10px;color:#707070;"src="../static/assets/img/delete.png" alt="delete"/> </span></a><div class="modal fade" id="sureModal" tabindex="-1" aria-labelledby="sureModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"><h5 class="modal-title" id="sureModalLabel">Are you Sure?</h5></div> <div class="modal-footer"><button type="button" style="background-color:red;" class="btn btn-danger" data-bs-dismiss="modal">No</button><a href="{urls}" class="btn btn-primary">Yes</a></div></div></div></div>'
        # return f'<br><button hidden id="primaryButton" href="{urls}"></button><a data-bs-toggle="modal" data-bs-target="#sureModal"> <span class ="options" style="  margin-top:20px;color:#707070;" > <img class="img2"style="width:20px; margin-top:10px;color:#707070;"src="../static/assets/img/delete.png" alt="delete"/> </span></a><div class="modal fade" id="sureModal" tabindex="-1" aria-labelledby="sureModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"><h5 class="modal-title" id="sureModalLabel">Are you Sure?</h5></div> <div class="modal-footer"><button type="button" style="background-color:red;" class="btn btn-danger" data-bs-dismiss="modal">No</button><button type="button" id='"secondaryButton"' class="btn btn-primary" onclick="document.getElementById("primaryButton").click()">Yes</button></div></div></div></div>'
    


        