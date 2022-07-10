import csv
import json
import re
import unicodedata
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
CATEGORIES = json.loads((DATA_DIR / "categories.json").read_text())
WANTED_BLOCKS = (DATA_DIR / "wanted-blocks.txt").read_text().strip().splitlines()
BLOCKS_PATH = DATA_DIR / "Blocks.txt"
CHARS_PATH = DATA_DIR / "UnicodeData.txt"
BLOCK_PATTERN = re.compile("^(?P<start>[0-9A-F]+)..(?P<end>[0-9A-F]+); (?P<name>.+)$", re.MULTILINE)
BLOCKS = [(int(start, 16), int(end, 16), name) for start, end, name in BLOCK_PATTERN.findall(BLOCKS_PATH.read_text())]
LATEX_LOOKUPS = json.loads((DATA_DIR / "unicode-latex.json").read_text())


def get_block(code_point: int):
    for start, end, name in BLOCKS:
        if start <= code_point <= end:
            return name
    raise ValueError(f"Block not found for codepoint: {code_point}")


def main():
    with CHARS_PATH.open("r") as fp:
        reader = csv.reader(fp, delimiter=";")
        for row in reader:
            code_point_hex, name, category_abbrev = row[:3]
            code_point_int = int(code_point_hex, 16)
            try:
                character = chr(code_point_int)
                if "\t" in character:
                    continue
                name = unicodedata.name(character)
                category_name = CATEGORIES[category_abbrev]
                block = get_block(code_point_int)
                aliases = [name.lower(), hex(code_point_int)]
                if character in LATEX_LOOKUPS:
                    aliases.append(LATEX_LOOKUPS[character])
                alias_str = " | ".join(aliases)
                if block in WANTED_BLOCKS:
                    print(f"{character}\tUnicode {category_name}\t{block}\t{name}\t{alias_str}")
            except ValueError:
                continue


if __name__ == "__main__":
    main()
