from django.forms import ModelForm
from .finition import Finition

# Create the form class.
class FinitionForm(ModelForm):
    class Meta:
        model = Finition
        fields = ["pourcentage", "libelle", "id_finition"]
