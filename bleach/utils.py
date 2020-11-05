from collections import OrderedDict
import re

import six

from bleach._vendor.django.core.validators import URLValidator


def _attr_key(attr):
    """Returns appropriate key for sorting attribute names

    Attribute names are a tuple of ``(namespace, name)`` where namespace can be
    ``None`` or a string. These can't be compared in Python 3, so we conver the
    ``None`` to an empty string.

    """
    key = (attr[0][0] or ""), attr[0][1]
    return key


def alphabetize_attributes(attrs):
    """Takes a dict of attributes (or None) and returns them alphabetized"""
    if not attrs:
        return attrs

    return OrderedDict([(k, v) for k, v in sorted(attrs.items(), key=_attr_key)])


def force_unicode(text):
    """Takes a text (Python 2: str/unicode; Python 3: unicode) and converts to unicode

    :arg str/unicode text: the text in question

    :returns: text as unicode

    :raises UnicodeDecodeError: if the text was a Python 2 str and isn't in
        utf-8

    """
    # If it's already unicode, then return it
    if isinstance(text, six.text_type):
        return text

    # If not, convert it
    return six.text_type(text, "utf-8", "strict")


netloc_port_re = re.compile(
    "^" + URLValidator.netloc_re + URLValidator.port_re + "$", re.IGNORECASE
)


# Characters valid in scheme names
scheme_chars = (
    "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "0123456789" "+-."
)


def _is_valid_netloc_and_port(netloc):
    """
    Returns the scheme for a URI or None when parsing the URI fails

    :arg str/unicode netloc:

    :returns: bool

    """
    # The maximum length of a full host name is 253 characters per RFC 1034
    # section 3.1. It's defined to be 255 bytes or less, but this includes
    # one byte for the length of the name and one byte for the trailing dot
    # that's used to indicate absolute names in DNS.
    netloc = netloc_port_re.match(netloc)
    return bool(netloc and len(netloc.group(0)) < 254)


def _parse_uri_scheme(uri):
    """
    Returns the scheme for a URI or None when parsing the URI fails

    :arg str/unicode text:

    :returns: text or None

    """
    # replicate Python 3.9 urlparse scheme parsing for older Python versions
    i = uri.find(":")
    if i > 0:
        scheme = uri[:i]
        for c in uri[:i]:
            if c not in scheme_chars:
                break
        return scheme

    return None
