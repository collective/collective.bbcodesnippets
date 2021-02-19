from .parser import create_parser
from lxml import etree
from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implements(ITransform)
@adapts(Interface, IBBCodeSnippetsLayer)
class BBCodeSnippetsTransform(object):

    # after diazo (plone.app.theming) which is 8850
    order = 9000

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def parseTree(self, result):
        contentType = self.request.response.getHeader("Content-Type")
        if contentType is None or not contentType.startswith("text/html"):
            return None

        if self.request.response.getHeader("Content-Encoding") in (
            "zip",
            "deflate",
            "compress",
        ):
            return None

        try:
            return getHTMLSerializer(result, pretty_print=False)
        except (AttributeError, TypeError, etree.ParseError):
            return None

    def transformBytes(self, result, encoding):
        try:
            result = result.decode(encoding)
        except UnicodeDecodeError:
            # This is probably a file or an image
            # FIXME probably we do not event want to apply
            # this transform for files and images
            return None
        return self.transformIterable([result], encoding)

    def transformString(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformUnicode(self, result, encoding):
        return self.transformIterable([result], encoding)

    def create_parser(self, root):
        self.parser = create_parser()

    def transformIterable(self, result, encoding):
        result = self.parseTree(result)
        if result is None:
            return None

        for el in etree.iterwalk(result.tree):
            pass

        return result
