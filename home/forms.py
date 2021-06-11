import random
from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import FieldWithButtons
from .models import Title


placeholders = [
    'Тут мог бы быть ваш заголовок...',
    'Введите черновое название публикации',
    'Предварительное название статьи...'
]

class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'title-text', 
                'required': True, 
                'placeholder': random.choice(placeholders)
            })
        }
        error_messages = {
            'text': {
                'required': _("Введите текст заголовка"),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            FieldWithButtons('text',
                ButtonHolder(Submit('submit', 'Проверить ↵')))
            )
