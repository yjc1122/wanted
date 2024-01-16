from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Company, Recruitment

User = get_user_model()


class CompanyTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_company(self):
        url = '/companies/'
        data = {
            'name': '카카오',
            'description': '라이언과 친구들',
            'scale': 3

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, '카카오')

    def test_create_recruitment(self):
        url = '/recruitments/'
        company = Company.objects.create(
            name='카카오',
            description='라이언과 친구들',
            scale=3
        )
        data = {
            'company': company.id,
            'position': '백엔드 개발자',
            'reward': '500000',
            'description': '신규 사업 개발 담당자 구인',
            'skills': 'Django DRF'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Recruitment.objects.count(), 1)
        self.assertEqual(Recruitment.objects.get().reward, 500000)
