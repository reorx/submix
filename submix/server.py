"""
Start a django server from command line,
this module is not intended to use for production deployment.
"""

from .views import cli_state
from .parser import NodeList


def run(sub_source: str, sub_content: bytes, nodes: NodeList):
    # set views state
    cli_state.sub_source = sub_source
    cli_state.sub_content = sub_content
    cli_state.nodes = nodes

    argv = ['manage.py', 'runserver']
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(argv)
