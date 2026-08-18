alphabet = {
    "a": ".- ",   "b": "-... ", "c": "-.-. ", "d": "-.. ",
    "e": ". ",    "f": "..-. ", "g": "--. ",  "h": ".... ",
    "i": ".. ",   "j": ".--- ", "k": "-.- ",  "l": ".-.. ",
    "m": "-- ",   "n": "-. ",   "o": "--- ",  "p": ".--. ",
    "q": "--.- ", "r": ".-. ",  "s": "... ",  "t": "- ",
    "u": "..- ",  "v": "...- ", "w": ".-- ",  "x": "-..- ",
    "y": "-.-- ", "z": "--.. ", " ": " ",
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


def main():

    choice = input("Text2morse or morse2text (t/m)? ").lower().strip()

    if choice == "t":
        print(text2morse(input("text: ")))
    elif choice == "m":
        print(morse2text(input("morse: ")))
    else:
        print("Unexpected input; please input t for text to morse, m for morse to text.")


if __name__ == "__main__":
    main()