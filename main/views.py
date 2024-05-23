# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, TranslateArticle
from .deepl import translate, checkStatus, writeToFile
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.core.files.base import ContentFile
import time
import json
import uuid
import os
from io import BytesIO

def page(request):
    all_files = Article.objects.all()

    context = {
        'all_files' : all_files
    }

    if request.method == 'POST':
        file_name = request.POST.get("file_name")
        
        annotated_files = Article.objects.annotate(
        similarity=TrigramSimilarity('name', file_name)
        )

        filtered_files = annotated_files.filter(
        Q(name__icontains=file_name) | Q(similarity__gte=0.8)
        ).distinct()

        context = {
            'all_files': filtered_files
        }
        return render(request, 'mainpage.html', context)


    return render(request, 'mainpage.html', context)

def loadpage(request):
    if request.method == 'POST':
        
        uploaded_file = request.FILES['pdf']
        filename = request.POST['articlename']
        language = request.POST['language']

        file_data = translate(uploaded_file, language)
        
        check_data = json.loads(checkStatus(file_data["id"], file_data["key"]))

        while(check_data["status"] != "done"):
            check_data = json.loads(checkStatus(file_data["id"], file_data["key"]))
            time.sleep(1)

        translated_data = writeToFile(file_data["id"], file_data["key"])
        
        file_stream = BytesIO(translated_data)
        file_stream.seek(0)
        translated_file_content = ContentFile(file_stream.read(), name=f"{uuid.uuid4()}.pdf")

        article = Article()
        article.name = f"{filename}{os.path.splitext(article.name)[1]}"
        article.file.save('{0}.pdf'.format(uuid.uuid4()), uploaded_file)

        translated_article = TranslateArticle()
        translated_article.orig = article
        translated_article.lang = language
        translated_article.file.save(translated_file_content.name, translated_file_content)

        return redirect('pdfpage/{0}'.format(translated_article.file))

    return render(request, 'loadpage.html')

def pdfpage(request, file_id):
    if request.method == 'GET':
        file = get_object_or_404(Article, pk=file_id)
        return  render(request, 'pdfpage.html', {'file': file})
    
    if request.method == 'POST':

        language = request.POST['language']
        print(file_id)

        article = get_object_or_404(Article, pk=file_id)
        translated_article = article

        if article.lang != language:
            try:
                translated_article = TranslateArticle.objects.get(orig=article, lang=language)
            except:
                file_data = translate(article.file, language)

                check_data = json.loads(checkStatus(file_data["id"], file_data["key"]))

                while(check_data["status"] != "done"):
                    check_data = json.loads(checkStatus(file_data["id"], file_data["key"]))
                    time.sleep(1)

                translated_data = writeToFile(file_data["id"], file_data["key"])

                file_stream = BytesIO(translated_data)
                file_stream.seek(0)
                translated_file_content = ContentFile(file_stream.read(), name=f"{uuid.uuid4()}.pdf")

                translated_article = TranslateArticle()
                translated_article.orig = article
                translated_article.lang = language
                translated_article.file.save(translated_file_content.name, translated_file_content)

        return redirect('pdfpage'.format(translated_article.file))
        