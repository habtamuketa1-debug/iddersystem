from django import forms
from .models import Member, Contribution, ETHIOPIAN_MONTHS
from ethiopian_date import EthiopianDateConverter  # የኢትዮጵያ ቀን መቀየሪያ ቤተ-መጽሐፍት

class MemberAdminForm(forms.ModelForm):
    # የኢትዮጵያ ቀን መራጫ ፊልዶች
    eth_day = forms.IntegerField(
        label="የኢትዮጵያ ቀን (1-30)", 
        min_value=1, 
        max_value=30, 
        initial=1
    )
    eth_month = forms.ChoiceField(
        choices=ETHIOPIAN_MONTH_NAMES if 'ETHIOPIAN_MONTH_NAMES' in globals() else ETHIOPIAN_MONTHS, 
        label="የኢትዮጵያ ወር"
    )
    eth_year = forms.IntegerField(
        label="ዓመተ ምሕረት", 
        initial=2016
    )

    class Meta:
        model = Member
        exclude = ['joined_date']  # አሮጌውን የግሪጎሪያን ቀን መምረጫ በመደበቅ በኢትዮጵያ ቀን እንዲተካ ማድረግ

    def clean(self):
        cleaned_data = super().clean()
        eth_day = cleaned_data.get('eth_day')
        eth_month = cleaned_data.get('eth_month')
        eth_year = cleaned_data.get('eth_year')

        if eth_day and eth_month and eth_year:
            try:
                # EthiopianDateConverter ተጠቅሞ ወደ ግሪጎሪያን ቀን መቀየር
                gregorian_date = EthiopianDateConverter.to_gregorian(
                    int(eth_year), int(eth_month), int(eth_day)
                )
                
                # የተለወጠውን ቀን ለ cleaned_data እና ለ instance መስጠት
                cleaned_data['joined_date'] = gregorian_date
                self.instance.joined_date = gregorian_date
                
            except Exception as e:
                raise forms.ValidationError(f"የተሳሳተ የኢትዮጵያ ቀን አቆጣጠር: {e}")
                
        return cleaned_data