import os

from django.test import TestCase
from django.utils.importlib import import_module

from baseline.util import get_project_root


def find_test_modules(module_path):
    module_dir = os.path.realpath(os.path.dirname(module_path))
    scope = {}

    for filename in os.listdir(module_dir):
        if not (filename.startswith('test_') and filename.endswith('.py')):
            continue

        project_parent_dir = os.path.dirname(get_project_root())

        module_name = filename.replace('.py', '')
        module_path = '{0}.{1}'.format(
            module_dir.replace(project_parent_dir, ''), module_name).replace('/', '.')[1:]

        module = import_module(module_path)

        for name in dir(module):
            item = getattr(module, name)

            try:
                if issubclass(item, TestCase):
                    scope[name] = item
            except TypeError:
                pass

    return scope
