from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBBCodeSnippetsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFormatterFactory(Interface):
    def __call__():
        """create a new bbcode formatter."""
