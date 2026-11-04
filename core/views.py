from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db.models import Sum
from .models import Member, Contribution, IddirEvent, FamilyMember
from ethiopian_date import EthiopianDateConverter  # <--- የኢትዮጵያ ካላንደር ፓኬጅ ተጨምሯል


# ረዳት ፉንክሽን (Helper Function): ግሬጎሪያን ቀንን ወደ ኢትዮጵያ ቀን የሚቀይር
def format_to_ethiopian(gregorian_date):
    if not gregorian_date:
        return ""
    try:
        eth_year, eth_month, eth_day = EthiopianDateConverter.to_ethiopian(
            gregorian_date.year, gregorian_date.month, gregorian_date.day
        )
        months = [
            "መስከረም", "ጥቅምት", "ህዳር", "ታህሳስ", "ጥር", "የካቲት",
            "መጋቢት", "ሚያዝያ", "ግንቦት", "ሰኔ", "ሐምሌ", "ነሐሴ", "ጳጉሜ"
        ]
        month_name = months[eth_month - 1] if 1 <= eth_month <= len(months) else str(eth_month)
        return f"{month_name} {eth_day}, {eth_year}"
    except Exception:
        return str(gregorian_date)


# 0. የሎጊን ፕላትፎርም (Custom Login View)
def custom_login_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(request, username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ወደ ዳሽቦርድ ይመራቸዋል
        else:
            return render(request, 'core/login.html', {'error': 'የተሳሳተ የተጠቃሚ ስም ወይም የይለፍ ቃል!'})
    return render(request, 'core/login.html')


# 1. ዳሽቦርድ (Dashboard View)
def iddir_dashboard(request):
    total_members = Member.objects.count()
    active_members = Member.objects.filter(is_active=True).count()
    
    # ጠቅላላ የተሰበሰበ መዋጮ መጠን
    total_contributions = Contribution.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # ያልተጠናቀቁ የሀዘን/የዕድር ጉዳዮች
    pending_events = IddirEvent.objects.filter(is_settled=False).count()
    
    recent_members = Member.objects.order_by('-joined_date')[:5]
    for m in recent_members:
        m.ethiopian_joined = format_to_ethiopian(m.joined_date)

    recent_contributions = Contribution.objects.order_by('-date_paid')[:5]
    for c in recent_contributions:
        c.ethiopian_date = format_to_ethiopian(c.date_paid)

    context = {
        'total_members': total_members,
        'active_members': active_members,
        'total_contributions': total_contributions,
        'pending_events': pending_events,
        'recent_members': recent_members,
        'recent_contributions': recent_contributions,
    }
    return render(request, 'core/dashboard.html', context)


# 2. የሂሳብ እና ኦዲት ሪፖርት (Financial & Audit Report View)
def financial_report_view(request):
    # ጠቅላላ ገቢ (ከተሰበሰቡ መዋጮዎች)
    total_income = Contribution.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    # ጠቅላላ ወጪ (ከተሰጡ የሀዘን ድጋፎች)
    total_expense = IddirEvent.objects.filter(is_settled=True).aggregate(total=Sum('payout_amount'))['total'] or 0
    
    # ቀሪ ሂሳብ
    net_balance = total_income - total_expense

    # የክፍያዎች እና የሀዘን መዝገቦች ዝርዝር
    contributions = Contribution.objects.all().order_by('-date_paid')
    for item in contributions:
        item.ethiopian_date = format_to_ethiopian(item.date_paid)

    events = IddirEvent.objects.filter(is_settled=True).order_by('-event_date')
    for event in events:
        event.ethiopian_date = format_to_ethiopian(event.event_date)

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'contributions': contributions,
        'events': events,
    }
    return render(request, 'core/financial_report.html', context)


# 3. የአባላት ፖርታል (Member Portal View)
def member_portal_view(request):
    phone = request.GET.get('phone', '')
    member = None
    contributions = []
    family_members = []

    if phone:
        try:
            member = Member.objects.get(phone_number=phone)
            contributions = Contribution.objects.filter(member=member).order_by('-date_paid')
            for c in contributions:
                c.ethiopian_date = format_to_ethiopian(c.date_paid)
            family_members = FamilyMember.objects.filter(member=member)
        except Member.DoesNotExist:
            member = None

    context = {
        'member': member,
        'phone': phone,
        'contributions': contributions,
        'family_members': family_members,
    }
    return render(request, 'core/member_portal.html', context)


# 4. አዲስ አባል መመዝገቢያ (Add Member View)
def add_member_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        
        # ዳታቤዝ ውስጥ መመዝገብ እና ሴቭ ማድረግ
        Member.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            is_active=True
        )
        return redirect('dashboard')
        
    return render(request, 'core/add_member.html')