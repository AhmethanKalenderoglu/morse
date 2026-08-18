# morse

Two-way morse code translator in python.

## Run interactively

```
python morse.py
```

Choose `t` for text → Morse, or `m` for Morse → text.

## Use as a module

import morse

morse.text2morse("hello world")   # '.... . .-.. .-.. ---  .-- --- .-. .-.. -..'

morse.morse2text(".... . .-.. .-.. ---  .-- --- .-. .-.. -..")       # 'hello world'


## Notes

- Supports the letters a–z and spaces. Unrecognized characters are replaced with `*`. 
The characters you add to the alphabet will also work; just don't forget to add a space at the end of the response for the ones you've added

