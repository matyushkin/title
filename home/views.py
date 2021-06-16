import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Title
from .forms import TitleForm

from ml.nlp_model.corr_model import text_to_suggestion


def home(request):
    title_form = TitleForm()
    return render(request, 'pages/home.html', {"title_form": title_form})



@csrf_exempt
def create_title(request):
    if request.method == 'POST':
        title_text = request.POST.get('text')
        group_id = request.POST.get('group_id')

        response_data = text_to_suggestion(title_text)

        post = Title(text=title_text,
            value=response_data['rating'],
            # group_id используется для простейшей группировки
            # текущих запросов - минимальная идентификация
            group_id = group_id)
        post.save()


        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def about(request):
    titles_count = Title.objects.all().count()
    context = {'titles_count': titles_count}
    return render(request, 'pages/about.html', context)
