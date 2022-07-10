import json
import sys
import unicodedata
from pathlib import Path

CATEGORIES = {
    "Lu": "Uppercase Letter",
    "Ll": "Lowercase Letter",
    "Lt": "Titlecase Letter",
    "Lm": "Modifier Letter",
    "Lo": "Other Letter",
    "Mn": "Non-spacing Mark",
    "Mc": "Spacing Mark",
    "Me": "Enclosing Mark",
    "Nd": "Decimal Number",
    "Nl": "Letter Number",
    "No": "Other Number",
    "Pc": "Connector Punctuation",
    "Pd": "Dash Punctuation",
    "Ps": "Opening Punctuation",
    "Pe": "Closing Punctuation",
    "Pi": "Initial Quotation Mark",
    "Pf": "Final Quotation Mark",
    "Po": "Other Punctuation",
    "Sm": "Mathematical Symbol",
    "Sc": "Currency Sign",
    "Sk": "Non-letter Modifier Symbol",
    "So": "Other Symbol",
    "Zs": "Space Separator",
    "Zl": "Line Separator",
    "Zp": "Paragraph Separator",
    "Cc": "Control Character",
    "Cf": "Format Control Character",
    "Cs": "Surrogate Code Point",
    "Co": "Private-use Character",
    "Cn": "Reserved Unassigned Code Point",
}

WANTED_BLOCK_TEXT = """
Basic Latin
Latin-1 Supplement
Latin Extended-A
Latin Extended-B
IPA Extensions
Spacing Modifier Letters
Combining Diacritical Marks
Greek and Coptic
Cyrillic
Hebrew
Latin Extended Additional
Greek Extended
General Punctuation
Superscripts and Subscripts
Currency Symbols
Combining Diacritical Marks for Symbols
Letterlike Symbols
Number Forms
Arrows
Mathematical Operators
Miscellaneous Technical
Control Pictures
Enclosed Alphanumerics
Miscellaneous Symbols
Dingbats
Miscellaneous Mathematical Symbols-A
Supplemental Arrows-A
Supplemental Arrows-B
Miscellaneous Mathematical Symbols-B
Supplemental Mathematical Operators
Miscellaneous Symbols and Arrows
Latin Extended-C
Supplemental Punctuation
Latin Extended-D
Latin Extended-E
Ancient Symbols
Latin Extended-F
Mathematical Alphanumeric Symbols
Playing Cards
Enclosed Alphanumeric Supplement
Enclosed Ideographic Supplement
Miscellaneous Symbols and Pictographs
Emoticons
Ornamental Dingbats
Geometric Shapes Extended
Supplemental Arrows-C
Supplemental Symbols and Pictographs
Chess Symbols
Symbols and Pictographs Extended-A
"""
WANTED_BLOCKS = WANTED_BLOCK_TEXT.strip().splitlines()

DATA_DIR = Path(__file__).parent / "data"


def get_blocks():
    blocks = {}
    with (DATA_DIR / "Blocks.txt").open("r") as fp:
        for line in fp:
            line = line.strip()
            if line and line[0] in "0123456789ABCDEF":
                # 1FA00..1FA6F; Chess Symbols
                points, name = line.split("; ")
                start, end = points.split("..")
                start, end = int(start, 16), int(end, 16)
                for i in range(start, end + 1):
                    blocks[i] = name
    return blocks


def get_latex():
    with (DATA_DIR / "unicode-latex.json").open("r") as fp:
        return json.load(fp)


def main():
    blocks = get_blocks()
    latex = get_latex()
    data_txt = Path(__file__).parent / "data/UnicodeData.txt"
    for line in data_txt.read_text().splitlines():
        fields = line.strip().split(";")
        cp, name, cat = fields[:3]
        i = int(cp, 16)
        try:
            c = chr(i)
            if "\t" in c:
                continue
            name = unicodedata.name(c)
            cat = unicodedata.category(c)
            category_name = CATEGORIES[cat]
            block = blocks[i]
            aliases = [name.lower(), hex(i)]
            if c in latex:
                aliases.append(latex[c])
            alias_str = " | ".join(aliases)
            if block in WANTED_BLOCKS:
                print(f"{c}\tUnicode {category_name}\t{block}\t{name}\t{alias_str}")
        except ValueError:
            continue


if __name__ == "__main__":
    main()
