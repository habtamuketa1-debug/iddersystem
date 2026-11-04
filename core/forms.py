from django import forms
from .models import Member, Contribution, ETHIOPIAN_MONTHS
from ethiopian_date import EthiopianDateConverter # የኢትዮጵያ ቀን መቀየሪያ ቤተ-መጽሐፍት

class MemberAdminForm(forms.ModelForm):
    # የኢትዮጵያ ቀን መራጫ ፊልዶች
    eth_day = forms.IntegerField(label="የኢትዮጵያ ቀን (1-30)", min_value=1, max_value=30, initial=1)
    eth_month = forms.ChoiceField(choices=ETHIOPIAN_MONTHS, label="የኢትዮጵያ ወር")
    eth_year = forms.IntegerField(label="ዓመተ ምሕረት", initial=2016) # እንደ አስፈላጊነቱ አመቱን ማስተካከል ይቻላል

    class Meta:
        model = Member
        fields = '__all__'
        # ዴፍልት የሆነውን የፈረንሳይኛ ቀን ፊልድ ከፈለጉ መደበቅ ወይም ከዚህ በታች ማስተካከል ይቻላል

    def clean(self):
        cleaned_data = super().clean()
        eth_day = cleaned_data.get('eth_day')
        eth_month = int(cleaned_data.get('eth_month', 1))
        eth_year = cleaned_data.get('eth_year')

        if eth_day and eth_month and eth_year:
            try:
                # EthiopianDateConverter ተጠቅሞ ወደ ግሪጎሪያን (European) ቀን መቀየር
                gregorian_date = EthiopianDateConverter.to_gregorian(eth_year, eth_month, eth_day)
                # የዳታቤዙን የተጠቃሚ መቀበያ ቀን (לምሳሌ: joined_date) በእርግጠኛነት መቀየር
                cleaned_data['joined_date'] = gregorian_date 
            except Exception as e:
                raise forms.ValidationError(f"የተሳሳተ የኢትዮጵያ ቀን አቆጣጠር: {e}")
                
        return cleaned_data