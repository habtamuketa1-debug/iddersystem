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
        exclude = ['joined_date']

    def clean(self):
        cleaned_data = super().clean()
        
        eth_day = cleaned_data.get('eth_day')
        eth_month_raw = cleaned_data.get('eth_month')
        eth_year = cleaned_data.get('eth_year')

        if eth_day and eth_month_raw and eth_year:
            try:
                # የወሩ ዋጋ ስም ከሆነ ወደ ተጓዳኝ ቁጥር (1-13) መቀየር
                month_mapping = {
                    "መስከረም": 1, "ጥቅምት": 2, "ህዳር": 3, "ታህሳስ": 4,
                    "ጥር": 5, "የካቲት": 6, "መጋቢት": 7, "ሚያዝያ": 8,
                    "ግንቦት": 9, "ሰኔ": 10, "ሐምሌ": 11, "ነሐሴ": 12, "ጳጉሜ": 13
                }
                
                if str(eth_month_raw).isdigit():
                    month_int = int(eth_month_raw)
                else:
                    month_int = month_mapping.get(str(eth_month_raw).strip(), 1)

                year_int = int(eth_year)
                day_int = int(eth_day)

                # EthiopianDateConverter ተጠቅሞ ወደ ግሪጎሪያን ቀን መቀየር
                gregorian_date = EthiopianDateConverter.to_gregorian(year_int, month_int, day_int)
                
                # የተገኘውን ትክክለኛ ቀን መመደብ
                self.instance.joined_date = gregorian_date
                cleaned_data['joined_date'] = gregorian_date
                
            except Exception as e:
                raise forms.ValidationError(f"የተሳሳተ የኢትዮጵያ ቀን አቆጣጠር: {e}")
                
        return cleaned_data