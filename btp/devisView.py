from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from btp.detailsDevis import DetailsDevis
from btp.devisPdf import get_html_for_pdf
from btp.lieu import Lieu
from btp.models import get_duree_total_devis, get_montant_total, insert_details_devis, montant_devis_par_mois_par_an

from btp.paiement import Paiement
from btp.views import check_if_connected
from utility.pdfHandler import Pdf_handler
from .devis import Devis
from .utilisateurs import Utilisateurs
from .finition import Finition
from .typeMaison import TypeMaison


def index(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = request.GET.get('message', '')
    error = request.GET.get('error', '')
    
    datas = Devis.objects.all().order_by("id_devis")
    paginator = Paginator(datas, 8)
    page_num = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    pourcentage = []
    for elt in page_obj:
        if elt.paiement_effectue is None:
            pourcentage.append(0)
        else:
            temp = (elt.paiement_effectue/elt.prix_total)*100
            pourcentage.append(format(temp,".2f"))
    limit = len(pourcentage)
    context = {        
        'message' : message,
        'error' : error,
        'num': page_num,
        'data':page_obj,
        'pourcentage': pourcentage,
        'range': range(0, limit)
    }
    return render(request, "devis/devis-admin.html", context)

def client_index(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')  
    
    message = request.GET.get('message', '')
    error = request.GET.get('error', '')
    
    datas = Devis.objects.filter(client__exact = request.session['user']['id_utilisateur']).order_by("id_devis")
    paginator = Paginator(datas, 8)
    page_num = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    print(datas)
    context = {        
        'message' : message,
        'error' : error,
        'num': page_num,
        'data':page_obj
    }
    return render(request, "devis/devis.html", context)

def updateDevisForm(request, id):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')
    object = Devis.objects.get(id_devis = id) 
    finitions = Finition.objects.all()
    typeMaisons = TypeMaison.objects.all()
    context = {
        'error' : error,
        'object' : object,
        'finition' : finitions,
        'type_maison' : typeMaisons
    }
    return render(request, "devis/update-devis.html", context)

def updateDevis(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    id = request.POST['id_devis']
    devis = Devis.objects.get(id_devis = id)
    if request.method == 'POST':
        try:
            devis.type = TypeMaison.objects.get(id_type = request.POST['type'])   
            devis.finition = Finition.objects.get(id_finition = request.POST['finition'])
            devis.prix_total = 0
            devis.save()  
            message = "Updated succesfully"
        except Exception as e:
            error = str(e)
            return redirect(reverse('updateForm-devis', args = (id,))+ f'?error={error}')
    return redirect(reverse('devis')+ f'?message={message}&error={error}&page=1')

def deleteDevis(request, id):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    try:
        object = Devis.objects.get(id_devis = id) 
        object.delete()
        message = "Deleted succesfully"
    except Exception as e:
        error = str(e)
    return redirect(reverse('devis')+ f'?message={message}&error={error}&page=1')

def insertDevisForm(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')
    finitions = Finition.objects.all()
    typeMaisons = TypeMaison.objects.all()
    lieu = Lieu.objects.all()
    context = {
        'error' : error,
		'finition' : finitions,
		'type_maison' : typeMaisons,
        'lieu': lieu,
    }
    return render(request, "devis/create-devis.html", context)

def insertion(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    message = ""
    error = ""
    devis = Devis()
    if request.method == "POST":
        try:
            finition = Finition.objects.get(id_finition = request.POST['finition'])
            devis.client = Utilisateurs.objects.get(id_utilisateur = request.session['user']['id_utilisateur'])
            devis.type = TypeMaison.objects.get(id_type = request.POST['type'])   
            devis.finition = finition
            devis.pourcentage = finition.pourcentage
            devis.date_devis = datetime.now()
            devis.date_debut_construction = request.POST['date_debut_construction']
            devis.lieu = Lieu.objects.get(id_lieu = request.POST['lieu'])
            devis.paiement_effectue = 0
            devis.save()
            devis.prix_total = get_montant_total(devis.id_devis, finition.pourcentage)
            devis.date_fin_construction = datetime.strptime(devis.date_debut_construction, "%Y-%m-%d") + timedelta(days=devis.type.duree)
            devis.save()
            message = "Devis added succesfully"
        except Exception as e:
            error = str(e)
            return redirect(reverse('insertForm-devis')+ f'?error={error}')
    return redirect(reverse('devis')+ f'?message={message}&error={error}&page=1')

def detail_devis_to_pdf(request, id):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    devis = Devis.objects.get(id_devis = id)
    paiement = Paiement.objects.filter(devis__exact = id)
    details = DetailsDevis.objects.filter(devis__exact = id)
    html = get_html_for_pdf(devis, details, paiement)
    pdf_handler = Pdf_handler("./files/devis.pdf", html)

    pdf_content = pdf_handler.toPdf()
    
    if pdf_content:
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="devis.pdf"'
        return response
    else:
        return HttpResponse("Failed to generate PDF", status=500)
    
def details_devis_html(request, id):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    devis = Devis.objects.get(id_devis = id)
    details = DetailsDevis.objects.filter(devis__exact = id)
    context = {
        'devis' : devis,
        'details' : details,
    }
    return render(request, "devis/detail-devis.html", context)

def histogramme_montant_par_mois_par_an(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    annee = request.GET.get('annee')
    # Remove the comma
    formatted_string = annee.replace(",", "")
    # Convert the formatted string to an integer
    integer_value = int(formatted_string)
    datas = montant_devis_par_mois_par_an(integer_value)
    context = {
        'annee' : integer_value,
        'data' : datas
    }
    return render(request, "charts/stack-bar.html", context)
