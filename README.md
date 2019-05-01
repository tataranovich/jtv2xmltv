# jtv2xmltv

JTV to XMLTV converter.

Currently supports only reading JTV file in ZIP format.

# Install

```
git clone https://github.com/tataranovich/jtv2xmltv.git
cd jtv2xmltv
python setup.py install
```

# Usage

Convert EPG in JTV format to XMLTV:

```
jtv2xmltv [-t timezone] <-i input> [-o output]
```

## Examples

Convert file examples/TelecomTVepg.zip and save to /tmp/tvguide.xml.

```
jtv2xmltv -t +0300 -i examples/TelecomTVepg.zip -o /tmp/tvguide.xml
```

Convert file examples/TelecomTVepg.zip and print to stdout.

```
jtv2xmltv -i examples/TelecomTVepg.zip -o -
```

or

```
jtv2xmltv -i examples/TelecomTVepg.zip
```

# Validate

To validate XML output use following command

```
jtv2xmltv -i examples/TelecomTVepg.zip -o output.xml
wget https://raw.githubusercontent.com/XMLTV/xmltv/master/xmltv.dtd
xmllint --noout --dtdvalid xmltv.dtd output.xml

```
