
from . import serializers
from . import models
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView, Response
from django.db.models import Sum

class StudentListAPIView(ListAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('student_type', 'university')
    search_fields = ('full_name',)


class StudentDetailAPIView(RetrieveUpdateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentDetailSerializer


class StudentSponsorCreateAPIView(CreateAPIView):
    queryset = models.StudentSponsor.objects.all()
    serializer_class = serializers.StudentSponsorSerializer



class StudentSponsorListAPIView(ListAPIView):
    queryset = models.StudentSponsor.objects.all()
    serializer_class = serializers.StudentSponsorListSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ('student',)


class StatisticAPIView(APIView):

    def get(self, request):
        total_paid_amount = models.StudentSponsor.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_required_amount = models.Student.objects.aggregate(total=Sum('contract_amount'))['total'] or 0
        total_unpaid_amount = total_required_amount - total_paid_amount
        return Response(
            data={
            "total_paid_amount": total_paid_amount,
            "total_required_amount": total_required_amount,
            "total_unpaid_amount": total_unpaid_amount
        })



class GraphicAPIView(APIView):

    def get(self, request):
        from datetime import datetime
        this_year = datetime.now().year

        # yanvar sponsor
        result = []
        for i in range(1, 13):
            sponsor_amount = models.Sponsor.objects.filter(
                created_at__month=i, 
                created_at__year=this_year, 
                status='apporved'
            ).aggregate(total=Sum('amount'))['total'] or 0

            student_amount = models.Student.objects.filter(
                created_at__month=i, 
                created_at__year=this_year, 
            ).aggregate(total=Sum('contract_amount'))['total'] or 0
            result.append({
                "month": i,
                "sponsor_amount" : sponsor_amount,
                "student_amount": student_amount
            })
        return Response(result)


