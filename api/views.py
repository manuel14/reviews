from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponseForbidden
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import detail_route, list_route
from rest_framework.status import HTTP_201_CREATED


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class ReviewerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewerSerializer
    queryset = Reviewer.objects.all()


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    def create(self, request):
        """
        Creates 1 or more reviews objects.
        """
        # retrieving ip from request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:# pragma: no cover
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        # looping request.data if its a list or setting directly if its a dict the ip attr
        reviewer = Reviewer.objects.get(user=request.user).pk
        if (isinstance(request.data, list)):
            for rev in request.data:
                rev["reviewerIp"] = ip
                rev["reviewer"] = reviewer
        else:
            request.data["reviewerIp"] = ip
            request.data["reviewer"] = reviewer
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self, *args, **kwargs):
        """
        Defines wich serializer to use depending on the action dispatched.
        """
        if self.action in ["list", "retrieve"]:
            return ReviewListSerializer
        else:
            return ReviewSerializer

    def list(self, request):
        """
        Returns all reviews for the logged-in user.
        """
        data = Review.objects.filter(reviewer__user=request.user)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieves a single Review if the logged-in user is the author.
        """
        try:
            review = Review.objects.get(pk=pk, reviewer__user=request.user)
            serializer = self.get_serializer(review, many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('The review does not exist or your not the author')
