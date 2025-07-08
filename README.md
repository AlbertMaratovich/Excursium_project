# Excursium_project
This repository contains basic example of usage PageObject pattern with Selenium and Python.


Files

base/base.py contains parent class for POM.

pages/ contains child classes for each testing web pages.

tests/test_excursium.py contains several user-case Web UI tests for Excursium (https://excursium.com/)

tests/conftest.py contains fixture for correct start webdriver with all required options.


How To Run Tests

Install all requirements:


pip3 install -r requirements

Run tests:

python -m pytest
or use the "run" button in the IDE
