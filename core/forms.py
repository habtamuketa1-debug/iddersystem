from django import forms
from .models import Member, Contribution, ETHIOPIAN_MONTHS
from ethiopian_date import EthiopianDateConverter  # የኢትዮጵያ ቀን መቀየሪያ ቤተ-መጽሐፍት

class MemberAdminForm(forms.ModelForm):
    # የኢትዮጵያ ቀን መራጫ ፊልዶች
    eth_day = forms.IntegerField(label="የኢትዮጵያ ቀን (1-30)", min_value=1, max_value=30, initial=1)
    eth_month = forms.ChoiceField(choices=ETHIOPIAN_MONTHS, label="የኢትዮጵያ ወር")
    eth_year = forms.IntegerField(label="ዓመተ ምሕረት", initial=2016)

    class Meta:
        model = Member
        exclude = ['joined_date']  # የፈረንሳይኛውን ቀን መደበቅ

    def clean(self):
        cleaned_data = super().clean()
        
        # ከፎርሙ የኢትዮጵያ ቀን መምረጫዎች የተመረጠውን መውሰድ
        eth_day = cleaned_data.get('eth_day')
        eth_month = cleaned_data.get('eth_month')
        eth_year = cleaned_data.get('eth_year')

        if eth_day and eth_month and eth_year:
            try:
                # ቁጥሮች መሆናቸውን ማረጋገጥ እና ወደ ግሪጎሪያን መቀየር
                year_int = int(eth_year)
                month_int = int(eth_month)
                day_int = int(eth_day)

                # EthiopianDateConverter ተጠቅሞ ወደ ግሪጎሪያን ቀን መቀየር
                gregorian_date = EthiopianDateConverter.to_gregorian(year_int, month_int, day_int)
                
                # የተገኘውን ትክክለኛ የግሪጎሪያን ቀን ለ ሞዴሉ ኢንስታንስ መስጠት
                self.instance.joined_date = gregorian_date
                cleaned_data['joined_date'] = gregorian_date
                
            except Exception as e:
                raise forms.ValidationError(f"የተሳሳተ የኢትዮጵያ ቀን አቆጣጠር: {e}")
                
        return cleaned_data