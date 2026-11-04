from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from ethiopian_date import EthiopianDateConverter

# የኢትዮጵያ ወራት ስም መዝገብ (ለድረ-ገጽ ማሳያ)
ETHIOPIAN_MONTH_DICT = {
    1: "መስከረም", 2: "ጥቅምት", 3: "ህዳር", 4: "ታህሳስ",
    5: "ጥር", 6: "የካቲት", 7: "መጋቢት", 8: "ሚያዝያ",
    9: "ግንቦት", 10: "ሰኔ", 11: "ሐምሌ", 12: "ነሐሴ", 13: "ጳጉሜ"
}

MEMBER_STATUS_CHOICES = [
    ('ACTIVE', 'ንቁ (Active)'),
    ('SUSPENDED', 'የረፈደ (Suspended)'),
    ('RESIGNED', 'የወጣ'),
]

class Member(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="ሙሉ ስም")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="ስልክ ቁጥር")
    address = models.CharField(max_length=250, verbose_name="አድራሻ (ቀበሌ/ወረዳ)")
    profile_picture = CloudinaryField('image', blank=True, null=True)
    status = models.CharField(max_length=20, choices=MEMBER_STATUS_CHOICES, default='ACTIVE', verbose_name="የአባል ሁኔታ")
    joined_date = models.DateField(null=True, blank=True, verbose_name="የተቀላቀለበት ቀን")
    is_active = models.BooleanField(default=True, verbose_name="ንቁ ነው?")

    def __str__(self):
        return f"{self.full_name} ({self.get_status_display()})"

    def formatted_joined_date_eth(self):
        if not self.joined_date:
            return "-"
        try:
            dt = self.joined_date
            ey, em, ed = EthiopianDateConverter.to_ethiopian(dt.year, dt.month, dt.day)
            m_name = ETHIOPIAN_MONTH_DICT.get(int(em), str(em))
            return f"{m_name} {ed}፣ {ey} ዓ.ም"
        except Exception:
            return str(self.joined_date)

    class Meta:
        verbose_name = "የዕድር አባል"
        verbose_name_plural = "የዕድር አባላት"


class FamilyMember(models.Model):
    member = models.ForeignKey(Member, on_default=models.CASCADE, on_delete=models.CASCADE, related_name='family_members', verbose_name="ዋናው አባል")
    full_name = models.CharField(max_length=150, verbose_name="የቤተሰብ አባል ስም")
    relationship = models.CharField(max_length=50, verbose_name="ዝምድና")
    
    def __str__(self):
        return f"{self.full_name} - {self.relationship} ({self.member.full_name})"

    class Meta:
        verbose_name = "የቤተሰብ አባል"
        verbose_name_plural = "የቤተሰብ አባላት"


ETHIOPIAN_MONTHS = [
    ('1', 'መስከረም'), ('2', 'ጥቅምት'), ('3', 'ህዳር'), ('4', 'ታህሳስ'),
    ('5', 'ጥር'), ('6', 'የካቲት'), ('7', 'መጋቢት'), ('8', 'ሚያዝያ'),
    ('9', 'ግንቦት'), ('10', 'ሰኔ'), ('11', 'ሐምሌ'), ('12', 'ነሐሴ'), ('13', 'ጳጉሜ'),
]


class Contribution(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='contributions', verbose_name="አባል")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="የተከፈለ መጠን (ብር)")
    eth_month = models.CharField(max_length=20, choices=ETHIOPIAN_MONTHS, verbose_name="የኢትዮጵያ ወር")
    eth_year = models.CharField(max_length=10, default="2019", verbose_name="ዓመተ ምሕረት")
    date_paid = models.DateField(null=True, blank=True, verbose_name="የተከፈለበት ቀን")

    def __str__(self):
        return f"{self.member.full_name} - {self.amount} ብር"

    def formatted_date_paid_eth(self):
        if not self.date_paid:
            return "-"
        try:
            dt = self.date_paid
            ey, em, ed = EthiopianDateConverter.to_ethiopian(dt.year, dt.month, dt.day)
            m_name = ETHIOPIAN_MONTH_DICT.get(int(em), str(em))
            return f"{m_name} {ed}፣ {ey} ዓ.ም"
        except Exception:
            return str(self.date_paid)

    class Meta:
        verbose_name = "የመዋጮ ክፍያ"
        verbose_name_plural = "የመዋጮ ክፍያዎች"


class IddirEvent(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='events', verbose_name="ጉዳዩ የደረሰበት አባል")
    deceased_name = models.CharField(max_length=150, verbose_name="የሞተው/የተቸገረው ሰው ስም")
    relationship = models.CharField(max_length=50, verbose_name="ከአባሉ ጋር ያለው ዝምድና")
    event_date = models.DateField(null=True, blank=True, verbose_name="ክስተቱ/ሀዘኑ የደረሰበት ቀን")
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="የተሰጠ የገንዘብ ድጋፍ (ብር)")
    is_settled = models.BooleanField(default=False, verbose_name="ድጋፉ ተሰጥቶ ተጠናቋል?")

    def __str__(self):
        return f"ሀዘን፦ {self.deceased_name} ({self.member.full_name})"

    class Meta:
        verbose_name = "የሀዘን/ጉዳይ መዝገብ"
        verbose_name_plural = "የሀዘን/ጉዳይ መዝገቦች"