.PHONY: replace data
UNICODE_VERSION ?= 14.0.0

all_emojis.txt: data/only_emojis.txt data/extra_unicode.txt
	cat $^ > $@

/usr/local/share/rofi-emoji/all_emojis.txt: all_emojis.txt
	sudo cp $< $@

replace: /usr/local/share/rofi-emoji/all_emojis.txt

data/unicode-latex.json:
	@mkdir -p data
	curl https://raw.githubusercontent.com/ViktorQvarfordt/unicode-latex/master/unicode-latex.json > $@

data/Blocks.txt:
	@mkdir -p data
	curl http://ftp.unicode.org/Public/${UNICODE_VERSION}/ucd/Blocks.txt > $@

data/UnicodeData.txt:
	@mkdir -p data
	curl http://ftp.unicode.org/Public/${UNICODE_VERSION}/ucd/UnicodeData.txt > $@

data/extra_unicode.txt: add_extra.py data/Blocks.txt data/UnicodeData.txt data/unicode-latex.json
	python $< > $@