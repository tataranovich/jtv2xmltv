# jtv2xmltv

JTV to XMLTV converter.

Currently supports only reading JTV file in ZIP format.

# Usage

Convert EPG in JTV format to XMLTV:

```
python src/jtv2xmltv.py <input> [output]
```

## Examples

Convert file examples/TelecomTVepg.zip and save to /tmp/tvguide.xml.

```
python src/jtv2xmltv.py examples/TelecomTVepg.zip /tmp/tvguide.xml
```

Convert file examples/TelecomTVepg.zip and print to stdout.

```
python src/jtv2xmltv.py examples/TelecomTVepg.zip -
```

or

```
python src/jtv2xmltv.py examples/TelecomTVepg.zip
```
