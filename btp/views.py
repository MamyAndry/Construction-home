from django.shortcuts import render,redirect

from btp.models import get_annee, log_admin, login, montant_paiement_effectue_total_devis, montant_total_devis

# Create your views here.
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
    if(user == None):
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

