from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# form to create new users(user-signup)
class SignupForm(UserCreationForm):

    class Meta:
        fields = ("username","email","password1","password2")
        model = get_user_model()
        
    def __init__(self,*args,**kwargs):          #changes the default label in form for the fields
        super().__init__(*args,**kwargs)
        self.fields["username"].label = "Display Name"