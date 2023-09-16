from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from django.contrib.sessions.models import Session
from django.contrib.gis.geoip2 import GeoIP2

from user_agents import parse
from .models import Login_Logs, User


@receiver(user_logged_in)
def log_user_login(sender, user, request, **kwargs):
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    user_agent_parsed = parse(user_agent)
    browser = user_agent_parsed.browser.family

    # Use GeoIP2 to get location information based on IP address
    g = GeoIP2()
    try:
        location = g.city(ip_address)
        # Extract city, country, etc. from the location object if needed
    except Exception as e:
        location = None

    # Create a Login_Logs instance to log the login details
    login_log = Login_Logs.objects.create(
        ip       = ip_address,
        browser  = browser,
        user     = user,
        location = location
    )