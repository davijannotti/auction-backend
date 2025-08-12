from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from auctions.models import Category, Item, Auction, Bid


class Command(BaseCommand):
    help = "Popula o banco com usuários, categorias, leilões, itens e lances variados"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Usuários
        users_data = [
            {"username": "admin", "email": "admin@example.com", "first_name": "Admin", "last_name": "User", "birth_date": "1990-01-01", "is_staff": True, "is_superuser": True, "password": "admin"},
            {"username": "alice", "email": "alice@example.com", "first_name": "Alice", "last_name": "Wonder", "birth_date": "1992-03-12", "phone_number": "11122233344", "password": "password"},
            {"username": "bob", "email": "bob@example.com", "first_name": "Bob", "last_name": "Builder", "birth_date": "1985-07-09", "phone_number": "22233344455", "password": "password"},
            {"username": "carol", "email": "carol@example.com", "first_name": "Carol", "last_name": "Smith", "birth_date": "1998-11-22", "phone_number": "33344455566", "password": "password"},
            {"username": "dave", "email": "dave@example.com", "first_name": "Dave", "last_name": "Jones", "birth_date": "1978-01-30", "phone_number": "44455566677", "password": "password"},
            {"username": "eve", "email": "eve@example.com", "first_name": "Eve", "last_name": "Adams", "birth_date": "1995-05-15", "phone_number": "55566677788", "password": "password"},
        ]

        users = {}
        for udata in users_data:
            user, created = User.objects.get_or_create(
                username=udata["username"],
                defaults={
                    "email": udata["email"],
                    "first_name": udata["first_name"],
                    "last_name": udata["last_name"],
                    "birth_date": udata["birth_date"],
                    "phone_number": udata.get("phone_number"),
                    "is_staff": udata.get("is_staff", False),
                    "is_superuser": udata.get("is_superuser", False),
                },
            )
            if created:
                user.set_password(udata["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Usuário '{user.username}' criado."))
            else:
                self.stdout.write(self.style.WARNING(f"Usuário '{user.username}' já existe."))
            users[user.username] = user

        # Categorias
        categories_data = [
            "Eletrônicos",
            "Arte e Antiguidades",
            "Veículos",
            "Móveis",
            "Livros",
        ]
        categories = {}
        for cname in categories_data:
            category, created = Category.objects.get_or_create(name=cname)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Categoria '{cname}' criada."))
            else:
                self.stdout.write(self.style.WARNING(f"Categoria '{cname}' já existe."))
            categories[cname] = category

        now = timezone.now()

        # Leilões
        auctions_data = [
            {"name": "Leilão de Eletrônicos Premium", "owner": users["admin"], "category": categories["Eletrônicos"], "status": "AGUARDANDO"},
            {"name": "Leilão de Arte Clássica", "owner": users["alice"], "category": categories["Arte e Antiguidades"], "status": "ATIVO"},
            {"name": "Leilão de Carros Antigos", "owner": users["bob"], "category": categories["Veículos"], "status": "ENCERRADO"},
            {"name": "Leilão de Móveis Raros", "owner": users["carol"], "category": categories["Móveis"], "status": "ENCERRADO"},
            {"name": "Leilão de Livros Históricos", "owner": users["dave"], "category": categories["Livros"], "status": "CANCELADO"},
            {"name": "Leilão Geral", "owner": users["eve"], "category": categories["Eletrônicos"], "status": "ATIVO"},
        ]

        auctions = {}
        for adata in auctions_data:
            auction, created = Auction.objects.get_or_create(
                name=adata["name"],
                defaults={
                    "owner": adata["owner"],
                    "category": adata["category"],
                    "start_time": now,
                    "end_time": now + timezone.timedelta(days=7),
                    "status": adata["status"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Leilão '{auction.name}' criado."))
            else:
                self.stdout.write(self.style.WARNING(f"Leilão '{auction.name}' já existe."))
            auctions[auction.name] = auction

        # Itens para os leilões (nome, descrição, bids mínimo e máximo, dono)
        items_data = [
            # Eletrônicos - Leilão 1
            {"name": "iPhone 15 Pro Max", "description": "iPhone 15 Pro Max 256GB, novo.", "starting_bid": 4500, "max_bid": 9000, "current_bid": 4500, "auction": auctions["Leilão de Eletrônicos Premium"], "owner": users["alice"]},
            {"name": "MacBook Pro M3", "description": "MacBook Pro 14\" com chip M3.", "starting_bid": 8000, "max_bid": 15000, "current_bid": 8000, "auction": auctions["Leilão de Eletrônicos Premium"], "owner": None},
            {"name": "Samsung QLED TV 65\"", "description": "TV QLED 65 polegadas, 4K.", "starting_bid": 3500, "max_bid": 7000, "current_bid": 3500, "auction": auctions["Leilão de Eletrônicos Premium"], "owner": None},

            # Arte Clássica - Leilão 2
            {"name": "Pintura a Óleo Vintage", "description": "Pintura a óleo século XIX.", "starting_bid": 2500, "max_bid": 10000, "current_bid": 2500, "auction": auctions["Leilão de Arte Clássica"], "owner": None},
            {"name": "Escultura de Bronze", "description": "Escultura em bronze, altura 45cm.", "starting_bid": 1800, "max_bid": 5000, "current_bid": 1800, "auction": auctions["Leilão de Arte Clássica"], "owner": users["bob"]},

            # Veículos - Leilão 3
            {"name": "Volkswagen Fusca 1975", "description": "Fusca restaurado, cor azul.", "starting_bid": 25000, "max_bid": 50000, "current_bid": 25000, "auction": auctions["Leilão de Carros Antigos"], "owner": None},
            {"name": "Chevrolet Opala 1980", "description": "Opala 1980, motor V8.", "starting_bid": 20000, "max_bid": 45000, "current_bid": 20000, "auction": auctions["Leilão de Carros Antigos"], "owner": users["carol"]},

            # Móveis - Leilão 4
            {"name": "Cadeira Luís XV", "description": "Cadeira estilo Luís XV, madeira maciça.", "starting_bid": 1500, "max_bid": 5000, "current_bid": 1500, "auction": auctions["Leilão de Móveis Raros"], "owner": None},
            {"name": "Mesa de Jantar Antiga", "description": "Mesa de jantar com 8 cadeiras.", "starting_bid": 3000, "max_bid": 10000, "current_bid": 3000, "auction": auctions["Leilão de Móveis Raros"], "owner": users["dave"]},

            # Livros - Leilão 5
            {"name": "Coleção Machado de Assis", "description": "Livros antigos de Machado de Assis.", "starting_bid": 1200, "max_bid": 4000, "current_bid": 1200, "auction": auctions["Leilão de Livros Históricos"], "owner": None},

            # Geral - Leilão 6
            {"name": "iPad Pro 2024", "description": "iPad Pro com 12.9 polegadas.", "starting_bid": 5000, "max_bid": 12000, "current_bid": 5000, "auction": auctions["Leilão Geral"], "owner": None},
            {"name": "Câmera Canon EOS R6", "description": "Câmera profissional Canon.", "starting_bid": 6000, "max_bid": 14000, "current_bid": 6000, "auction": auctions["Leilão Geral"], "owner": users["eve"]},
        ]

        items = {}
        for idata in items_data:
            item, created = Item.objects.get_or_create(
                name=idata["name"],
                auction=idata["auction"],
                defaults={
                    "description": idata["description"],
                    "starting_bid": idata["starting_bid"],
                    "max_bid": idata["max_bid"],
                    "current_bid": idata["current_bid"],
                    "owner": idata["owner"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Item '{item.name}' criado no leilão '{item.auction.name}'."))
            else:
                self.stdout.write(self.style.WARNING(f"Item '{item.name}' já existe."))
            items[item.name] = item

        # Lances (bids) - criando competição e variação
        bids_data = [
            # iPhone 15 Pro Max (owned by Alice) - bids from Bob and Carol
            {"user": users["bob"], "item": items["iPhone 15 Pro Max"], "amount": 4600},
            {"user": users["carol"], "item": items["iPhone 15 Pro Max"], "amount": 4800},

            # MacBook Pro M3 (no owner) - bids from Alice and Dave
            {"user": users["alice"], "item": items["MacBook Pro M3"], "amount": 9000},
            {"user": users["dave"], "item": items["MacBook Pro M3"], "amount": 11000},

            # Samsung QLED TV 65" (no owner) - bids from Eve
            {"user": users["eve"], "item": items["Samsung QLED TV 65\""], "amount": 4000},

            # Escultura de Bronze (owned by Bob) - bids from Alice
            {"user": users["alice"], "item": items["Escultura de Bronze"], "amount": 2000},

            # Volkswagen Fusca 1975 (no owner) - bids from Eve and Carol
            {"user": users["eve"], "item": items["Volkswagen Fusca 1975"], "amount": 27000},
            {"user": users["carol"], "item": items["Volkswagen Fusca 1975"], "amount": 30000},

            # Mesa de Jantar Antiga (owned by Dave) - bids from Bob and Eve
            {"user": users["bob"], "item": items["Mesa de Jantar Antiga"], "amount": 3500},
            {"user": users["eve"], "item": items["Mesa de Jantar Antiga"], "amount": 3700},

            # iPad Pro 2024 (no owner) - bid from Alice
            {"user": users["alice"], "item": items["iPad Pro 2024"], "amount": 5500},

            # Câmera Canon EOS R6 (owned by Eve) - bid from Dave
            {"user": users["dave"], "item": items["Câmera Canon EOS R6"], "amount": 6200},
        ]

        for bdata in bids_data:
            bid, created = Bid.objects.get_or_create(
                user=bdata["user"],
                item=bdata["item"],
                defaults={"amount": bdata["amount"]},
            )
            if created:
                # Atualiza o current_bid do item se o lance for maior
                item = bdata["item"]
                if item.current_bid is None or bdata["amount"] > item.current_bid:
                    item.current_bid = bdata["amount"]
                    item.save()
                self.stdout.write(self.style.SUCCESS(f"Lance criado: {bdata['user'].username} -> ${bdata['amount']} em '{item.name}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Lance já existe: {bdata['user'].username} em '{bdata['item'].name}'"))

        self.stdout.write(self.style.SUCCESS("Banco populado com sucesso!"))
