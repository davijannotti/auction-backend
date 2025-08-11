from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from auctions.models import Category, Item, Auction, Bid


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Create admin user
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "birth_date": "1990-01-01",
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

        # Create test users
        test_user1, created = User.objects.get_or_create(
            username="testuser1",
            defaults={
                "email": "testuser1@example.com",
                "first_name": "Test1",
                "last_name": "User1",
                "birth_date": "1995-05-15",
                "phone_number": "1234567890",
            },
        )
        if created:
            test_user1.set_password("password")
            test_user1.save()
            self.stdout.write(self.style.SUCCESS("Test user created."))
        else:
            self.stdout.write(self.style.WARNING("Test user already exists."))

        test_user2, created = User.objects.get_or_create(
            username="testuser2",
            defaults={
                "email": "testuser2@example.com",
                "first_name": "Test2",
                "last_name": "User2",
                "birth_date": "1995-05-15",
                "phone_number": "1234567890",
            },
        )
        if created:
            test_user2.set_password("password")
            test_user2.save()
            self.stdout.write(self.style.SUCCESS("Test user created."))
        else:
            self.stdout.write(self.style.WARNING("Test user already exists."))

        # Create categories
        category1, created = Category.objects.get_or_create(
            name="Eletrônicos",
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Category '{category1.name}' created.")
            )

        category2, created = Category.objects.get_or_create(
            name="Arte e Antiguidades",
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Category '{category2.name}' created.")
            )

        category3, created = Category.objects.get_or_create(
            name="Veículos",
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Category '{category3.name}' created.")
            )

        # Create auctions first
        auction1, created = Auction.objects.get_or_create(
            name="Leilão de Eletrônicos Premium",
            defaults={
                "owner": admin,
                "start_time": timezone.now(),
                "end_time": timezone.now(),
                "status": "AGUARDANDO",
                "category": category1,
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Auction '{auction1.name}' created."))

        auction2, created = Auction.objects.get_or_create(
            name="Leilão de Arte Clássica",
            defaults={
                "owner": test_user1,
                "start_time": timezone.now(),
                "end_time": timezone.now(),
                "status": "ATIVO",
                "category": category2,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Auction '{auction2.name}' created."))

        auction3, created = Auction.objects.get_or_create(
            name="Leilão de Carros Antigos",
            defaults={
                "owner": admin,
                "start_time": timezone.now(),
                "end_time": timezone.now(),
                "status": "ENCERRADO",
                "category": category3,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Auction '{auction3.name}' created."))

        auction4, created = Auction.objects.get_or_create(
            name="Leilão",
            defaults={
                "owner": admin,
                "start_time": timezone.now(),
                "end_time": timezone.now(),
                "status": "CANCELADO",
                "category": category3,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Auction '{auction3.name}' created."))

        # Create items for auction1 (Electronics)
        item1, created = Item.objects.get_or_create(
            name="iPhone 15 Pro Max",
            defaults={
                "description": "iPhone 15 Pro Max 256GB em perfeito estado, com todos os acessórios originais.",
                "starting_bid": 4500.00,
                "max_bid": 8000.00,
                "current_bid": 4500.00,
                "auction": auction1,
                "owner": test_user1,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Item '{item1.name}' created."))

        item2, created = Item.objects.get_or_create(
            name="MacBook Pro M3",
            defaults={
                "description": "MacBook Pro 14 polegadas com chip M3, 16GB RAM, 512GB SSD. Usado por apenas 6 meses.",
                "starting_bid": 8000.00,
                "max_bid": 15000.00,
                "current_bid": 8000.00,
                "auction": auction1,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Item '{item2.name}' created."))

        # Create items for auction2 (Art)
        item3, created = Item.objects.get_or_create(
            name="Pintura a Óleo Vintage",
            defaults={
                "description": "Pintura a óleo de paisagem do século XIX, moldura original em madeira entalhada.",
                "starting_bid": 2500.00,
                "max_bid": 10000.00,
                "current_bid": 2800.00,
                "auction": auction2,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Item '{item3.name}' created."))

        item4, created = Item.objects.get_or_create(
            name="Escultura de Bronze",
            defaults={
                "description": "Escultura em bronze representando figura clássica, altura 45cm, base em mármore.",
                "starting_bid": 1800.00,
                "max_bid": 5000.00,
                "current_bid": 1800.00,
                "auction": auction2,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Item '{item4.name}' created."))

        # Create items for auction3 (Vehicles)
        item5, created = Item.objects.get_or_create(
            name="Volkswagen Fusca 1975",
            defaults={
                "description": "Fusca 1975 completamente restaurado, motor 1600, cor azul original.",
                "starting_bid": 25000.00,
                "max_bid": 50000.00,
                "current_bid": 25000.00,
                "auction": auction3,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Item '{item5.name}' created."))

        # Create bids
        bid1, created = Bid.objects.get_or_create(
            user=test_user1,
            item=item1,
            amount=2800.00,
        )
        if created:
            # Update item's current bid
            item3.current_bid = 2800.00
            item3.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Bid created: {test_user1.username} -> ${bid1.amount} on {item3.name}"
                )
            )

        bid2, created = Bid.objects.get_or_create(
            user=test_user2,
            item=item1,
            amount=4800.00,
        )
        if created:
            # Update item's current bid
            item1.current_bid = 4800.00
            item1.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Bid created: {test_user2.username} -> ${bid2.amount} on {item1.name}"
                )
            )

        bid3, created = Bid.objects.get_or_create(
            user=test_user2,
            item=item5,
            amount=27000.00,
        )
        if created:
            # Update item's current bid
            item5.current_bid = 27000.00
            item5.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Bid created: {admin.username} -> ${bid3.amount} on {item5.name}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS("Database populated successfully with sample data!")
        )
