.PHONY: replace

data/extra_unicode.txt: add_extra.py data/Blocks.txt data/unicode-math-symbols.csv
	python $< > $@

all_emojis.txt: data/only_emojis.txt data/extra_unicode.txt
	cat $^ > $@

/usr/local/share/rofi-emoji/all_emojis.txt: all_emojis.txt
	sudo cp $< $@

replace: /usr/local/share/rofi-emoji/all_emojis.txt