from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .finitionForm import FinitionForm
from .finition import Finition



def index(request):
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
    error = request.GET.get('error', '')
    object = Finition.objects.get(id_finition = id)  

    context = {
        'error' : error,
	'object' : object,

    }
    return render(request, "finition/update-finition.html", context)

def updateFinition(request):
    message = ""
    error = ""
    id = request.POST['id_finition']
    model_instance = Finition.objects.get(id_finition = id)
    if request.method == 'POST':
        form = FinitionForm(request.POST, instance=model_instance)
        if(form.is_valid()):
            try:
                form.save() 
                message = "Updated succesfully"
            except Exception as e:
                error = str(e)
                return redirect(reverse('updateForm-finition', args = (id,))+ f'?error={error}')
    return redirect(reverse('finition')+ f'?message={message}&error={error}&page=1')

def deleteFinition(request, id):
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
    error = request.GET.get('error', '')

    context = {
        'error' : error,

    }
    return render(request, "finition/create-finition.html", context)



def insertion(request):
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

