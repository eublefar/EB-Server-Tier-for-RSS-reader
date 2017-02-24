from django.http import HttpResponse
from .models import Article, Source, Event, Category, User_source
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
import datetime
import ast
from django.views.decorators.csrf import csrf_exempt
import boto3

session = boto3.Session(region_name='eu-central-1', aws_access_key_id='key_id', aws_secret_access_key='secret_key')
sqs = session.resource('sqs')
worker_queue = sqs.get_queue_by_name(QueueName='worker_queue_name')

def index(request):
    latest_article_list = Article.objects.order_by('-pub_date')[:5]
    output = ', '.join([a.article_name for a in latest_article_list])
    return HttpResponse(output)


@login_required
def articleDetail(request, page):
    sources = User_source.objects.filter(user = request.user.id)

    articles = Article.objects.filter(source_id__in=[source.source_id for source in sources])

    paginator = Paginator(articles,15)
    result_dict = {'articles':[model_to_dict(article) for article in paginator.page(page)]}

    return JsonResponse(result_dict)

@csrf_exempt
@login_required
def sourceDetail(request):
    if request.method == 'POST':
        source_address = request.POST['source_address']
        source_name = request.POST['source_name']
        source = Source.objects.filter(source_address=source_address)
        if len(source)==0:
            new_source = Source.objects.create(source_name=source_name, source_address=source_address,is_public = False, modified=None)
            new_source.save()
            source = [new_source,]
            worker_queue.send_message(Entries={'feed':source_address})
        User_source.objects.create(user = request.user, source=source[0]).save()
        return HttpResponse(status=200)
    elif request.method == 'DELETE':
        qdict = QueryDict(request.body)

        delete = ast.literal_eval(qdict.keys()[0])
        source_address = delete['source_address']
        print('\n' + source_address)
        source = Source.objects.filter(source_address=source_address)
        if len(source)==0:
            return HttpResponse(status=204)
        relation = User_source.objects.filter(user=request.user, source=source[0])
        if len(relation)==0:
            return HttpResponse(status=204)
        relation[0].delete()
        if len(User_source.objects.filter(source=source[0]))==0:
            source[0].delete()
        return HttpResponse(status=200)
    else:
        s = User_source.objects.filter(user_id=request.user.id)
        sources = Source.objects.filter(id__in=[u_s_relation.source_id for u_s_relation in s])
        if(len(sources) != 0):
            return JsonResponse({'sources':[model_to_dict(source) for source in sources]})
        else:
            return HttpResponse(status=204)
