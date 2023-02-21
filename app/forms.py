from django import forms  
from .models import Addemployee , Event , CompanySetup , Absent_emp , Leave_Policy
from django.forms import ModelForm, DateInput

class DateInput(forms.DateInput):
    input_type = 'date'
    
     
class AddemployeeForm(forms.ModelForm):  
    class Meta:  
        model = Addemployee  
        fields = "__all__"  
        
    widgets = {
            'D_O_B': DateInput(),
            'Date_of_join': DateInput(), 
        } 
    
from .models import CompanySetup 

class CompanySetupForm(forms.ModelForm):  
    class Meta:  
        model = CompanySetup  
        fields = "__all__"
        

from .models import Leave_Policy 

class Leave_PolicyForm(forms.ModelForm):  
    class Meta:  
        model = Leave_Policy  
        fields = "__all__"
        
               
from .models import Absent_emp 
        
class Absent_empForm(forms.ModelForm):  
    class Meta:  
        model = Absent_emp  
        fields = "__all__"
    
from .models import Admin_Login 

class Admin_LoginForm(forms.ModelForm):  
    class Meta:  
        model = Admin_Login  
        fields = "__all__"
        
        
from .models import Leave_App 

class DateInput(forms.DateInput):
    input_type = 'date'
    
     
class Leave_AppForm(forms.ModelForm):  
    class Meta:  
        model = Leave_App  
        fields = "__all__" 
     
        
    widgets = {
            'Date':DateInput(),
            'From': DateInput(),
            'to': DateInput(), 
        } 



class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'date': DateInput(format='%Y-%m-%d'),
    }
    fields = '__all__'    