from django.conf import settings
import re

def get_site_url():  # regex sso url
    regex = r"^(.+)\/s.+"
    matches = re.finditer(regex, settings.ESI_SSO_CALLBACK_URL, re.MULTILINE)
    url = "http://"

    for m in matches:
        url = m.groups()[0] # first match

    return url

PAYMENT_CORP = getattr(settings, "PAYMENT_CORP", 1639878825)

# Name of this app as shown in the Auth sidebar, page titles
INVOICES_APP_NAME = getattr(settings, "INVOICES_APP_NAME", "Alliance Contributions")


def discord_bot_active():
    return 'aadiscordbot' in settings.INSTALLED_APPS
