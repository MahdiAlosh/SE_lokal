# testsuite.py

import pytest

# Importiere die Testfälle aus den Testdateien
from tests.test_auth import *
from tests.test_search import *

if __name__ == "__main__":
    # Führe die Tests aus
    pytest.main()
