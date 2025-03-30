from django import forms
from gestion.models  import CustomUser

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
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
