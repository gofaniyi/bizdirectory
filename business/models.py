from django.db import models

# Create your models here.


class BusinessCategory(models.Model):
    category = models.ForeignKey(
        to='Category',
        related_name="business_categories",
        on_delete=models.CASCADE,
    )
    business = models.ForeignKey(
        to='Business',
        related_name="business_categories",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            ('category', 'business'),
        )


class Phone(models.Model):
    number = models.CharField(max_length=255)
    business = models.ForeignKey(
        to='Business',
        related_name="business_phones",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.number

class Business(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.CharField(max_length=255)
    contact_email = models.EmailField()
    address = models.TextField()
    categories = models.ManyToManyField(
        to="business.Category",
        through=BusinessCategory,
        related_name="businesses"
    )
    views = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def phones(self):
        return Phone.objects.filter(business_id=self.id).all().values_list('number', flat=True)

    @property
    def categories_list(self):
        return self.categories.all().values()

    @property
    def category_ids(self):
        return self.categories.values_list('id', flat=True)



class Image(models.Model):
    image = models.TextField()
    is_default = models.BooleanField(default=True)
    business = models.ForeignKey(
        to='Business',
        related_name="images",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.image

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


