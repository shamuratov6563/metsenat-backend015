from rest_framework.serializers import  ModelSerializer
from . import models
from rest_framework import serializers
from django.db.models import Sum



class StudentSerializer(ModelSerializer):
    university = serializers.StringRelatedField(source='university.title')
    allocated_money = serializers.SerializerMethodField()

    def get_allocated_money(self, obj):
        return obj.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0


    class Meta:
        model = models.Student
        exclude = ('phone', 'created_at', 'updated_at', )


class StudentDetailSerializer(ModelSerializer):
    university = serializers.StringRelatedField(source='university.title')
    allocated_money = serializers.SerializerMethodField()

    def get_allocated_money(self, obj):
        return obj.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0


    class Meta:
        model = models.Student
        exclude = ('created_at', 'updated_at')


class StudentSponsorSerializer(ModelSerializer):

    class Meta:
        model = models.StudentSponsor
        fields = ("id", 'student', 'sponsor', 'amount')

    def validate(self, attrs):
        amount = attrs.get('amount')
        sponsor = attrs.get('sponsor')
        student = attrs.get('student')
        from django.db.models import Sum
        student_paid_money = student.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        if student.contract_amount - student_paid_money < amount:
            raise serializers.ValidationError(
                detail={'error': f"Siz {student.contract_amount - student_paid_money}  pul to'lasangiz yetarli"})

        sponsor_paid_money = sponsor.student_sponsors.all().aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        if sponsor.amount - sponsor_paid_money < amount:
            raise serializers.ValidationError(
                detail={'error': f"Sizning hisobingizda {sponsor.amount - sponsor_paid_money} sum mavjud"})

        return attrs
    



class StudentSponsorListSerializer(ModelSerializer):
    sponsor = serializers.StringRelatedField(source='sponsor.full_name')

    class Meta:
        model = models.StudentSponsor
        fields = ("id", 'sponsor', 'amount')