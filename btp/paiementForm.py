from django.forms import ModelForm
from .paiement import Paiement

# Create the form class.
class PaiementForm(ModelForm):
    class Meta:
        model = Paiement
        fields = ["ref_paiement" ,"date_paiement", "montant"]
