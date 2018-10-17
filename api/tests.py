from django.urls import reverse
from rest_framework import status
from .models import Company, Review, Reviewer
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
import json
from django.test import Client, TestCase
from rest_framework.authtoken.models import Token
from .serializers import ReviewSerializer, ReviewListSerializer


class ReviewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="firstUser",
            password="firstPassword"
        )
        self.user2 = User.objects.create_user(
            username="secondUser",
            password="secondPassword"
        )
        self.first_reviewer = Reviewer.objects.create(
            user=self.user,
            name="firstReviewer",
            email="firstMail@test.com"
        )
        self.second_reviewer = Reviewer.objects.create(
            user=self.user2,
            name="secondReviewer",
            email="secondMail@test.com"
        )
        self.first_company = Company.objects.create(
            name="firstCompany"
        )
        self.second_company = Company.objects.create(
            name="secondCompany"
        )
        user = json.dumps(
            {"username": "firstUser", "password": "firstPassword"})
        jwt_url = reverse('jwt-create')
        jwt_resp = self.client.post(
            jwt_url, data=user, content_type="application/json")
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT ' + jwt_resp.data["token"])

    def test_get_reviews(self):
        """
        Ensure we can retrieve reviews for the logged user.
        """
        # Testing that returns data for a user with existing reviews

        data = Review(rating=1, summary="mock summary",
                      title="mock title", submissionDate="2018-09-09",
                      reviewerIp='127.0.0.1',
                      reviewer=self.first_reviewer, company=self.first_company)
        data.save()
        review = Review.objects.filter(reviewer__user=self.user)[0]
        review_serializer = ReviewListSerializer(review, many=False)
        response = self.client.get(
            '/v1/api/review/', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(review_serializer.data, response.json()[0])

        # Testing that it doesnt retrieve data for a user without reviews
        user = json.dumps(
            {"username": "secondUser", "password": "secondPassword"})
        client = APIClient()
        jwt_url = reverse('jwt-create')
        jwt_resp = client.post(
            jwt_url, data=user, content_type="application/json")
        client.credentials(HTTP_AUTHORIZATION='JWT ' + jwt_resp.data["token"])
        response = client.get(
            "/v1/api/review/", content_type="application/json")
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_reviews(self):
        # Testing creation of a review
        data = json.dumps({"rating": 1, "summary": "mock summary",
                           "title": "mock title", "submissionDate": "2018-09-09",
                           "reviewer": self.first_reviewer.pk, "company": self.first_company.pk})
        response = self.client.post(
            "/v1/api/review/", data=data, content_type="application/json")
        review = Review.objects.get(pk=response.json()["id"])
        review_serializer = ReviewSerializer(review)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), review_serializer.data)

    def tearDown(self):
        Review.objects.all().delete()
