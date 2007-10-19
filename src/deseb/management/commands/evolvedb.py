from django.core.management.base import AppCommand
from optparse import make_option

class Command(AppCommand):
    option_list = AppCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
    )
    help = """Prints the ALTER TABLE SQL statements for the given app name(s), in order to 
non-destructively bring them into compliance with your models.
See: http://code.google.com/p/deseb/wiki/Usage"""

    output_transaction = True

    def handle(self, *app_labels, **options):
        from django.db import connection
        from django.db.models.loading import get_apps 
        all_apps = get_apps()
        run_apps = []

        if app_labels:
            for app in all_apps:
                app_name = app.__name__.split('.')[-2]
                if app_name in app_labels:
                    run_apps.append(app)
        else:
            run_apps = all_apps
            
        cursor = connection.cursor()

        for app in run_apps:
            if app.__name__.startswith('django'): continue
            self.handle_app(app, **options)

    def handle_app(self, app, **options):
        import deseb.schema_evolution
        deseb.schema_evolution.evolvedb(app, options.get('interactive', True))