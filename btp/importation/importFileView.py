from django.shortcuts import render, redirect
from django.urls import reverse
from .importFile import treat_csv_devis, treat_csv_paiement, treat_csv_travaux
from btp.views import check_if_connected
from utility.uploadHandler import UploadHandler


def import_other_Form(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')
    context = {
        'error' : error,
    }
    return render(request, "import/import-other.html", context)

def import_paiement_Form(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = request.GET.get('error', '')
    context = {
        'error' : error,
    }
    return render(request, "import/import-paiement.html", context)


def import_other(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = []
    try:
        UploadHandler.handle_uploaded_file(request.FILES['travaux'])
        error.append(treat_csv_travaux())
        UploadHandler.handle_uploaded_file(request.FILES['devis'])
        error.append(treat_csv_devis())
        print(error)
        message = "".join(error)
        if(len(message) > 0):
            return redirect(reverse('importForm-other')+ f'?error={message}')
    except Exception as e:
        error = str(e)
        return redirect(reverse('importForm-other')+ f'?error={error}')
    return redirect("homepage")

def import_paiement(request):
    bool = check_if_connected(request)
    if(bool is False):
        return redirect('index')
    error = ""
    try:
        UploadHandler.handle_uploaded_file(request.FILES['paiement'])
        error = treat_csv_paiement()
        print(error)
        if(len(error) > 0):
            return redirect(reverse('importForm-paiement')+ f'?error={error}')
    except Exception as e:
        error = str(e)
        return redirect(reverse('importForm-paiement')+ f'?error={error}')
    return redirect("homepage")

