from django.forms import ModelForm
from .travaux import Travaux

# Create the form class.
class TravauxForm(ModelForm):
    class Meta:
        model = Travaux
        fields = ["libelle", "id_travaux", "prix_unitaire"]
