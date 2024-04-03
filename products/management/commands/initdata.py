from django.core.management.base import BaseCommand, CommandError
from products.models import Status, Product, Section, NewUser, Type
import requests

class Command(BaseCommand):
    help = "First init DB"

    def handle(self, *args, **options):

        Status_CHOICES = [
            'New',
            'Actual',
            'Old',
        ]

        Type_CHOICES = [
            'Manager',
            'User',
            'Worker',
        ]

        Section_CHOICES = [
            'Sport',
            'Factory',
            'Garden',
        ]

        try:
            for status in Status_CHOICES:
                if not Status.objects.filter(name=status).exists():
                    Status.objects.create(name=status)
            for type in Type_CHOICES:
                if not Type.objects.filter(name=type).exists():
                    Type.objects.create(name=type)
            for section in Section_CHOICES:
                if not Section.objects.filter(name=section).exists():
                    Section.objects.create(name=section)
        except Exception as e:
            self.stdout.write(f"Failed fill status, type or section...\n{e}")



        self.stdout.write("Create superuser(admin@admin.io)")
        try:
            Type_user, created_type = Type.objects.get_or_create(name='Manager')
            NewUser.objects.create_user(
                email="admin@admin.io",
                username="admin",
                password="admin",
                type=Type_user,
                is_superuser=True,
                is_staff=True,
            )
        except Exception as e:
            self.stdout.write(f"Failed create SU...\n{e}")

        self.stdout.write("Create normaluser(user@mail.pl)")
        try:
            Type_user, created_type = Type.objects.get_or_create(name='User')
            NewUser.objects.create_user(
                email="user@mail.pl",
                username="user",
                password="user",
                type=Type_user,
                is_superuser=False,
                is_staff=False,
            )
        except Exception as e:
            self.stdout.write(f"Failed create normal user...\n{e}")

        self.stdout.write("Create Products")
        response = requests.get('https://fakestoreapi.com/products/')
        if response.status_code == 200:
            data = response.json()
            try:
                for product in data:
                    if not Product.objects.filter(title=product['title']).exists():
                        new_product = Product.objects.create(
                            title=product['title'],
                            price=product['price'],
                            description=product['description'],
                            category=product['category'],
                            image=product['image'],
                            status_id=1,
                            owner_id=1,
                            )
                        section1 = Section.objects.get(pk=1) 
                        new_product.sections.add(section1)
            except Exception as e:
                self.stdout.write(f"Failed save Products...\n{e}")
        else:
            self.stdout.write("Response not ok")
