from .parser import create_parser
from lxml import etree
from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ITransform)
@adapter(Interface, IBBCodeSnippetsLayer)
class BBCodeSnippetsTransform(object):

    # after diazo (plone.app.theming) which is 8850
    order = 9000

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def parseTree(self, result):
        contentType = self.request.response.getHeader("Content-Type")
        if (
            contentType is None
            or not contentType.startswith("text/html")
            or self.request.response.getHeader("Content-Encoding")
            in (
                "zip",
                "deflate",
                "compress",
            )
        ):
            return None

        try:
            return getHTMLSerializer(result, pretty_print=False)
        except (AttributeError, TypeError, etree.ParseError):
            return None

    def denylist(self):
        return ["textarea"]

    def transformBytes(self, result, encoding):
        try:
            result = result.decode(encoding)
        except UnicodeDecodeError:
            return None
        return self.transformIterable([result], encoding)

    def transformString(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformUnicode(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformIterable(self, result, encoding):
        parser = create_parser()
        result = self.parseTree(result)
        if result is None:
            return None
        denylist = self.denylist()
        for el in etree.iterwalk(result.tree):
            if el.text and el.tag.lower() not in denylist:
                el.text = parser.transform(el.text)
            if el.tail and el.getParent().tag.lower() not in denylist:
                el.tail = parser.transform(el.tail)
        return result
