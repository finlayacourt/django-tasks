#!/usr/bin/env python

import os
import sys


def main():
    """Main function."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test.settings")

    try:
        from django.core import management
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            + "available on your PYTHONPATH environment variable? Did you "
            + "forget to activate a virtual environment?",
        ) from None

    management.execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
