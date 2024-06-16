# Standard Library Imports
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator

# Third-party Imports
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Local App Imports
from apps.child.models import Child
from apps.staff.models import Staff


# Constant for the sponsorship types
class SponsorshipType:
    CHILD_FULL_SUPPORT = 'Child full support'
    CHILD_CO_SUPPORT = 'Child co-support'
    FAMILY_FULL_SUPPORT = 'Family full support'
    FAMILY_CO_SUPPORT = 'Family co-support'
    GENERAL_SUPPORT = 'General support'

SPONSORSHIP_TYPE_CHOICES = (
    ('', 'Sponsorship Type'),
    (SponsorshipType.CHILD_FULL_SUPPORT, 'Child full support'),
    (SponsorshipType.CHILD_CO_SUPPORT, 'Child co-support'),
    (SponsorshipType.FAMILY_FULL_SUPPORT, 'Family full support'),
    (SponsorshipType.FAMILY_CO_SUPPORT, 'Family co-support'),
    (SponsorshipType.GENERAL_SUPPORT, 'General support'),
)


# =================================== SPONSOR MODEL ===================================
class Sponsor(models.Model):
    DEPARTURE_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    first_name = models.CharField(max_length=25, null=True, verbose_name="First Name")
    last_name = models.CharField(max_length=25, null=True, verbose_name="Last Name")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=False,
                               verbose_name="Gender")
    email = models.EmailField(verbose_name="Email")
    sponsorship_type_at_signup = models.CharField(
        max_length=20, choices=SPONSORSHIP_TYPE_CHOICES, null=True, blank=True, 
        verbose_name="Type of Sponsorship Interest")
    job_title = models.CharField(max_length=30, null=True, verbose_name="Job Title")
    region = models.CharField(max_length=30, null=True, verbose_name="Region")
    town = models.CharField(max_length=30, null=True, verbose_name="Town")
    origin = models.CharField(max_length=30, null=True, verbose_name="Origin")
    business_telephone = PhoneNumberField(null=True, blank=True, default="+256999999999",
                                           verbose_name="Business Telephone")
    mobile_telephone = PhoneNumberField(null=True, blank=True, default="+256999999999",
                                         verbose_name="Mobile Telephone")
    city = models.CharField(max_length=30, null=True, verbose_name="City")
    start_date = models.DateField(null=True, blank=True,
                                  verbose_name="Start Date",
                                  validators=[
                                      MinValueValidator(limit_value=datetime.date(year=2013, month=1, day=1)),
                                      MaxValueValidator(limit_value=datetime.date.today())
                                  ])
    first_street_address = models.CharField(max_length=100, null=True, verbose_name="First Street Address")
    second_street_address = models.CharField(max_length=100, null=True, verbose_name="Second Street Address")
    zip_code = models.CharField(max_length=10, null=True, verbose_name="ZIP Code")
    is_departed = models.BooleanField(
        default=False,
        verbose_name="Departed?",
    )
    comment = models.CharField(max_length=50, null=True, verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'sponsor_details'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def prefixed_id(self):
        return f"PS-0{self.pk}"
    
# =================================== SPONSOR DEPARTURE MODEL ===================================

class SponsorDeparture(models.Model):
    sponsor = models.ForeignKey(
        'Sponsor',
        on_delete=models.CASCADE,
        verbose_name='Sponsor Information', 
        related_name='departures'
    )
    departure_date = models.DateField(verbose_name='Departure Date', null=True, blank=True)
    departure_reason = models.TextField(verbose_name='Reason for Departure')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Sponsor Departure'
        verbose_name_plural = 'Sponsor Departures'


# =================================== CHILD SPONSORSHIP MODEL ===================================
class ChildSponsorship(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsored_children')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='sponsorships_received')
    sponsorship_type = models.CharField(
        max_length=20, choices=SPONSORSHIP_TYPE_CHOICES, null=True, blank=True, verbose_name="Sponsorship Type"
    )
    start_date = models.DateField(null=True, blank=True, verbose_name="Start Date")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = 'child_sponsorship_details'
        verbose_name_plural = 'Child Sponsorships'
        unique_together = (('child', 'sponsor'),)

    def __str__(self):
        return f"{self.child} sponsored by {self.sponsor}"
    

# =================================== STAFF SPONSORSHIP MODEL ===================================
class StaffSponsorship(models.Model):
    sponsor = models.ForeignKey('Sponsor', on_delete=models.CASCADE, verbose_name="Sponsor", 
                                related_name='sponsored_staff')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='sponsorships_received')
    sponsorship_type = models.CharField(
        max_length=20, choices=SPONSORSHIP_TYPE_CHOICES, null=True, blank=True, verbose_name="Sponsorship Type"
    )
    start_date = models.DateField(null=True, blank=True, verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = 'staff_sponsorship'
        verbose_name_plural = 'Staff Sponsorships'
        unique_together = (('staff', 'sponsor'),)

    def __str__(self):
        return f"{self.staff} sponsored by {self.sponsor}"