from django import forms
from .models import Member, Contribution, ETHIOPIAN_MONTHS

class MemberAdminForm(forms.ModelForm):
    # የኢትዮጵያ ቀን መራጫ ፊልዶች
    eth_day = forms.IntegerField(label="የኢትዮጵያ ቀን (1-30)", min_value=1, max_value=30, initial=1)
    eth_month = forms.ChoiceField(choices=ETHIOPIAN_MONTHS, label="የኢትዮጵያ ወር")
    eth_year = forms.IntegerField(label="ዓመተ ምሕረት", initial=2019)

    class Meta:
        model = Member
        fields = '__all__'