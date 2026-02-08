from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.bank.models import BankManager


class Command(BaseCommand):
    help = 'Create a bank manager user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the manager')
        parser.add_argument('password', type=str, help='Password for the manager')
        parser.add_argument('employee_id', type=str, help='Employee ID for the manager')
        parser.add_argument('--email', type=str, help='Email for the manager', default='')
        parser.add_argument('--phone', type=str, help='Phone number for the manager', default='')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        employee_id = options['employee_id']
        email = options.get('email', '')
        phone = options.get('phone', '')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User "{username}" already exists!'))
            return

        # Check if employee_id already exists
        if BankManager.objects.filter(employee_id=employee_id).exists():
            self.stdout.write(self.style.ERROR(f'Employee ID "{employee_id}" already exists!'))
            return

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # Create manager profile
        manager = BankManager.objects.create(
            user=user,
            employee_id=employee_id,
            phone=phone
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created bank manager: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Employee ID: {employee_id}'))
        self.stdout.write(self.style.SUCCESS(f'Manager can now login at /bank/manager/login/'))
