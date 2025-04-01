from django import forms
from gestion.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(label="Confirmar Contraseña",widget=forms.PasswordInput)
    class Meta:
        model= CustomUser
        fields=[
            'nombre',
            'correo',
            'username',
        ]
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Encripta la contraseña
        if commit:
            user.save()
        return user
class CustomAuthenticationForm(AuthenticationForm):
    pass
   # class Meta:
      #  model = CustomUser  # O tu modelo de usuario
      #  fields = ['username', 'password']

    
