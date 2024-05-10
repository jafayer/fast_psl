install:
	pip install -r requirements.txt

refresh-psl:
	python -m fast_psl.refresh_psl

refresh-psl-curl:
	curl -o public_suffix_list.dat "https://publicsuffix.org/list/public_suffix_list.dat"
