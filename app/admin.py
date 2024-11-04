from django.contrib import admin
from .models import Student, Sponsor, StudentSponsor, University


admin.site.register(Student)
admin.site.register(Sponsor)
admin.site.register(StudentSponsor)
admin.site.register(University)
