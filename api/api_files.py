import os
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse
from django.utils.encoding import escape_uri_path

def download(request):
    filename  = request.GET.get('filename')
    file_path = '/data/pyweb/data-quality/static/files/' + filename
    ext = os.path.basename(file_path).split('.')[-1].lower()
    # 禁止请求含有py、db、sqlite3关键字的文件名
    if ext not in ['py', 'db',  'sqlite3']:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
        print(response['Content-Disposition'])
        return response
    else:
        raise Http404