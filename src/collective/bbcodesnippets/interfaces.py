from zope.interface import Interface


class IFormatterFactory(Interface):
    def __call__():
        """create a new bbcode formatter."""
