from django.core.management.base import BaseCommand
from newsletters.models import Newsletter
from newsletters.tasks import send_newsletter


class Command(BaseCommand):
    help = 'Manually send a newsletter by ID'

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID of the newsletter to send')

    def handle(self, *args, **options):
        newsletter_id = options['newsletter_id']
        try:
            newsletter = Newsletter.objects.get(id=newsletter_id)
            send_newsletter.delay(newsletter_id)
            self.stdout.write(self.style.SUCCESS(f'Successfully started sending newsletter {newsletter_id}'))
        except Newsletter.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Newsletter with ID {newsletter_id} does not exist'))
