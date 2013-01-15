from django.conf import settings

try:
    from south.management.commands.test import Command as TestCommand
except ImportError:
    from django.core.management.commands.test import Command as TestCommand

class Command(TestCommand):
    def handle(self, *test_labels, **options):
        try:
            if not test_labels and hasattr(settings, 'MY_APPS'):
                test_labels += settings.MY_APPS
                print '!! only testing %s !!' % (' '.join(test_labels),)
        except: pass

        super(Command, self).handle(*test_labels, **options)
