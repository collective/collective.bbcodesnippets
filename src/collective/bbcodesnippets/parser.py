from .controlpanel import IBBCodeSnippetsSettings
from .interfaces import IFormatterFactory
from plone import api
from zope.component import getUtilitiesFor

import bbcode


# possible alternative https://github.com/TamiaLab/PySkCode
# + many more features
# + better code and concept
# + easier to plugin, better architecture
# - no release on PyPI
# - stalled project -> would need takeover/fork


class Parser(bbcode.Parser):
    def format(self, data, **context):
        """
        Formats the input text using any installed renderers. Any context keyword arguments
        given here will be passed along to the render functions as a context dictionary.
        """
        tokens = self.tokenize(data)
        full_context = self.default_context.copy()
        full_context.update(context)
        result = self._format_tokens(tokens, None, **full_context)
        if self.newline:
            return result.replace("\r", self.newline)
        return result


def _null_linker(url):
    return url


def create_parser():
    enabled = api.portal.get_registry_record("bbcodesnippets.formatters")
    parser = Parser(
        newline=None,
        install_defaults=False,
        escape_html=False,
        replace_cosmetic=False,
        linker=_null_linker,
    )
    for name, factory in getUtilitiesFor(IFormatterFactory):
        __traceback_info__ = name
        if name in enabled:
            formatter, options = factory()
            parser.add_formatter(name, formatter, **options)
    return parser
