from django.core.management.base import BaseCommand
from ...models import Category, Post


class Command(BaseCommand):
    help = 'Delete all posts from category'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(
            f'Do you really want to delete all posts from category {options["category"]}? yes/no: '
        )
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Canceled'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(categories=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all {category.name} posts!'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {options['category']}'))
