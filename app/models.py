from django.db import models


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)

    class Meta:
        abstract = True


class University(BaseModel):
    title = models.CharField(max_length=100)


class Sponsor(BaseModel):
    class SponsorStatus(models.TextChoices):
        NEW = 'new', 'Yangi'
        MODERATION = 'moderation', 'Madiratsiyada'
        APPROVED = 'apporved', 'Tasdiqlangan'
        CANCEL = 'canceled', 'Bekor qilingan'

    class SponsorType(models.TextChoices):
        YURIDIK = 'yuridik', 'Yuridik'
        JISMONIY = 'jismoniy', 'Jismoniy'

    class PaymentType(models.TextChoices):
        CARD = 'card', 'Plastik karta'
        CASH = 'cash', 'Naqd pul'

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    organization = models.CharField(max_length=100)
    sponsor_type = models.CharField(max_length=100, choices=SponsorType.choices, default=SponsorType.JISMONIY)
    status = models.CharField(max_length=20, choices=SponsorStatus.choices, default=SponsorStatus.NEW)
    payment_type = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.full_name


class Student(BaseModel):
    class StudentType(models.TextChoices):
        BACHELOR = 'bachelor', 'Bakalavr'
        MASTER = 'master', 'Magister'

    full_name = models.CharField(max_length=100)
    student_type = models.CharField(max_length=100, choices=StudentType.choices, default=StudentType.BACHELOR)
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    contract_amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class StudentSponsor(BaseModel):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT, related_name="student_sponsors")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='student_sponsors')
