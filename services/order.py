from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from django.contrib.auth import get_user_model



@transaction.atomic
def create_order(tickets: list, username: str, date=None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"]
        )
    return order

def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = Order.objects.filter(user__username=username)
    return queryset