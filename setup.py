from setuptools import setup, find_packages

setup(
    name='fast_psl',
    version="0.1.0",
    description='A fast and efficient public suffix list implementation.',
    author="CleanDNS Inc.",
    packages=find_packages(),
    install_requires=[
        "marisa_trie==1.1.1",
        "requests==2.31.0"
    ],   
)