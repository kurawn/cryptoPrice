from dal import autocomplete
from django import forms


class PairForm(forms.Form):
    exchange = forms.ChoiceField(
        choices=[('', 'Select an exchange'), ('binance', 'Binance'), ('kraken', 'Kraken')],
        required=False,
        label="Exchange"
    )
    pair = forms.CharField(
        widget=autocomplete.ListSelect2(
            url='pair-autocomplete',
            forward=['exchange']
        ),
        required=False,
        label="Pair"
    )
