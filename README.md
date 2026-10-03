# morse

[![tests](https://github.com/AhmethanKalenderoglu/morse/actions/workflows/ci.yml/badge.svg)](https://github.com/AhmethanKalenderoglu/morse/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A two-way Morse code translator in Python. One file, no dependencies, works as a command line tool and as a module.

## Install

```
pip install git+https://github.com/AhmethanKalenderoglu/morse.git
```

Or just download `morse.py`. Python 3.9+ is required.

## Command line

```
$ morse -t "hello world"
.... . .-.. .-.. ---  .-- --- .-. .-.. -..

$ morse -m ".... . .-.. .-.. ---  .-- --- .-. .-.. -.."
hello world
```

Run `morse` with no arguments for the interactive prompt (`t` = text to Morse, `m` = Morse to text). Without installing, use `python morse.py` instead of `morse`.

## As a module

```python
import morse

morse.text2morse("hello world")
# '.... . .-.. .-.. ---  .-- --- .-. .-.. -..'

morse.morse2text(".... . .-.. .-.. ---  .-- --- .-. .-.. -..")
# 'hello world'
```

## Format

- Letters are separated by one space, words by two spaces.
- Supports a-z, 0-9, common punctuation (`. , ? ' ! / ( ) & : ; = + - _ " $ @`) and spaces. Input is case-insensitive.
- Unrecognized characters become `*` in both directions.
- To add a character, add it to the `alphabet` dict in `morse.py`. Keep the trailing space in its code.

## Tests

```
python -m unittest discover -s tests -v
```

## License

MIT
