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
        url = get_url("api/materials/{}/".format(self.material_2.id))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
# ----------------------------------------------------------------------

class LaborApiTestCase(APITestCase):
    def setUp(self):
        self.user_3 = User.objects.create(login='test user 1', password='1111')

        self.product_1 = Product.objects.create(product_name='test product 1', currency='BYN',
                                                output_volume='12', period="3", sale_price="1141",
                                                cost_price="0", return_on_sales="100", breakeven_point="0",
                                                user_id = self.user_3)

        self.labor_1 = Labor_costs.objects.create(profession='test labor 1',
                                                number_of_people='5', salary="50", deduction="5",
                                                  total_price="26.25", product_id = self.product_1)

        self.labor_2 = Labor_costs.objects.create(profession='test labor 2',
                                                  number_of_people='12', salary="12", deduction="1",
                                                  total_price="9.70", product_id=self.product_1)

    def test_get(self):
        url = get_url("api/labors/")
        response = self.client.get(url)
        serializer_data = LaborSerializer([self.labor_1, self.labor_2], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = get_url("api/labors/")
        data = {
            "profession": "labor",
            "number_of_people": "5",
            "salary": "50",
            "deduction": "5",
            "product_id": self.product_1.id
        }
        kol = Labor_costs.objects.all().count() + 1
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(kol, Labor_costs.objects.all().count())
        self.assertEqual("26.25", response.data["total_price"])

    def test_put(self):
        url = get_url("api/labors/{}/".format(self.labor_1.id))
        data = {
            "profession": self.labor_1.profession,
            "number_of_people": self.labor_1.number_of_people,
            "salary": "500",
            "deduction": self.labor_1.deduction,
            "product_id": self.product_1.id
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.labor_1.refresh_from_db()
        self.assertEqual(500.00, self.labor_1.salary)
        self.assertEqual(262.50, self.labor_1.total_price)

    def test_delete(self):
        url = get_url("api/labors/{}/".format(self.labor_2.id))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

# ----------------------------------------------------------------------

class AmortizationApiTestCase(APITestCase):
    def setUp(self):
        self.user_3 = User.objects.create(login='test user 1', password='1111')

        self.product_1 = Product.objects.create(product_name='test product 1', currency='BYN',
                                                output_volume='12', period="3", sale_price="1141",
                                                cost_price="0", return_on_sales="100", breakeven_point="0",
                                                user_id = self.user_3)

        self.amortization_1 = Amortization_costs.objects.create(equipment_name='test amortization 1',
                                                count_equipment='5', cost="500", service_life="5",
                                                  total_price="4.11", product_id = self.product_1)

        self.amortization_2 = Amortization_costs.objects.create(equipment_name='test amortization 2',
                                                                count_equipment='3', cost="300", service_life="5",
                                                                total_price="1.48", product_id=self.product_1)

    def test_get(self):
        url = get_url("api/amortizations/")
        response = self.client.get(url)
        serializer_data = AmortizationSerializer([self.amortization_1, self.amortization_2], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = get_url("api/amortizations/")
        data = {
            "equipment_name": "amortization",
            "count_equipment": "5",
            "cost": "500",
            "service_life": "5",
            "product_id": self.product_1.id
        }
        kol = Amortization_costs.objects.all().count() + 1
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(kol, Amortization_costs.objects.all().count())
        self.assertEqual("4.11", response.data["total_price"])

    def test_put(self):
        url = get_url("api/amortizations/{}/".format(self.amortization_1.id))
        data = {
            "equipment_name": self.amortization_1.equipment_name,
            "count_equipment": self.amortization_1.count_equipment,
            "cost": "1250",
            "service_life": "6",
            "product_id": self.product_1.id
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.amortization_1.refresh_from_db()
        self.assertEqual(1250.00, self.amortization_1.cost)
        self.assertEqual(6, self.amortization_1.service_life)
        tot_pr = str(self.amortization_1.total_price)
        self.assertEqual("8.56", tot_pr)


    def test_delete(self):
        url = get_url("api/amortizations/{}/".format(self.amortization_2.id))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

# ----------------------------------------------------------------------

class InvoiceApiTestCase(APITestCase):
    def setUp(self):
        self.user_3 = User.objects.create(login='test user 1', password='1111')

        self.product_1 = Product.objects.create(product_name='test product 1', currency='BYN',
                                                output_volume='12', period="3", sale_price="1141",
                                                cost_price="0", return_on_sales="100", breakeven_point="0",
                                                user_id = self.user_3)

        self.invoice_1 = Invoice_costs.objects.create(invoice_name='test invoice 1',
                                                count='3', cost="4", total_price="12",
                                                product_id = self.product_1)

        self.invoice_2 = Invoice_costs.objects.create(invoice_name='test invoice 2',
                                                      count='5', cost="6", total_price="30",
                                                      product_id=self.product_1)

    def test_get(self):
        url = get_url("api/invoices/")
        response = self.client.get(url)
        serializer_data = InvoiceSerializer([self.invoice_1, self.invoice_2], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = get_url("api/invoices/")
        data = {
            "invoice_name": "invoice 3",
            "count": "3",
            "cost": "6",
            "product_id": self.product_1.id
        }
        kol = Invoice_costs.objects.all().count() + 1
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(kol, Invoice_costs.objects.all().count())
        self.assertEqual("18.00", response.data["total_price"])

    def test_put(self):
        url = get_url("api/invoices/{}/".format(self.invoice_1.id))
        data = {
            "invoice_name": self.invoice_1.invoice_name,
            "count": "15",
            "cost": "3",
            "product_id": self.product_1.id
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.invoice_1.refresh_from_db()
        self.assertEqual(15, self.invoice_1.count)
        self.assertEqual(3, self.invoice_1.cost)
        self.assertEqual(45.00, self.invoice_1.total_price)

    def test_delete(self):
        url = get_url("api/invoices/{}/".format(self.invoice_2.id))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)