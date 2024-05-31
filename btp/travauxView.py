from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from btp.views import check_if_connected
from .travauxForm import TravauxForm
from .travaux import Travaux
from .unite import Unite



def index(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = request.GET.get('message', '')
    error = request.GET.get('error', '')
    
    datas = Travaux.objects.all().order_by("id_travaux")
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
    return render(request, "travaux/travaux.html", context)

def updateTravauxForm(request, id):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')
    object = Travaux.objects.get(id_travaux = id)  
    unites = Unite.objects.all()
    context = {
        'error' : error,
        'object' : object,
        'unite' : unites
    }
    return render(request, "travaux/update-travaux.html", context)

def updateTravaux(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    id = request.POST['id_travaux']
    object = Travaux.objects.get(id_travaux = id)
    if request.method == 'POST':
            try:
                object.prix_unitaire = float(request.POST['prix_unitaire'])
                object.libelle = request.POST['libelle']
                object.save() 
                message = "Updated succesfully"
            except Exception as e:
                error = str(e)
                return redirect(reverse('updateForm-travaux', args = (id,))+ f'?error={error}')
    return redirect(reverse('travaux')+ f'?message={message}&error={error}&page=1')

def deleteTravaux(request, id):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    try:
        object = Travaux.objects.get(id_travaux = id) 
        object.delete()
        message = "Deleted succesfully"
    except Exception as e:
        error = str(e)
    return redirect(reverse('travaux')+ f'?message={message}&error={error}&page=1')

def insertTravauxForm(request):    
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')
    unites = Unite.objects.all()
    context = {
        'error' : error,
		'unite' : unites
    }
    return render(request, "travaux/create-travaux.html", context)



def insertion(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    if request.method == "POST":
        form = TravauxForm(request.POST)
        if(form.is_valid()):
            try:
                form.save()  
                message = "Travaux added succesfully"
            except Exception as e:
                error = str(e)
                return redirect(reverse('updateForm-travaux')+ f'?error={error}')
    return redirect(reverse('travaux')+ f'?message={message}&error={error}&page=1')

