from django.urls import path
from btp import devisView, finitionView, paiementView, travauxView, importFileView

from btp import views

urlpatterns = [
    path('homepage', views.homepage, name = "homepage"),
    path('', views.loginClientForm, name="index"),	
    path('clean', views.clean),
    path('admin-log', views.loginAdminForm, name="log-admin"),
    path('login', views.login_client),
    path('log-out', views.logout),
    path('login-admin', views.login_admin),
    path('devis', devisView.client_index, name='devis'),
    path('devis-admin', devisView.index, name='devis-admin'),
	path('devis/insert-devis', devisView.insertion),
	path('devis/insert', devisView.insertDevisForm, name='insertForm-devis'),
    path('histogramme', devisView.histogramme_montant_par_mois_par_an),	
	path('devis/updateForm/<int:id>', devisView.updateDevisForm, name='updateForm-devis'),
	path('devis/update-devis', devisView.updateDevis),
	path('devis/delete/<int:id>', devisView.deleteDevis),
	path('devis/pdf/<int:id>', devisView.detail_devis_to_pdf),
	path('devis/details/<int:id>', devisView.details_devis_html),
    path('paiement', paiementView.index, name='paiement'),
	path('paiement/insert-paiement', paiementView.insertion),
	path('paiement/pay/<int:id>', paiementView.insertPaiementForm, name='insertForm-paiement'),
	path('travaux', travauxView.index, name='travaux'),
	path('travaux/updateForm/<int:id>', travauxView.updateTravauxForm, name='updateForm-travaux'),
	path('travaux/update-travaux', travauxView.updateTravaux),
	path('finition', finitionView.index, name='finition'),
	path('finition/updateForm/<int:id>', finitionView.updateFinitionForm, name='updateForm-finition'),
	path('finition/update-finition', finitionView.updateFinition),
	path('import/import-other-Form', importFileView.import_other_Form, name='importForm-other'),
	path('import/import-other', importFileView.import_other),
	path('import/import-paiement-Form', importFileView.import_paiement_Form, name='importForm-paiement'),
	path('import/import-paiement', importFileView.import_paiement),
]