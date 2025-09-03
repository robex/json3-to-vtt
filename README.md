# Convert YouTube's json3 subtitle format to VTT

### Usage

```
usage: json3_to_vtt.py [-h] [-l LANG_CODE] file

YouTube json3 to VTT subtitle converter

positional arguments:
  file                  Input file in json3 format

options:
  -h, --help            show this help message and exit
  -l, --lang_code LANG_CODE
                        ISO language code to use, default: en
```

Example usage, this will output the file `subs.ru.vtt` in the current directory:
```
python3 json3_to_vtt.py -l ru subs.json
```

## Possible issues
### Incorrect format
Make sure the input file is in the correct format, a quick check is that it must have the following JSON key at the root level: `"wireMagic": "pb3"`
