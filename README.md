# jtv2xmltv

JTV to XMLTV converter.

Currently supports only reading JTV file in ZIP format.

# Usage

Convert EPG in JTV format to XMLTV:

```
python src/jtv2xmltv.py [-t timezone] <-i input> [-o output]
```

## Examples

Convert file examples/TelecomTVepg.zip and save to /tmp/tvguide.xml.

```
python src/jtv2xmltv.py -t +0300 -i examples/TelecomTVepg.zip -o /tmp/tvguide.xml
```

Convert file examples/TelecomTVepg.zip and print to stdout.

```
python src/jtv2xmltv.py -i examples/TelecomTVepg.zip -o -
```

or

```
python src/jtv2xmltv.py -i examples/TelecomTVepg.zip
```
