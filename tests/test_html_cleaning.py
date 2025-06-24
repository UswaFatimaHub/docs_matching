# tests/test_html_cleaning.py
from matcher.management.commands.runapscheduler import clean_html

def test_clean_html():
    html = "<p>Hello <b>world</b></p>"
    assert clean_html(html) == "Hello world"

def test_clean_empty():
    assert clean_html("") == ""
    assert clean_html(None) == ""

