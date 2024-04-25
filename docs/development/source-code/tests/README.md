# Test Durchführung

## Folgende Befehle müssen vor dem Testen ausgeführt werden

* cd docs/development/source-code 
* pip install pytest 
* pip install pytest-cov
* pip install pytest Flask-Testing
* pip install Flask-Login
* pip install Flask-SQLAlchemy
* pip install Flask-Login
* pip install Flask-WTF
* pip install Flask-Migrate
* pip install wikipedia-api
* pip install wikipedia


_Dateien müssen test_ oder _test im Namen haben_

### **Ausführen:** 
* pytest -s tests/test_auth.py
* pytest -s tests/test_search.py

#### oder 

* pytest -s tests/testsuite.py

## Pipeline ausführung

_Tests werden automatisch beim Pushen/Pullen ausgeführt_

## Testcoverage

_Die Coverage kann durch den folgeden Befehl überprüft werden:_
* pytest --cov=docs/development/source-code docs/development/source-code/tests