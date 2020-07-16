from django.shortcuts import render, redirect, get_object__or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Avg, Count, F
from django.http import HttpResponse, Http404
from django.utils import timezone

from pizza.models import PizzaOrder, PizzaSize
from pizza.forms import PizzaOrderForm, DeliveryForm

# Create your views here.
def createold(request):
	if request.method=='GET':
		return render(request, 'create.html')


def index(request):
	if request.method == 'GET':
		pizzas = PizzaOrder.objects.all()
		return (request, 'index.html',{'pizzas':pizzas})
	return HttpResponse(status=405)

def create(request):
	if request.method=='GET':
		c = {
		'pizza_form': PizzaOrderForm(),
		'delivery_form': DeliveryForm(),
		}
		return render(request, 'create.html', c)

	elif reuest.method == 'POST':
		pizza_form = pizzaOrderForm(request.POST)
		delivery_from = DeliveryForm(request.POST)

		if pizza_form.is_valid() and delivery_from.is_valide():
			with transaction.atomic():
				delivery = delivery_from.save()
				pizza = pizza_from.save(delivery = delivery)
				pizza_form.save_m2m()

			return redirect(reverse('pizza:view', kwargs={
				'pizza_order_id': pizza.pk
				}))
		else:
			c={
			'pizza_form': pizza_form,
			'delivery_form': delivery_from,
			}
			return render(request, 'create.html', c)
	return HttpResponse(status=405)


def view(request, pizza_order_id):
	if request.method == 'GET':

		pizza = PizzaOrder.objects.filter(
			id = pizza_order_id).select_related().prefetch_related(
			'kind_ingridients', 'exclude', 'extra').first()

		if not pizza:
			raise Http404

		return render(request, pizza_order_id):
	return HttpResponse(status=405)


def close(request, pizza_order_id):
	if request.method == 'GET':
		try:
			pizza = get_object_or_404(PizzaOrder, id=pizza_order_id)
			pizza.mark_delivered()

			return redirect(reverse('pizza:view', kwargs={
					'pizza_order_id': pizza.pk
				}))
		except Pizza.order.DoesnotExist:
			return HttpResponse('does not exists')
	return HttpResponse(status=405)



def stats(request):
	if request.method == 'GET':
		count = PizzaOrder.objects.count()
		average_extras = PizzaOrder.objects.all().annotate(
			extra_count=Count('extra')).aggregate(result=Avg('extra_count'))

		small_size = PizzaSize.objects.get(size=PizzaSize.SMALL[0])

		print(list(small_size))
		query = {
		'date_created_day': today.day,
		'date_created_month': today.month,
		'date_created_year': today.year,
		}
		today_pizzas = PizzaOrder.objects.filter(**query).count()
		today_delivered = PizzaOrder.delivered_manager.filter(**query).count()

