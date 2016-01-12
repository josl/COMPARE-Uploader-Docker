#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ["SITE_ENV"] == "prod":
        os.environ.setdefault(
          "DJANGO_SETTINGS_MODULE", "uploader.prod_settings"
        )
    elif os.environ["SITE_ENV"] == "dev":
        os.environ.setdefault(
          "DJANGO_SETTINGS_MODULE", "uploader.dev_settings"
        )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
