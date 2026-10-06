__version__ = "1.2.0"

import argparse
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import wave

SAMPLE_RATE = 44100

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


def _timing(morse):
    # (is_tone, units) pairs. Dot = 1 unit, dash = 3, gap inside a letter = 1,
    # between letters = 3, between words = 7.
    timing = []
    previous = ""

    for symbol in str(morse).strip():
        if symbol == ".":
            timing += [(True, 1), (False, 1)]
        elif symbol == "-":
            timing += [(True, 3), (False, 1)]
        elif symbol == " ":
            timing.append((False, 4 if previous == " " else 2))
        previous = symbol

    if timing and not timing[-1][0]:
        timing.pop()

    return timing


def morse2wav(morse, file, wpm=20, frequency=600, volume=0.5):
    """Write Morse code as a tone to a WAV file (path or binary file object)."""

    if wpm <= 0 or frequency <= 0:
        raise ValueError("wpm and frequency must be positive")

    unit = int(SAMPLE_RATE * 1.2 / wpm)
    ramp = min(int(SAMPLE_RATE * 0.005), unit // 2)
    amplitude = int(32767 * max(0.0, min(volume, 1.0)))
    step = 2 * math.pi * frequency / SAMPLE_RATE

    tones = {}
    frames = bytearray()

    for is_tone, units in _timing(morse):
        length = unit * units
        if not is_tone:
            frames += bytes(2 * length)
            continue
        if length not in tones:
            samples = []
            for i in range(length):
                envelope = min(1.0, i / ramp, (length - 1 - i) / ramp) if ramp else 1.0
                samples.append(int(amplitude * envelope * math.sin(step * i)))
            tones[length] = struct.pack(f"<{length}h", *samples)
        frames += tones[length]

    with wave.open(file, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(bytes(frames))


def play(morse, wpm=20, frequency=600, volume=0.5):
    """Play Morse code through the speakers."""

    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)

    try:
        morse2wav(morse, path, wpm, frequency, volume)

        if sys.platform == "win32":
            import winsound
            winsound.PlaySound(path, winsound.SND_FILENAME)
            return

        players = [["afplay"]] if sys.platform == "darwin" else [
            ["paplay"], ["aplay", "-q"], ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]]
        for player in players:
            if shutil.which(player[0]):
                subprocess.run(player + [path], check=True)
                return

        raise RuntimeError("no audio player found; use --wav to save to a file instead")
    finally:
        os.remove(path)


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
    parser.add_argument("-p", "--play", action="store_true",
                        help="play the Morse code as sound")
    parser.add_argument("-w", "--wav", metavar="FILE",
                        help="save the Morse code as a WAV file")
    parser.add_argument("--wpm", type=float, default=20,
                        help="speed in words per minute (default: 20)")
    parser.add_argument("--freq", type=float, default=600,
                        help="tone frequency in Hz (default: 600)")
    parser.add_argument("-V", "--version", action="version",
                        version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    if (args.play or args.wav) and args.text is None and args.morse is None:
        parser.error("--play and --wav need -t or -m")
    if args.wpm <= 0 or args.freq <= 0:
        parser.error("--wpm and --freq must be positive")

    if args.text is not None:
        code = text2morse(args.text)
        print(code)
    elif args.morse is not None:
        code = args.morse
        print(morse2text(code))
    else:
        interactive()
        return

    if args.wav:
        morse2wav(code, args.wav, args.wpm, args.freq)
    if args.play:
        try:
            play(code, args.wpm, args.freq)
        except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
            sys.exit(f"morse: cannot play sound: {error}")


if __name__ == "__main__":
    main()
