from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from auctions.models import Category, Item, Auction


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Usuário de teste
        user, created = User.objects.get_or_create(username="admin", defaults={
            "email": "admin@admin.com",
            "is_staff": True,
            "is_superuser": True
        })

        if created:
            user.set_password("admin")
            user.save()

        # Categoria
        category = Category.objects.create(name="Homens peludos")

        # Item de Leilão
        item = Item.objects.create(
            name="Davazoko",
            description="Um homem de qualidade e pé preto",
            category=category,
            starting_bid=150.00,
            max_bid=1000.00,
        )

        # Leilão
        auction = Auction.objects.create(
            item=item,
            owner=user,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1),
            current_price=150.00,
            status="ATIVO",
        )

        print("Dados de exemplo criados com sucesso!")
