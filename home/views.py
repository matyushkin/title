import random
from django.shortcuts import render, get_object_or_404
from .models import Title
from .forms import TitleForm
from ml.nlp_model.corr_model import text_to_suggestion


def main_page(request):
    if request.method == 'POST':
        form = TitleForm(request.POST)
        new_form = form.save(commit=False)
        s = text_to_suggestion(new_form.text)
        new_form.value = s['rating']
        new_form.group_id = random.randint(1, 10)
        new_form.save()
        title_form = TitleForm()
    else:
        s = None
        title_form = TitleForm()
    return render(request, 'pages/home.html', {"title_form": title_form, "s": s})
