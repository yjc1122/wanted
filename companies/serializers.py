# serializers.py
from rest_framework import serializers
from .models import Company, Recruitment


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Company
        fields = (
            'name',
            'description',
            'scale'
        )

    def validate(self, attrs):
        attrs.pop('name')
        return attrs


class CompanyNameSerializer(serializers.Serializer):
    name = serializers.CharField(source='company__name')
    scale = serializers.IntegerField(source='company__scale')


class RecruitmentSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_desc = serializers.CharField(source='company.description', read_only=True)
    recruitment_ids = serializers.ListSerializer(child=serializers.IntegerField())

    class Meta:
        model = Recruitment
        fields = (
            'id',
            'company',
            'company_name',
            'company_desc',
            'position',
            'reward',
            'description',
            'skills',
            'recruitment_ids'
        )

    # def get_other_recruitments(self, obj):
    #     ids = obj.company_recruitments.values_list('id', flat=True)
    #     return ids

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     company_id = representation['company']
    #
    #     # 같은 회사의 다른 채용공고의 ID들만 가져오기
    #     other_recruitment_ids = (
    #         Recruitment.objects
    #         .filter(company__id=company_id)
    #         .exclude(id=instance.id)
    #         .values_list('id', flat=True)
    #     )
    #
    #     representation['other_recruitment_ids'] = list(other_recruitment_ids)
    #
    #     return representation


