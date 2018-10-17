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
        Checking that rating its between 1-5
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
