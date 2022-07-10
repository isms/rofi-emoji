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
    "Cn": "Reserved Unassigned Code Point"
}

WANTED_BLOCK_TEXT = """
0000..007F; Basic Latin
0080..00FF; Latin-1 Supplement
0100..017F; Latin Extended-A
0180..024F; Latin Extended-B
0250..02AF; IPA Extensions
02B0..02FF; Spacing Modifier Letters
0300..036F; Combining Diacritical Marks
0370..03FF; Greek and Coptic
0400..04FF; Cyrillic
0590..05FF; Hebrew
1E00..1EFF; Latin Extended Additional
1F00..1FFF; Greek Extended
2000..206F; General Punctuation
2070..209F; Superscripts and Subscripts
20A0..20CF; Currency Symbols
20D0..20FF; Combining Diacritical Marks for Symbols
2100..214F; Letterlike Symbols
2150..218F; Number Forms
2190..21FF; Arrows
2200..22FF; Mathematical Operators
2300..23FF; Miscellaneous Technical
2400..243F; Control Pictures
2460..24FF; Enclosed Alphanumerics
2600..26FF; Miscellaneous Symbols
2700..27BF; Dingbats
27C0..27EF; Miscellaneous Mathematical Symbols-A
27F0..27FF; Supplemental Arrows-A
2900..297F; Supplemental Arrows-B
2980..29FF; Miscellaneous Mathematical Symbols-B
2A00..2AFF; Supplemental Mathematical Operators
2B00..2BFF; Miscellaneous Symbols and Arrows
2C60..2C7F; Latin Extended-C
2E00..2E7F; Supplemental Punctuation
A720..A7FF; Latin Extended-D
AB30..AB6F; Latin Extended-E
10190..101CF; Ancient Symbols
1D400..1D7FF; Mathematical Alphanumeric Symbols
1F0A0..1F0FF; Playing Cards
1F100..1F1FF; Enclosed Alphanumeric Supplement
1F200..1F2FF; Enclosed Ideographic Supplement
1F300..1F5FF; Miscellaneous Symbols and Pictographs
1F600..1F64F; Emoticons
1F650..1F67F; Ornamental Dingbats
1F780..1F7FF; Geometric Shapes Extended
1F800..1F8FF; Supplemental Arrows-C
1F900..1F9FF; Supplemental Symbols and Pictographs
1FA00..1FA6F; Chess Symbols
1FA70..1FAFF; Symbols and Pictographs Extended-A
"""
WANTED_BLOCKS = [line.split("; ")[1] for line in WANTED_BLOCK_TEXT.strip().splitlines()]


def get_blocks():
    blocks_txt = Path(__file__).parent / "data/Blocks.txt"
    blocks = {}
    with blocks_txt.open("r") as fp:
        for line in fp:
            line = line.strip()
            if line and line[0] in '0123456789ABCDEF':
                # 1FA00..1FA6F; Chess Symbols
                points, name = line.split("; ")
                start, end = points.split("..")
                start, end = int(start, 16), int(end, 16)
                for i in range(start, end + 1):
                    blocks[i] = name
    return blocks


def main():
    blocks = get_blocks()
    for i in range(32, sys.maxunicode):
        x = hex(i)
        try:
            c = chr(i)
            if c == "\t":
                continue
            name = unicodedata.name(c)
            cat = unicodedata.category(c)
            category_name = CATEGORIES[cat]
            block = blocks[i]
            aliases = [name.lower()]
            alias_str = " | ".join(aliases)
            if block in WANTED_BLOCKS:
                print(f"{c}\t{category_name}\t{block}\t{name}\t{alias_str}")
        except ValueError:
            continue


if __name__ == '__main__':
    main()
