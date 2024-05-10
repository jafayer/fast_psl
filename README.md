⚠️ Under active development ⚠️
------

# Fast PSL

A fast, efficient, minimal Public Suffix List package.

This package takes inspiration from several other public suffix list
packages that came before it.

It uses the excellent [marisa-trie](https://pypi.org/project/marisa-trie/) package as an underlying data structure for fast, efficient lookups. It builds on the prior ecosystem of PSL packages to provide a feature-rich package.

## Acknowledgements

[publicsuffix2](https://pypi.org/project/publicsuffix2/) gave general
inspiration for using a trie structure as the lookup data structure.

[psl](https://pypi.org/project/psl/) gave inspiration for its icann_only functionality, and 