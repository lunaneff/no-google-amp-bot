from urllib.parse import urlparse, parse_qs
import requests
from tld import get_tld


def is_amp(url):
    """
    Check if the given URL is an AMP URL
    :param url: The URL to check
    :type url: string
    :return: Returns a boolean if it's an AMP URL
    :returns: bool
    """
    parsed = urlparse(url)
    tld = get_tld(parsed.hostname, as_object=True, fix_protocol=True, fail_silently=True)

    if tld and tld.domain == 'google' \
            and parsed.path.startswith('/amp/'):
        return True
    return False


def amp_to_normal(url):
    """
    Check if the given URL is an AMP url. If it is, send a request to find the normal URL

    :param url: The URL to check
    :type url: string
    :return: Returns the non-AMP version of the given URL if it's an AMP URL. Otherwise, it returns None
    :returns: string?
    """
    if is_amp(url):
        r = requests.get(url)
        return r.url
    else:
        return None


def is_google_redirect(url):
    """
    Check if the given URL is a Google redirect (https://www.google.com/url?q=...)
    :param url: The URL to check
    :type url: string
    :return: Returns a boolean if it's a redirect
    :returns: bool
    """
    parsed = urlparse(url)
    tld = get_tld(parsed.hostname, as_object=True, fix_protocol=True, fail_silently=True)

    if tld and tld.domain == 'google' \
            and parsed.path.startswith('/url'):
        return True
    return False


def follow_google_redirect(url):
    """
    Check if the given URL is a Google redirect (https://www.google.com/url?q=...). If it is, extract the q query
    parameter to find the real link
    :param url: The URL to check
    :type url: string
    :return: Returns the real link if it's a redirect. Otherwise, it returns None
    :returns: string
    """
    if is_google_redirect(url):
        parsed = parse_qs(urlparse(url).query)
        q = parsed.get('q')
        if isinstance(q, list):
            return q[0]
        return q
    return None
