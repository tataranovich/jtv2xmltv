from setuptools import setup, find_packages


setup(
    name="jtv2xmltv",
    version="0.1.0",
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'jtv2xmltv = jtv2xmltv.main:main',
        ]
    },

    install_requires=[],

    author="Andrey Tataranovich",
    author_email="tataranovich@gmail.com",
    description="JTV to XMLTV converter",
    license="GPL-3",
    keywords="epg xmltv jtv",
    url="https://github.com/tataranovich/jtv2xmltv/",

)
