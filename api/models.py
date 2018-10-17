from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    """
    A class that represents a Company

    ...

    Attributes
    ----------
    name: str
        the name of the company

    """
    name = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        """
        String representation of any object of the class
        """
        return self.name


class Review(models.Model):
    """
    A class that represents a Review

    ...

    Attributes
    ----------
    rating:int
        The rating of the review, a number between 1 and 5
    title:str
        Title of the review
    summary: str
        Summary of the review
    reviewerIp:str
        The ip of the reviewer
    company:int
        A foreign key that points to the company object
    reviewer:int
        A foreign key that points to the reviewer object
    """
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
        """
        String representation of any object of the class
        """
        return self.title + " " + self.submissionDate.strftime('%d-%m-%Y')

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class Reviewer(models.Model):
    """
    A Class that represents a Reviewer

    ...

    Attributes
    ----------
    name:str
        Name of the reviewer
    email:str
        Email of the reviewer
    user:int
        Foreign key that points to the user object
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Reviewer"
        verbose_name_plural = "Reviewers"

    def __str__(self):
        """
        String representation of the class
        """
        return self.name
