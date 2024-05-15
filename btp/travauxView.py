from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .travauxForm import TravauxForm
from .travaux import Travaux
from .unite import Unite



def index(request):
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
    message = ""
    error = ""
    id = request.POST['id_travaux']
    model_instance = Travaux.objects.get(id_travaux = id)
    if request.method == 'POST':
        form = TravauxForm(request.POST, instance=model_instance)
        if(form.is_valid()):
            try:
                form.save() 
                message = "Updated succesfully"
            except Exception as e:
                error = str(e)
                return redirect(reverse('updateForm-travaux', args = (id,))+ f'?error={error}')
    return redirect(reverse('travaux')+ f'?message={message}&error={error}&page=1')

def deleteTravaux(request, id):
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
    error = request.GET.get('error', '')
    unites = Unite.objects.all()
    context = {
        'error' : error,
		'unite' : unites
    }
    return render(request, "travaux/create-travaux.html", context)



def insertion(request):
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

