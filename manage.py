#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import environ

env = environ.Env()
environ.Env.read_env()


def main():
    """Run administrative tasks."""
    # If "test" command is run
    if sys.argv[1] == "test":
        # Live-server test need different settings
        if sys.argv[2] == "--live":
            sys.argv.pop(2)
            os.environ.setdefault(
                "DJANGO_SETTINGS_MODULE", "social.settings.testing_live"
            )

        # Normal tests
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social.settings.testing")

    # Other commands
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"social.settings.{env('DJANGO_ENV')}")

    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
