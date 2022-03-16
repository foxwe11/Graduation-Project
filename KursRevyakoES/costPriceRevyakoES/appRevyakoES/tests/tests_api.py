from rest_framework.test import APITestCase
from appRevyakoES.serializers import *
from rest_framework import status
from django.test import TestCase, Client
import json


def get_url(str):
    return "http://127.0.0.1:8000/" + str


class UserApiTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(login='test user 1', password='1111')
        self.user_2 = User.objects.create(login='test user 2', password='2222')

    def test_get(self):
        url = get_url("api/users/")
        response = self.client.get(url)
        serializer_data = UserSerializer([self.user_1, self.user_2], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = get_url("api/users/")
        data = {
            "login": "test user 1",
            "password": 1111
        }
        kol = User.objects.all().count() + 1
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(kol, User.objects.all().count())

    def test_put(self):
        url = get_url("api/users/{}/".format(self.user_1.id))
        data = {
            "login": self.user_1.login,
            "password": 3333
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user_1.refresh_from_db()
        self.assertEqual('3333', self.user_1.password)

    def test_delete(self):
        url = get_url("api/users/{}/".format(self.user_2.id))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


# ----------------------------------------------------------------------

class ProductApiTestCase(APITestCase):
    def setUp(self):
        self.user_3 = User.objects.create(login='test user 1', password='1111')

        self.product_1 = Product.objects.create(product_name='test product 1', currency='BYN',
                                                output_volume='12', period="3", sale_price="1141",
                                                cost_price="0", return_on_sales="100", breakeven_point="0",
                                                user_id = self.user_3)

        self.product_2 = Product.objects.create(product_name='test product 2', currency='BYN',
                                                output_volume='35', period="20", sale_price="200",
                                                cost_price="0", return_on_sales="100", breakeven_point="0",
                                                user_id = self.user_3)

    def test_get(self):
        url = get_url("api/products/")
        response = self.client.get(url)
        serializer_data = ProductSerializer([self.product_1, self.product_2], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = get_url("api/products/")
        data = {
            "product_name": "test prod 11",
            "currency": "USD",
            "output_volume": "40",
            "period": "15",
            "sale_price": "333",
            "user_id": self.user_3.id
        }
        kol = Product.objects.all().count() + 1
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(kol, Product.objects.all().count())

    def test_put(self):
        url = get_url("api/products/{}/".format(self.product_1.id))
        data = {
            "product_name": self.product_1.product_name,
            "currency": self.product_1.currency,
            "output_volume": self.product_1.output_volume,
            "period": self.product_1.period,
            "sale_price": "3666",
            "user_id": self.user_3.id
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.product_1.refresh_from_db()
        self.assertEqual(3666.00, self.product_1.sale_price)

    def test_delete(self):
        url = get_url("api/products/{}/".format(self.product_2.id))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
# ----------------------------------------------------------------------

class MaterialApiTestCase(APITestCase):
    def setUp(self):
        self.user_3 = User.objects.create(login='test user 1', password='1111')

        self.product_1 = Product.objects.create(product_name='test product 1', currency='BYN',
                                                output_volume='12', period="3", sale_price="1141",
                                                cost_price="0", return_on_sales="100", breakeven_point="0",
                                                user_id = self.user_3)

        self.material_1 = Material_costs.objects.create(material_name='test material 1',
                                                count='3', cost="4", total_price="12",
                                                product_id = self.product_1)

        self.material_2 = Material_costs.objects.create(material_name='test material 2',
                                         count='3', cost="5", total_price="15",
                                         product_id=self.product_1)

    def test_get(self):
        url = get_url("api/materials/")
        response = self.client.get(url)
        serializer_data = MaterialSerializer([self.material_1, self.material_2], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = get_url("api/materials/")
        data = {
            "material_name": "test mat 3",
            "count": "5",
            "cost": "6",
            "product_id": self.product_1.id
        }
        kol = Material_costs.objects.all().count() + 1
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(kol, Material_costs.objects.all().count())
        self.assertEqual("30.00", response.data["total_price"])

    def test_put(self):
        url = get_url("api/materials/{}/".format(self.material_1.id))
        data = {
            "material_name": self.material_1.material_name,
            "count": "7",
            "cost": "8",
            "product_id": self.product_1.id
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.material_1.refresh_from_db()
        self.assertEqual(7, self.material_1.count)
        self.assertEqual(8, self.material_1.cost)
        self.assertEqual(56.00, self.material_1.total_price)

    def test_delete(self):
        url = get_url("api/materials/{}".format(self.material_2.id))
        url = url + "/"
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
# ----------------------------------------------------------------------

