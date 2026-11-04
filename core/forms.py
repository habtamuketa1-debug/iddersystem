from django import forms
from datetime import date
from .models import Member, Contribution, ETHIOPIAN_MONTHS
from ethiopian_date import EthiopianDateConverter

class MemberAdminForm(forms.ModelForm):
    # ዛሬ ያለንበትን የኢትዮጵያ ቀን ማስላት
    try:
        t_year, t_month, t_day = EthiopianDateConverter.to_ethiopian(
            date.today().year, date.today().month, date.today().day
        )
    except Exception:
        t_year, t_month, t_day = 2019, 3, 25

    eth_day = forms.IntegerField(label="የኢትዮጵያ ቀን (1-30)", min_value=1, max_value=30, initial=t_day)
    eth_month = forms.ChoiceField(choices=ETHIOPIAN_MONTHS, label="የኢትዮጵያ ወር", initial=str(t_month))
    eth_year = forms.IntegerField(label="ዓመተ ምሕረት", initial=t_year)

    class Meta:
        model = Member
        exclude = ['joined_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # አባልን ኤዲት (Edit) ሲያደርጉ የነበረውን ቀን ወደ ኢትዮጵያ ቀይሮ በኢንፑቱ ላይ ለማሳየት
        if self.instance and self.instance.joined_date:
            try:
                dt = self.instance.joined_date
                ey, em, ed = EthiopianDateConverter.to_ethiopian(dt.year, dt.month, dt.day)
                self.fields['eth_day'].initial = ed
                self.fields['eth_month'].initial = str(em)
                self.fields['eth_year'].initial = ey
            except Exception:
                pass

    def clean(self):
        cleaned_data = super().clean()
        eth_day = cleaned_data.get('eth_day')
        eth_month_raw = cleaned_data.get('eth_month')
        eth_year = cleaned_data.get('eth_year')

        if eth_day and eth_month_raw and eth_year:
            try:
                month_mapping = {
                    "መስከረም": 1, "ጥቅምት": 2, "ህዳር": 3, "ታህሳስ": 4,
                    "ጥር": 5, "የካቲት": 6, "መጋቢት": 7, "ሚያዝያ": 8,
                    "ግንቦት": 9, "ሰኔ": 10, "ሐምሌ": 11, "ነሐሴ": 12, "ጳጉሜ": 13
                }
                
                if str(eth_month_raw).isdigit():
                    month_int = int(eth_month_raw)
                else:
                    month_int = month_mapping.get(str(eth_month_raw).strip(), 3)

                # ወደ ግሪጎሪያን ቀን መቀየር
                gregorian_date = EthiopianDateConverter.to_gregorian(int(eth_year), month_int, int(eth_day))
                
                # የተለወጠውን ቀን ለ cleaned_data መስጠት
                cleaned_data['joined_date'] = gregorian_date
                
            except Exception as e:
                raise forms.ValidationError(f"የተሳሳተ የኢትዮጵያ ቀን አቆጣጠር: {e}")
                
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # clean() ውስጥ የተሰላውን joined_date በቀጥታ ለሞዴሉ መስጠት
        if 'joined_date' in self.cleaned_data:
            instance.joined_date = self.cleaned_data['joined_date']
            
        if commit:
            instance.save()
        return instance