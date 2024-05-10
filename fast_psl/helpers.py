import os

import idna
import requests

from .constants import ICANN_MARKERS, PRIVATE_MARKERS, PSL_FILE, PSL_URL

PSL_FILE_LOCATION = os.path.join(os.path.dirname(__file__), '../', PSL_FILE)

def get_local_public_suffix_list():
    """
    Get the local public suffix list.
    If file doesn't exist, raise an error.
    """
    if not os.path.exists(PSL_FILE_LOCATION):
        raise FileNotFoundError("The local public suffix list file does not exist.")
    with open(PSL_FILE_LOCATION, "r") as f:
        return f.read()

def fetch_remote_public_suffix_list():
    """
    Fetch the public suffix list from the remote URL.

    This should only be done at most once per day
    to respect the public suffix list rate limits.
    """
    response = requests.get(PSL_URL)
    response.raise_for_status()
    # write the response to a file
    with open(PSL_FILE_LOCATION, "w") as f:
        f.write(response.text)
    return response.text


def filter_public_or_private_block(psl_text, public=True):
    """
    Get the public domains from a PSL block.
    """
    BEGIN_MARKER, END_MARKER = ICANN_MARKERS if public else PRIVATE_MARKERS
    return psl_text.split(BEGIN_MARKER)[1].split(END_MARKER)[0].strip()

def to_punycode(domain: str) -> str:
    """
    Convert a domain to punycode.
    """
    return domain.encode("idna").decode("utf-8")

def should_store_punycode(domain):
    """
    Check if a domain should be stored in punycode.
    """
    return domain != to_punycode(domain)

def reverse(domain: str) -> str:
    """
    Reverse a domain.
    """
    return domain[::-1]

def sanitize_domain(domain: str) -> str:
    """
    Sanitize a fqdn by stripping whitespace, converting to lowercase,
    and stripping the trailing period, leaving leading periods as
    those might be significant.
    """
    return domain.strip().lower().rstrip(".")