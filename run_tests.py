import os
import sys
import django
from django.conf import settings

def main():
    # Add backend directory to sys.path
    sys.path.insert(0, os.path.abspath('backend'))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()

    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['social'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    main()
