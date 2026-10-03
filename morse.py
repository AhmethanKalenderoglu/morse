__version__ = "1.1.0"

import argparse

alphabet = {
    "a": ".- ",   "b": "-... ", "c": "-.-. ", "d": "-.. ",
    "e": ". ",    "f": "..-. ", "g": "--. ",  "h": ".... ",
    "i": ".. ",   "j": ".--- ", "k": "-.- ",  "l": ".-.. ",
    "m": "-- ",   "n": "-. ",   "o": "--- ",  "p": ".--. ",
    "q": "--.- ", "r": ".-. ",  "s": "... ",  "t": "- ",
    "u": "..- ",  "v": "...- ", "w": ".-- ",  "x": "-..- ",
    "y": "-.-- ", "z": "--.. ",
    "0": "----- ", "1": ".---- ", "2": "..--- ", "3": "...-- ",
    "4": "....- ", "5": "..... ", "6": "-.... ", "7": "--... ",
    "8": "---.. ", "9": "----. ",
    ".": ".-.-.- ", ",": "--..-- ", "?": "..--.. ", "'": ".----. ",
    "!": "-.-.-- ", "/": "-..-. ",  "(": "-.--. ",  ")": "-.--.- ",
    "&": ".-... ",  ":": "---... ", ";": "-.-.-. ", "=": "-...- ",
    "+": ".-.-. ",  "-": "-....- ", "_": "..--.- ", '"': ".-..-. ",
    "$": "...-..- ", "@": ".--.-. ", " ": " ",
}

reverse_alphabet = {"": " "}
for letter, code in alphabet.items():
    reverse_alphabet[code.strip()] = letter


def text2morse(text):
    text = str(text).lower()
    morse = ""

    for character in text:
        morse += alphabet.get(character, "* ")

    return morse.removesuffix(" ")


def morse2text(morse):

    morse = str(morse).split(" ")
    text = ""

    for codes in morse:
        text += reverse_alphabet.get(codes, "*")

    return text


def interactive():

    choice = input("Text2morse or morse2text (t/m)? ").lower().strip()

    if choice == "t":
        print(text2morse(input("text: ")))
    elif choice == "m":
        print(morse2text(input("morse: ")))
    else:
        print("Unexpected input; please input t for text to morse, m for morse to text.")


def main(argv=None):

    parser = argparse.ArgumentParser(
        prog="morse", description="Two-way Morse code translator.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--text", metavar="TEXT",
                       help="translate text to Morse")
    group.add_argument("-m", "--morse", metavar="MORSE",
                       help="translate Morse to text (letters separated by a space, words by two)")
    parser.add_argument("-V", "--version", action="version",
                        version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    if args.text is not None:
        print(text2morse(args.text))
    elif args.morse is not None:
        print(morse2text(args.morse))
    else:
        interactive()


if __name__ == "__main__":
    main()
