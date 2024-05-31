from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from btp.views import check_if_connected
from .finitionForm import FinitionForm
from .finition import Finition



def index(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = request.GET.get('message', '')
    error = request.GET.get('error', '')
    
    datas = Finition.objects.all().order_by("id_finition")
    paginator = Paginator(datas, 8)
    page_num = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {        
        'message' : message,
        'error' : error,
        'num': page_num,
        'data':page_obj
    }
    return render(request, "finition/finition.html", context)

def updateFinitionForm(request, id):    
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')
    object = Finition.objects.get(id_finition = id)  

    context = {
        'error' : error,
	'object' : object,

    }
    return render(request, "finition/update-finition.html", context)

def updateFinition(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    id = request.POST['id_finition']
    object = Finition.objects.get(id_finition = id)
    if request.method == 'POST':
        try:
            pourcentage = float(request.POST['pourcentage'])
            object.pourcentage = pourcentage
            object.libelle = request.POST['libelle']
            object.save() 
            message = "Updated succesfully"
        except Exception as e:
            error = str(e)
            return redirect(reverse('updateForm-finition', args = (id,))+ f'?error={error}')
    return redirect(reverse('finition')+ f'?message={message}&error={error}&page=1')

def deleteFinition(request, id):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    try:
        object = Finition.objects.get(id_finition = id) 
        object.delete()
        message = "Deleted succesfully"
    except Exception as e:
        error = str(e)
    return redirect(reverse('finition')+ f'?message={message}&error={error}&page=1')

def insertFinitionForm(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')

    context = {
        'error' : error,

    }
    return render(request, "finition/create-finition.html", context)



def insertion(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    if request.method == "POST":
        form = FinitionForm(request.POST)
        if(form.is_valid()):
            try:
                form.save()  
                message = "Finition added succesfully"
            except Exception as e:
                error = str(e)
                return redirect(reverse('updateForm-finition')+ f'?error={error}')
    return redirect(reverse('finition')+ f'?message={message}&error={error}&page=1')

