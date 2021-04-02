from .interfaces import IBBCodeSnippetsLayer
from .parser import create_parser
from lxml import etree
from plone.transformchain.interfaces import ITransform
from re import L
from repoze.xmliter.utils import getHTMLSerializer
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import logging


try:
    from html import escape
except ImportError:
    from cgi import escape

logger = logging.getLogger(__name__)

DENYLIST = ["textarea", "script", "link", "pre"]


@implementer(ITransform)
@adapter(Interface, IBBCodeSnippetsLayer)
class BBCodeSnippetsTransform(object):

    # after diazo (plone.app.theming) which is 8850
    order = 8960

    def __init__(self, published, request):
        self.published = published
        contentType = request.response.getHeader("Content-Type")
        self.valid = (
            contentType is not None
            and contentType.startswith("text/html")
            and not request.response.getHeader("Content-Encoding")
            in (
                "zip",
                "deflate",
                "compress",
            )
        )
        if self.valid:
            self.parser = create_parser()

    def parse_tree(self, result):
        try:
            return getHTMLSerializer(result, pretty_print=False)
        except (AttributeError, TypeError, etree.ParseError):
            return None

    def denylist(self):
        return DENYLIST

    def transformBytes(self, result, encoding):
        if not self.valid:
            return None
        try:
            result = result.decode(encoding)
        except UnicodeDecodeError:
            return None
        return self.transformIterable([result], encoding)

    def transformString(self, result, encoding):
        if not self.valid:
            return None
        return self.transformIterable([result], encoding)

    def transformUnicode(self, result, encoding):
        if not self.valid:
            return None
        return self.transformIterable([result], encoding)

    def transformIterable(self, result, encoding):
        if not self.valid:
            return None
        result = self.parse_tree(result)
        if result is None:
            return None

        denylist = self.denylist()
        parser = self.parser

        def _handle_text(el):
            # escape all literal tags in here and format with bbcode
            try:
                formatted = parser.format(escape(el.text))
            except Exception:
                logger.exception("BBCode format failed.")
                return el
            # wrap in element, now we have the new subtree
            try:
                sub = etree.fromstring("<bbcs>{}</bbcs>".format(formatted))
            except Exception:
                logger.exception("BBCode result is not valid xml failed.")
                return el
            # a text is replaced by a new text followed by new children
            # the new children got all inserted as first, shifting existing ones back
            # any new tail is already the tail of the last new child, so no action needed here.
            el.text = sub.text
            last_subel = None
            for deltaindex, subel in enumerate(sub.iterchildren()):
                el.insert(deltaindex, subel)
                last_subel = subel
            return last_subel

        def _handle_tail(el, last_sub):
            # escape all literal tags in here and format with bbcode
            try:
                formatted = parser.format(escape(el.tail))
            except Exception:
                logger.exception("BBCode format failed.")
                return
            # wrap in element, now we have the new subtree
            try:
                new_tail_structure = etree.fromstring(
                    "<bbcs>{}</bbcs>".format(formatted)
                )
            except Exception:
                logger.exception("BBCode result is not valid xml, failed.")
                return

            # A new "tail" structure may have a text and 1..n children,
            # but never has a tail (this is how lxml parses it, its on the last child).

            # The new text is the new tail
            el.tail = new_tail_structure.text

            # Children are just appended behind el
            parent = el.getparent()
            baseindex = parent.index(el) + 1
            current = el
            for deltaindex, child in enumerate(new_tail_structure.iterchildren()):
                parent.insert(baseindex + deltaindex, child)

        def _process_node(el):
            # process nodes depth first to avoid parsing just generated nodes.
            for cel in el.getchildren():
                if cel.tag in denylist:
                    continue
                _process_node(cel)

            if el.text and el.text.strip():
                last_sub = _handle_text(el)
            else:
                last_sub = None
            if el.tail and el.tail.strip():
                _handle_tail(el, last_sub)

        _process_node(result.tree.getroot())
        return result
