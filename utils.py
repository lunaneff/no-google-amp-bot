from urllib.parse import urlparse
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

    if get_tld(parsed.hostname, as_object=True, fix_protocol=True, fail_silently=True).domain == 'google' \
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
