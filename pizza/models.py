from django.db import models
from django.cont import settings
from django.db.models import Manager
from django.utils import timezone
from django.db.models.signal import post_save, m2m_changed
from django.utils.text import get_valid_filename


# Create your models here.


class Address(models.Model):
	full=models.CharField(max_length=150)


	def __str__(self):
		return str(self.full)

class PizzaIngridient(models.Model):
	name=models.CharField(max_length=50)


	def __str__(self):
		return str(self.name)


class PizzaMenuItem(models.Model):
	name = models.CharField(max_length=50)
	ingridients = models.ManyToManyField(
		'PizzaIngridient',
		related_name='menu_Items'
		)


	def __str__(self):
		return str(self.name)


class PizzaSize(models.Model):
	LARGE=('XL', 'LARGE')
	MEDIUM=('MD', 'MEDIUM')
	SMALL=('SM', 'SMALL')
	__all = (LARGE, MEDIUM, SMALL)


	size=models.CharField(max_length=2, choices=__all)


	def __str__(self):
		return str(self.size)


class PizzaOrderManager(Manager):
	def get_queryset(self, **kwargs):
		return super(PizzaOrderManager, self).get_queryset().filter(
				delivered=True
			)


class PizzaOrder(models.Model):
	kind = models.ForeignKey('PizzaMenuItem', related_name='pizzas')
	size = models.ForeignKey('PizzaSize', related_name='pizzas')
	delivery = models.ForeignKey('Address', related_name='pizzas')


	extra = models.ManyToManyField(
		'PizzaIngridiient', blank=True, related_name='pizzas_extra')
	exclude = models.ManyToManyField('PizzaIngridient', blank=True)
	comment = models.CharField(max_length=140, blank = True)


	delivered = models.BooleanField(default=False)
	date_created = models.DateTimeField(default=timezone.now())
	date_delivered = models.DateTimeField(default=None, blank=True)


	objects = Manager()
	delivered_manager = PizzaOrderManager()


	def mark_delivered(self, commit=True):
		self.delivered=True
		self.date_delivered = timezone.now()
		if commit:
			self.save()

	def save(self, **kwargs):
		if not self.pk:
			print('Creating new Pizzaorddr')
		else:
			print('updating existing pizza order')

		super(PizzaOrder, self).save(**kwargs)

	def __str__(self):
		return 'PizzaOreder [%s]' % self.id