from django.shortcuts import render, redirect
from django.http import HttpResponse

import os
from utils.functions import is_login


@is_login
def list(request):
    username = request.session['username']
    request_type = request.GET.get('request_type')
    file_name = os.listdir('/data/pyweb/data-quality/static/files')
    title = '数据治理知识库'

    if request_type == 'word_report':
        file_name = [f for f in file_name if f.find('工作通报') != -1]
        title = '数据治理工作通报'

    all_files = []
    for i in file_name:
        file_type = i.split('.')
        file_type = file_type[len(file_type) - 1]  #获取文件扩展名
        if file_type in ['xls', 'xlsx', 'xlsm', 'csv', 'xml']:
            file_type = 'excel'
        elif file_type in ['txt']:
            file_type = 'text'
        elif file_type in ['docx', 'doc']:
            file_type = 'word'
        elif file_type in ['htm', 'html']:
            file_type = 'html'
        elif file_type in ['ppt', 'pptx']:
            file_type = 'powerpoint'
        elif file_type in ['jpg', 'png', 'jpeg', 'gif', 'bmp']:
            file_type = 'image'
        all_files.append([file_type, i])
    return render(request, 'files/file_list.html', {
        'all_files': all_files,
        'username': username,
        'title': title
    })
