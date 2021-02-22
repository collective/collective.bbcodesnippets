from .controlpanel import IBBCodeSnippetsSettings
from .interfaces import IFormatterFactory
from plone import api
from zope.component import getUtilitiesFor

import bbcode


def _null_linker(url):
    return url


def create_parser():
    enabled = api.portal.get_registry_record(
        "formatters", interface=IBBCodeSnippetsSettings
    )
    parser = bbcode.Parser(
        install_defaults=False,
        escape_html=False,
        replace_cosmetic=False,
        linker=_null_linker,
    )
    for name, factory in getUtilitiesFor(IFormatterFactory):
        __traceback_info__ = name
        if factory.__doc__ or name in enabled:
            formatter, options = factory()
            parser.add_formatter(name, formatter, **options)
    return parser
