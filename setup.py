from setuptools import setup, find_packages


setup(
    name="jtv2xmltv",
    version="0.2.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jtv2xmltv = jtv2xmltv.main:main',
        ]
    },
    author="Andrey Tataranovich",
    author_email="tataranovich@gmail.com",
    description="JTV to XMLTV converter",
    long_description="JTV to XMLTV converter",
    license="MIT",
    keywords="epg xmltv jtv",
    url="https://github.com/tataranovich/jtv2xmltv/",
)
