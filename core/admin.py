from django.contrib import admin
from django.utils.html import format_html
from .models import Member, FamilyMember, Contribution, IddirEvent
from .forms import MemberAdminForm  # <--- 1. የኢትዮጵያ ፎርሙን ማስገባት
from ethiopian_date import EthiopianDateConverter  # <--- የኢትዮጵያ ቀን መቀየሪያ

# የኢትዮጵያ ወራት ስም ዝርዝር
ETHIOPIAN_MONTH_NAMES = {
    1: "መስከረም", 2: "ጥቅምት", 3: "ህዳር", 4: "ታህሳስ",
    5: "ጥር", 6: "የካቲት", 7: "መጋቢት", 8: "ሚያዝያ",
    9: "ግንቦት", 10: "ሰኔ", 11: "ሐምሌ", 12: "ነሐሴ", 13: "ጳጉሜ"
}

# 1. የአድሚን ፓነል ርዕሶችን በዕድራችን ስም ማበጀት
admin.site.site_header = "«በቅ.ሚካኤል ቤ.ክ የአካባቢ ልጆች መ.እድር» - አስተዳደር ፓነል"
admin.site.site_title = "የዕድር አስተዳደር"
admin.site.index_title = "ወደ ዕድር አስተዳደር ዳሽቦርድ እንኳን በደህና መጡ"


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    form = MemberAdminForm  # <--- 2. ፎርሙን ከዚህ ጋር ማያያዝ
    
    # ሠንጠረዡ ላይ የፈረንሳይኛውን 'joined_date' በማጥፋት የኢትዮጵያውን 'formatted_joined_date' ብቻ ማሳየት
    list_display = ('profile_preview', 'full_name', 'phone_number', 'address', 'status', 'formatted_joined_date')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('status',)

    # ፎቶውን በአድሚን ሰንጠረዥ ውስጥ በክብ ቅርጽ ለማሳየት
    def profile_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', obj.profile_picture.url)
        return "ፎቶ የለም"
    
    profile_preview.short_description = "መገለጫ ፎቶ"

    # የተመዘገበበትን ቀን ወደ ኢትዮጵያ አቆጣጠር እና በወር ስም ቀይሮ በአድሚን ሰንጠረዥ ውስጥ ለማሳየት
    def formatted_joined_date(self, obj):
        if obj.joined_date:
            try:
                dt = obj.joined_date
                eth_date = EthiopianDateConverter.to_ethiopian(dt.year, dt.month, dt.day)
                
                # የተመለሰው መረጃ ቅርጽ (Format) ታፕል፣ ሊስት ወይም ኦብጀክት መሆኑን በራሱ ለይቶ ማስተናገድ
                if isinstance(eth_date, (list, tuple)) and len(eth_date) >= 3:
                    eth_year, eth_month, eth_day = eth_date[0], eth_date[1], eth_date[2]
                elif hasattr(eth_date, 'year') and hasattr(eth_date, 'month') and hasattr(eth_date, 'day'):
                    eth_year, eth_month, eth_day = eth_date.year, eth_date.month, eth_date.day
                else:
                    eth_year, eth_month, eth_day = eth_date[0], eth_date[1], eth_date[2]

                month_name = ETHIOPIAN_MONTH_NAMES.get(int(eth_month), str(eth_month))
                return f"{month_name} {eth_day}፣ {eth_year} ዓ.ም"
            except Exception as e:
                return f"ስህተት: {e}"
        return "-"
    
    formatted_joined_date.short_description = "የተቀላቀለበት ቀን (ኢትዮጵያ)"


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'member', 'relationship')
    search_fields = ('full_name', 'member__full_name')


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    # 'eth_month' ምትክ 'formatted_eth_month' በመጠቀም የወሩን ስም በሰንጠረዥ ማሳየት
    list_display = ('member', 'amount', 'formatted_eth_month', 'eth_year', 'date_paid')
    search_fields = ('member__full_name',)
    list_filter = ('eth_month', 'eth_year', 'date_paid')

    # የኢትዮጵያ ወር ቁጥርን ወደ ጽሁፍ (ስም) ቀይሮ ለማሳየት
    def formatted_eth_month(self, obj):
        try:
            return ETHIOPIAN_MONTH_NAMES.get(int(obj.eth_month), obj.eth_month)
        except Exception:
            return obj.eth_month
            
    formatted_eth_month.short_description = "የኢትዮጵያ ወር"


@admin.register(IddirEvent)
class IddirEventAdmin(admin.ModelAdmin):
    list_display = ('member', 'deceased_name', 'relationship', 'event_date', 'payout_amount', 'is_settled')
    search_fields = ('member__full_name', 'deceased_name')
    list_filter = ('is_settled', 'event_date')