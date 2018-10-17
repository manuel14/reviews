from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Review(models.Model):
    rating = models.IntegerField()
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=10000)
    reviewerIp = models.GenericIPAddressField()
    submissionDate = models.DateField(auto_now_add=False, auto_now=False)
    company = models.ForeignKey(
        Company, related_name="reviews", on_delete=models.DO_NOTHING)
    reviewer = models.ForeignKey(
        "Reviewer", related_name="reviews", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title + " " + self.submissionDate.strftime('%d-%m-%Y')

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
    


class Reviewer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Reviewer"
        verbose_name_plural = "Reviewers"

    def __str__(self):
        return self.name
