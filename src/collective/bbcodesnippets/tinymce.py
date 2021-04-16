from .interfaces import IBBCodeSnippetsLayer
from .interfaces import IFormatterFactory
from plone import api
from Products.CMFPlone.patterns.tinymce import TinyMCESettingsGenerator
from zope.component import getUtilitiesFor


_original_get_tiny_config = TinyMCESettingsGenerator.get_tiny_config


def _patched_get_tiny_config(self):
    tiny_config = _original_get_tiny_config(self)
    if IBBCodeSnippetsLayer.providedBy(self.request):
        # look if we have something to show
        enabled = api.portal.get_registry_record("bbcodesnippets.formatters")
        items = []
        for name, factory in getUtilitiesFor(IFormatterFactory):
            if name not in enabled or not factory.__doc__:
                continue
            items.append("bbcs_{}".format(name))
        if items:
            tiny_config["plugins"].append("collectivebbcodesnippets")
            tiny_config["menu"]["bbcodesnippets"] = {
                "title": "BBCode Snippets",
                "items": " ".join(items),
            }
            tiny_config["menubar"].append("bbcodesnippets")
    return tiny_config


# TinyMCESettingsGenerator.get_tiny_config = _patched_get_tiny_config
