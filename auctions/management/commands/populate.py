from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from auctions.models import Category, Item, Auction


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Admin user
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password("admin")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Admin user created."))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists."))

        # Test user
        test_user, created = User.objects.get_or_create(
            username="testuser",
            defaults={
                "email": "testuser@example.com",
                "first_name": "Test",
                "last_name": "User",
                "birth_date": "1990-01-01",
                "phone_number": "1234567890",
            },
        )
        if created:
            test_user.set_password("password")
            test_user.save()
            self.stdout.write(self.style.SUCCESS("Test user created."))
        else:
            self.stdout.write(self.style.WARNING("Test user already exists."))

        self.stdout.write(self.style.SUCCESS("Finished populating the database."))

        # Categoria
        category = Category.objects.create(name="Homens peludos")
        category2 = Category.objects.create(name="Homens belos")

        # Item de Leilão
        for i in range(5):
            item = Item.objects.create(
                name="Davazoko",
                description="Um homem de qualidade e pé preto",
                category=category,
                starting_bid=150.00,
                max_bid=1000.00,
            )

        for i in range(5):
            item2 = Item.objects.create(
                name="AmorSurreal",
                description="Aquele que encanta todas as mulheres, com um corpo perfeito e uma voz sedutora",
                category=category2,
                starting_bid=150.00,
                max_bid=1000.00,
            )

        # Leilão
        Auction.objects.create(
            item=item,
            owner=admin,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1),
            current_price=150.00,
            status="ATIVO",
        )
        Auction.objects.create(
            item=item2,
            owner=admin,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=1),
            current_price=150.00,
            status="ATIVO",
        )

        print("Dados de exemplo criados com sucesso!")
