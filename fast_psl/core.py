from dataclasses import dataclass
from marisa_trie import Trie, LARGE_CACHE
from functools import reduce

from .helpers import get_local_public_suffix_list, fetch_remote_public_suffix_list, filter_public_or_private_block, to_punycode, should_store_punycode, reverse, sanitize_domain

@dataclass
class etld_parts:
    """
    A class to represent the parts of a public suffix.
    """
    domain: str # the full domain
    etld: str # the effective top-level domain
    etld_plus_one: str # the effective topmost registrable domain
    subdomain: str # the subdomain

class PublicSuffixList:
    def __init__(self, strict=False, trie_path=None, file_path=None, psl_text=None, remote_url=None):
        """
        Initialize the PublicSuffixList object.
        """
        self.strict = strict

        if trie_path is not None:
            self.public_suffixes = Trie().load(trie_path)
        elif psl_text is not None:
            domains = self._process_psl_text(psl_text)
            self.public_suffixes = Trie(domains, cache_size=LARGE_CACHE)
        elif file_path is not None:
            psl_text = get_local_public_suffix_list(file_path)
            domains = self._process_psl_text(psl_text)
            self.public_suffixes = Trie(domains, cache_size=LARGE_CACHE)
        elif remote_url is not None:
            psl_text = fetch_remote_public_suffix_list(remote_url)
            domains = self._process_psl_text(psl_text)
            self.public_suffixes = Trie(domains, cache_size=LARGE_CACHE)
        else:
            try:
                psl_text = get_local_public_suffix_list()
                domains = self._process_psl_text(psl_text)
                self.public_suffixes = Trie(domains, cache_size=LARGE_CACHE)
            except FileNotFoundError:
                psl_text = fetch_remote_public_suffix_list()
                domains = self._process_psl_text(psl_text)
                self.public_suffixes = Trie(domains, cache_size=LARGE_CACHE)
        try:
            if file_path:
                psl_text = get_local_public_suffix_list(file_path)
            else:
                psl_text = get_local_public_suffix_list()
        except FileNotFoundError:
            psl_text = fetch_remote_public_suffix_list()

    @staticmethod
    def from_marisa(trie_path: str):
        """
        Initialize a PublicSuffixList object from a marisa trie.
        """
        return PublicSuffixList(trie_path=trie_path)
    
    @staticmethod
    def from_text_file(file_path: str):
        """
        Initialize a PublicSuffixList object from a text file.
        """
        return PublicSuffixList(file_path=file_path)
    
    @staticmethod
    def from_remote_url(remote_url: str):
        """
        Initialize a PublicSuffixList object from a remote URL.
        """
        return PublicSuffixList(remote_url=remote_url)
    
    @staticmethod
    def from_text(psl_text: str):
        """
        Initialize a PublicSuffixList object from a text string.
        """
        return PublicSuffixList(psl_text=psl_text)

    def _process_psl_text(self, psl_text):
        if self.strict:
            psl_text = filter_public_or_private_block(psl_text, public=True)

        domains = [x for x in psl_text.split("\n") if x != "" and not x.startswith("//")]
        # loop through domains and determine if we should add punycode representation
        domains += [to_punycode(domain) for domain in domains if should_store_punycode(domain)]

        # reverse the domains for the trie
        domains = [reverse(x) for x in domains]

        return domains

    def get_public_suffix(self, domain: str, convert_to_punycode=False):
        """
        Get the public suffix of a domain.
        """
        pipeline = [ sanitize_domain, reverse ]
        if convert_to_punycode:
            pipeline.insert(0, to_punycode)
        domain = reduce(lambda x, f: f(x), pipeline, domain)
        search = self.public_suffixes.prefixes(domain)
        if len(search) == 0:
            raise ValueError("Domain not found in public suffix list.")
        
        longest_suffix = reverse(search[-1])
        return longest_suffix

    def get_public_suffix_parts(self, domain, convert_to_punycode=False):
        """
        Get the parts of a domain.
        """
        domain = domain.lower()
        if convert_to_punycode:
            domain = to_punycode(domain)
            
        public_suffix = self.get_public_suffix(domain, convert_to_punycode)
        parts = domain.replace(public_suffix, "").strip(".").split(".")
        etld_plus_one = ".".join([parts[-1], public_suffix])
        subdomain = ".".join(parts[:-1])

        return etld_parts(
            domain=domain,
            etld=public_suffix,
            etld_plus_one = etld_plus_one,
            subdomain=subdomain,
        )