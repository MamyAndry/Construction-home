from django.shortcuts import render,redirect
from django.urls import reverse

from btp.models import get_annee, log_admin, login, montant_paiement_effectue_total_devis, montant_total_devis, clean_datas

# Create your views here.


def check_if_connected(request):
    bool = True
    try:
        temp =  request.session['user'] 
    except:
        bool = False
    return bool

def loginClientForm(request):
    context = {
        
    }
    return render(request, "login.html", context)

def loginAdminForm(request):
    context = {
        
    }
    return render(request, "login-admin.html", context)



def login_client(request):
    numero = request.POST['numero']
    user = login(numero)
    if(user is None):
        return redirect('index')
    request.session["user"] = user
    return redirect('devis')
    
def login_admin(request):
    email = request.POST['email']
    mdp = request.POST['password']
    user = log_admin(email, mdp)
    if user != None:
        request.session["user"] = user
        return redirect('homepage')
    else: 
        return redirect('log-admin')

def signinForm(request):
    context = {
        
    }
    return render(request, "signin.html", context)

def homepage(request):
    error = request.GET.get('error', '')
    montant_total = montant_total_devis()
    montant_total_paiement_effectue = montant_paiement_effectue_total_devis()
    annee = get_annee()
    context = {
        'error': error,
        'montant': montant_total,
        'montant_total_paiement_effectue': montant_total_paiement_effectue,
        'annee': annee,
    }
    return render(request, 'homepage.html', context)

def logout(request):
    request.session.flush()
    return redirect("index")

def clean(request):
    clean_datas()
    return redirect('homepage')
