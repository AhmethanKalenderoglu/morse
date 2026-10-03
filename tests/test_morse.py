import unittest

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


if __name__ == "__main__":
    unittest.main()
