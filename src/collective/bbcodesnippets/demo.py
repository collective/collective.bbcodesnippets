from .interfaces import IFormatterFactory
from plone import api
from Products.Five.browser import BrowserView
from zope.component import getUtilitiesFor


class DemoView(BrowserView):
    def docsnippets(self):
        enabled = api.portal.get_registry_record("bbcodesnippets.formatters")
        for name, factory in getUtilitiesFor(IFormatterFactory):
            if not factory.__doc__:
                continue
            yield {
                "name": name,
                "snippet": factory.__bbcode_copy_snippet__,
                "demo": factory.__doc__,
                "enabled": name in enabled,
            }
