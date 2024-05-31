import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from btp.paiementForm import PaiementForm
from btp.views import check_if_connected

from .paiement import Paiement
from .devis import Devis


def index(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = request.GET.get('message', '')
    error = request.GET.get('error', '')
    
    datas = Paiement.objects.all().order_by("id_paiement")
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
    return render(request, "paiement/paiement.html", context)

def updatePaiementForm(request, id):    
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')
    object = Paiement.objects.get(id_paiement = id)  
    devis = Devis.objects.all
    context = {
        'error' : error,
			'object' : object,
			'devis' : devis
    }
    return render(request, "paiement/update-paiement.html", context)

def deletePaiement(request, id):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    try:
        object = Paiement.objects.get(id_paiement = id) 
        object.delete()
        message = "Deleted succesfully"
    except Exception as e:
        error = str(e)
    return redirect(reverse('paiement')+ f'?message={message}&error={error}&page=1')

def insertPaiementForm(request, id):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')
    context = {
        'error' : error,
		'devis' : id
    }
    return render(request, "paiement/create-paiement.html", context)


def check_montant_payer(total, effectue, montant):
    temp = float(effectue) + float(montant)
    if float(temp) > float(total):
        raise Exception("Le montant inserer est trop grand")
    return


def insertion(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    paiement = Paiement()
    if request.method == "POST":
        form = PaiementForm(request.POST)
        if(form.is_valid()):
            try:
                montant = request.POST['montant']
                devis = Devis.objects.get(id_devis = request.POST['devis'])
                paiement.montant = montant
                paiement.devis = devis
                paiement.ref_paiement = request.POST['ref_paiement']
                paiement.date_paiement = request.POST['date_paiement']
                check_montant_payer(float(devis.prix_total), float(devis.paiement_effectue), float(paiement.montant))
                paiement.save()
                devis.paiement_effectue = float(devis.paiement_effectue) + float(paiement.montant)
                devis.save()
                message = "Payement succesfully"
            except Exception as e:
                message = str(e)
    return HttpResponse(
        json.dumps(message),
        content_type="application/json"
    )

