import sys
from distutils.util import strtobool

from changedetectionio.content_fetchers.exceptions import BrowserStepsStepException
import os

visualselector_xpath_selectors = 'div,span,form,table,tbody,tr,td,a,p,ul,li,h1,h2,h3,h4, header, footer, section, article, aside, details, main, nav, section, summary'

# available_fetchers() will scan this implementation looking for anything starting with html_
# this information is used in the form selections
from changedetectionio.content_fetchers.requests import fetcher as html_requests

def available_fetchers():
    # See the if statement at the bottom of this file for how we switch between playwright and webdriver
    import inspect
    p = []
    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if inspect.isclass(obj):
            # @todo html_ is maybe better as fetcher_ or something
            # In this case, make sure to edit the default one in store.py and fetch_site_status.py
            if name.startswith('html_'):
                t = tuple([name, obj.fetcher_description])
                p.append(t)

    return p


# Decide which is the 'real' HTML webdriver, this is more a system wide config
# rather than site-specific.
use_playwright_as_chrome_fetcher = os.getenv('PLAYWRIGHT_DRIVER_URL', False)
if use_playwright_as_chrome_fetcher:
    if not strtobool(os.getenv('FAST_PUPPETEER_CHROME_FETCHER', 'False')):
        from .playwright import fetcher as html_webdriver
    else:
        from .puppeteer import fetcher as html_webdriver

else:
    from .webdriver_selenium import fetcher as html_webdriver
