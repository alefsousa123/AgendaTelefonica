from django import forms
from django.core.exceptions import ValidationError
from contact.models import Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from .models import Familia, Rua, GrupoFamilias, GrupoPreJovens, AulaCrianca, CirculoEstudo
from .widgets import ParticipanteWidget
from dal import autocomplete
from .utils import contatos_do_usuario



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'familia', 'birth_date', 'description', 'rua']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['familia'].queryset = Familia.objects.filter(owner=user)
            self.fields['rua'].queryset = Rua.objects.filter(owner=user)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError("First name is required.", code='required')
        return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. 30 characters or fewer.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. 30 characters or fewer.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User 
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.", code='required')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.", code='unique')
        return email   


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. 30 characters or fewer.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. 30 characters or fewer.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=254,
        required=False,  # Alterado para False
        help_text='Garanta que seja um email válido.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', }),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', }),
        help_text='Enter the same password as above, for verification.',
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        # Permite campo vazio se já houver email registrado
        if not email and current_email:
            return current_email

        # if not email:
        #     raise ValidationError("Email is required.", code='required')

        if current_email != email:
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email already exists.", code='unique')
        return email

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()
        
        return user
       
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            self.add_error('password2', ValidationError('Passwords do not match.'))

        return super().clean()

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as e:
                self.add_error(
                    'password1',
                    ValidationError(e)
                )
        return password1


class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        fields = ('nome', 'rua', 'endereco', 'reuniao_devocional', 'data_ultima_reuniao', 'nivel_envolvimento', 'description', )
          # ou especifique os campos desejados

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['rua'].queryset = Rua.objects.filter(owner=user)


class RuaForm(forms.ModelForm):
    class Meta:
        model = Rua
        fields = ('nome', 'bairro', 'description')  # Adicionado 'description'



class GrupoPreJovensForm(forms.ModelForm):
    class Meta:
        model = GrupoPreJovens
        fields = ('nome', 'rua', 'livro', 'licoes', 'description', 'pre_jovens', 'animador', 'data_ultimo_encontro', 'dia_semana')
        widgets = {
            'pre_jovens': forms.CheckboxSelectMultiple,
            # Remova esta linha:
            # 'rua': forms.CheckboxSelectMultiple,
            # 'animador': forms.RadioSelect,  # Opcional, se quiser radio no form
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['pre_jovens'].queryset = Contact.objects.filter(owner=user)
            self.fields['animador'].queryset = Contact.objects.filter(owner=user)
            self.fields['rua'].queryset = Rua.objects.filter(owner=user)

class AulaCriancaForm(forms.ModelForm):
    class Meta:
        model = AulaCrianca
        fields = ('nome', 'rua', 'participantes', 'serie', 'licao', 'dia_semana', 'data_ultima_aula', 'description', 'professor')
        widgets = {
            'participantes': forms.CheckboxSelectMultiple,
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['rua'].queryset = Rua.objects.filter(owner=user)
            self.fields['participantes'].queryset = Contact.objects.filter(owner=user)
            self.fields['professor'].queryset = Contact.objects.filter(owner=user)


class GrupoFamiliasForm(forms.ModelForm):
    class Meta:
        model = GrupoFamilias
        fields = ('nome', 'participantes', 'familias', 'ruas', 'description', 'data_ultima_reuniao_reflexao')
        widgets = {
            'participantes': forms.CheckboxSelectMultiple,
            'familias': forms.CheckboxSelectMultiple,
            'ruas': forms.CheckboxSelectMultiple,
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['participantes'].queryset = Contact.objects.filter(owner=user)
            self.fields['familias'].queryset = Familia.objects.filter(owner=user)
            self.fields['ruas'].queryset = Rua.objects.filter(owner=user)

class CirculoEstudoForm(forms.ModelForm):
    class Meta:
        model = CirculoEstudo
        fields = (
            'nome', 'tutor', 'participantes', 'dia_semana', 'data_ultimo_encontro',
            'livro', 'unidade', 'secao', 'description', 'rua'
        )
        widgets = {
            'participantes': forms.CheckboxSelectMultiple,
            # NÃO defina 'rua' aqui, pois você renderiza manualmente
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['tutor'].queryset = Contact.objects.filter(owner=user)
            self.fields['participantes'].queryset = Contact.objects.filter(owner=user)
            self.fields['rua'].queryset = Rua.objects.filter(owner=user)

    def clean(self):
        cleaned = super().clean()
        # Força a limpeza do campo rua
        cleaned['rua'] = self.clean_rua()
        return cleaned

    def clean_rua(self):
        data = self.data.getlist('rua')
        if not data:
            return None
        if len(data) > 1:
            raise ValidationError("Selecione apenas uma rua.")
        try:
            return Rua.objects.get(pk=data[0])
        except Rua.DoesNotExist:
            raise ValidationError("Rua inválida.")
