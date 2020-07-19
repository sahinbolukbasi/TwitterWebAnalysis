from django import forms  
from firstApp.models import Analysis  ,Contact
  
class EmpForm(forms.ModelForm):  
    class Meta:  
        model = Contact  
        fields = [
            'konu',
            'mesaj',
        ] 
        
class AnlysForm(forms.ModelForm):  
    class Meta:  
        model = Analysis  
        fields = [
            'Aad',
            'Akonu',
            'Ahastag',
            'Amesaj',          
            'baslangictarihi',
            'bitistarihi',
        ] 