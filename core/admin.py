from django.contrib import admin
from django.utils.html import format_html
from .models import Member, FamilyMember, Contribution, IddirEvent

# 1. የአድሚን ፓነል ርዕሶችን በዕድራችን ስም ማበጀት
admin.site.site_header = "«በቅ.ሚካኤል ቤ.ክ የአካባቢ ልጆች መ.እድር» - አስተዳደር ፓነል"
admin.site.site_title = "የዕድር አስተዳደር"
admin.site.index_title = "ወደ ዕድር አስተዳደር ዳሽቦርድ እንኳን በደህና መጡ"


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('profile_preview', 'full_name', 'phone_number', 'address', 'status', 'joined_date')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('status', 'joined_date')

    # ፎቶውን በአድሚን ሰንጠረዥ ውስጥ በክብ ቅርጽ ለማሳየት
    def profile_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', obj.profile_picture.url)
        return "ፎቶ የለም"
    
    profile_preview.short_description = "መገለጫ ፎቶ"


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'member', 'relationship')
    search_fields = ('full_name', 'member__full_name')


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'eth_month', 'eth_year', 'date_paid')
    search_fields = ('member__full_name',)
    list_filter = ('eth_month', 'eth_year', 'date_paid')


@admin.register(IddirEvent)
class IddirEventAdmin(admin.ModelAdmin):
    list_display = ('member', 'deceased_name', 'relationship', 'event_date', 'payout_amount', 'is_settled')
    search_fields = ('member__full_name', 'deceased_name')
    list_filter = ('is_settled', 'event_date')