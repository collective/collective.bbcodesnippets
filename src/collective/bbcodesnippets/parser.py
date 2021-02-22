from .interfaces import IFormatterFactory
from zope.component import getUtilitiesFor

import bbcode


def _null_linker(url):
    return url


def create_parser():
    parser = bbcode.Parser(
        install_defaults=False,
        escape_html=False,
        replace_cosmetic=False,
        linker=_null_linker,
    )
    for name, factory in getUtilitiesFor(IFormatterFactory):
        __traceback_info__ = name
        formatter, options = factory()   
        parser.add_formatter(name, formatter, **options)
    return parser
