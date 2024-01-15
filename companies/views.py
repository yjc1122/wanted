# views.py
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Company, Recruitment
from .serializers import CompanySerializer, RecruitmentSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class RecruitmentViewSet(viewsets.ModelViewSet):
    queryset = Recruitment.objects.all()
    serializer_class = RecruitmentSerializer

    def filter_queryset(self, queryset):
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(Q(position__icontains=search) | Q(skills=search))
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        company_recruitments_ids = self.get_queryset().filter(
            company_id=instance.company_id
        ).values_list('id', flat=True)

        setattr(instance, 'recruitment_ids', company_recruitments_ids)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    # todo 회사 정보 가져오는 action 추가 하기
    @action(detail=True, methods=['get'])
    def company_recruitments(self, request, pk=None):
        obj = self.get_object()
        company = obj.company
        # select_related와 values_list를 사용하여 관련된 Company 정보 중 id만 가져오기
        recruitment_ids = (
            Recruitment.objects
            .filter(company=company)
            .select_related('company')
            .values_list('id', flat=True)
        )

        # 결과를 JSON 형태로 반환
        return JsonResponse(list(recruitment_ids), safe=False)
