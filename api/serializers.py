from rest_framework import serializers
from .models import *


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('__all__')


class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewer
        fields = ('__all__')


class ReviewSerializer(serializers.ModelSerializer):

    def validate_rating(self, value):
        """
        A function that checks that the rating value is between 1 and 5

        Parameters
        ----------
        self:int
            The current serializer object
        value:int
            Rating number of the review
        Returns
        -------
        int
            The value of the rating
        str
            ValidationError
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    class Meta:
        model = Review
        fields = ('__all__')


class ReviewListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False, required=True)
    reviewer = ReviewerSerializer(many=False, required=True)

    class Meta:
        model = Review
        fields = ('title', 'reviewer', 'company',
                  'rating', 'summary', 'submissionDate')
