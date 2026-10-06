import contextlib
import io
import os
import tempfile
import unittest
import wave

import morse


class MorseTests(unittest.TestCase):
    def test_text_to_morse(self):
        self.assertEqual(morse.text2morse("sos"), "... --- ...")

    def test_words_separated_by_two_spaces(self):
        self.assertEqual(
            morse.text2morse("hello world"),
            ".... . .-.. .-.. ---  .-- --- .-. .-.. -..")

    def test_morse_to_text(self):
        self.assertEqual(
            morse.morse2text(".... . .-.. .-.. ---  .-- --- .-. .-.. -.."),
            "hello world")

    def test_round_trip_every_character(self):
        chars = "".join(c for c in morse.alphabet if c != " ")
        self.assertEqual(morse.morse2text(morse.text2morse(chars)), chars)

    def test_case_insensitive(self):
        self.assertEqual(morse.text2morse("SOS"), morse.text2morse("sos"))

    def test_unknown_characters(self):
        self.assertEqual(morse.text2morse("a~b"), ".- * -...")
        self.assertEqual(morse.morse2text(".- ....... -..."), "a*b")

    def test_empty(self):
        self.assertEqual(morse.text2morse(""), "")
        self.assertEqual(morse.morse2text(""), " ")

class SoundTests(unittest.TestCase):
    def duration_in_units(self, code, wpm=20):
        buffer = io.BytesIO()
        morse.morse2wav(code, buffer, wpm=wpm)
        buffer.seek(0)
        with wave.open(buffer) as wav:
            self.assertEqual(wav.getframerate(), morse.SAMPLE_RATE)
            self.assertEqual(wav.getnchannels(), 1)
            unit = int(morse.SAMPLE_RATE * 1.2 / wpm)
            return wav.getnframes() / unit

    def test_dot_and_dash(self):
        self.assertEqual(self.duration_in_units(".-"), 1 + 1 + 3)

    def test_letter_and_word_gaps(self):
        self.assertEqual(self.duration_in_units(". ."), 1 + 3 + 1)
        self.assertEqual(self.duration_in_units(".  ."), 1 + 7 + 1)

    def test_trailing_spaces_ignored(self):
        self.assertEqual(self.duration_in_units(" . "), 1)

    def test_empty(self):
        self.assertEqual(self.duration_in_units(""), 0)

    def test_tone_is_not_silent(self):
        buffer = io.BytesIO()
        morse.morse2wav("-", buffer)
        buffer.seek(0)
        with wave.open(buffer) as wav:
            self.assertTrue(any(wav.readframes(wav.getnframes())))

    def test_invalid_speed(self):
        with self.assertRaises(ValueError):
            morse.morse2wav(".", io.BytesIO(), wpm=0)

    def test_cli_writes_wav(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "sos.wav")
            with contextlib.redirect_stdout(io.StringIO()):
                morse.main(["-t", "sos", "--wav", path])
            with wave.open(path) as wav:
                self.assertGreater(wav.getnframes(), 0)


if __name__ == "__main__":
    unittest.main()
