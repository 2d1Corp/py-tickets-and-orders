from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from django.contrib.auth import get_user_model
from django.utils import timezone

@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(
        user=user,
        created_at=date if date else timezone.now()
    )
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
        queryset = queryset.filter(user__username=username)
    return queryset
