from .helpers import fetch_remote_public_suffix_list

if __name__ == "__main__":
    print("Refreshing the public suffix list.")
    fetch_remote_public_suffix_list()