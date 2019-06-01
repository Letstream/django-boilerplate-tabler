from django.core.management.base import BaseCommand, CommandError
from apps.core.models import Options
from apps.core.utils import addOption, getOption, options

class Command(BaseCommand):

    help = "Initializes Database Tables with initial values"

    def handle(self, *args, **kwargs):

        for option in options:
            if getOption(option[0]) == None:
                print(" -- Added Option %s - %s - %s" % (option[0], option[1], option[2]))
                addOption(option[0], option[1], option[2])
            else:
                print(" -- Existing Option %s - %s - %s" % (option[0], option[1], option[2]))

        print("Added Initial Entries!")