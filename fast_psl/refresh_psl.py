from .helpers import fetch_remote_public_suffix_list
from .core import PublicSuffixList
from .constants import PSL_TRIE_PICKLE_FILE

if __name__ == "__main__":
    print("Refreshing the public suffix list.")
    # fetch the remote public suffix list and cache it locally
    psl_text = fetch_remote_public_suffix_list(cache_file=True)
    psl = PublicSuffixList.from_text(psl_text)
    psl.save(file_path=PSL_TRIE_PICKLE_FILE)
    print("Public suffix list refreshed.")