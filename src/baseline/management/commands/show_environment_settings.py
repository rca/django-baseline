from django.core.management.base import BaseCommand, CommandError

from baseline.environment import get_catalog


class Command(BaseCommand):
    help = "Lists all the settings that come from the environment"

    def add_arguments(self, parser):
        """
        Adds an argument to the parser
        """
        parser.add_argument(
            "--attributes",
            dest="attributes",
            action="store_true",
            default=False,
            help="include additional attributes for each setting as a comment",
        )

    def handle(self, *args, **options):
        catalog = get_catalog()
        for k in sorted(catalog):
            item = catalog[k]

            attributes_s = ""
            if options["attributes"]:
                attributes = item.setting.attributes
                attributes_s = "  # " + ", ".join(
                    [
                        f"{attrs_k}={attributes[attrs_k]!r}"
                        for attrs_k in sorted(attributes)
                    ]
                )

            print(f"{k}={item}{attributes_s}")
