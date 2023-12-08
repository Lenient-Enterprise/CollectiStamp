#!/usr/bin/.env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def set_mode_settings():
    """Set Django settings module based on the --mode argument."""
    if "--mode" in sys.argv:
        try:
            mode_index = sys.argv.index("--mode")
            mode_value = sys.argv[mode_index + 1]
            sys.argv.pop(mode_index)  # Remove "--mode"
            sys.argv.pop(mode_index)  # Remove the mode value

            if mode_value == "production" or mode_value == "development" or mode_value == "deployment":
                os.environ['MODE'] = mode_value
            else:
                raise ValueError("Invalid value for --mode.")

        except IndexError:
            print("Error: Specify a value for --mode.")
            sys.exit(1)
    else:
        # Añade al entorno el modo
        os.environ['MODE'] = "development"

def main():
    """Run administrative tasks."""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'collecti_stamp.settings'
    set_mode_settings()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

