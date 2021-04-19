from .interfaces import IBBCodeSnippetsLayer
from .interfaces import IFormatterFactory
from plone import api
from Products.CMFPlone.patterns.tinymce import TinyMCESettingsGenerator
from zope.component import getUtilitiesFor

import copy


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
            items.append("bbcs{}".format(name))
        if items:
            MAIN = "bbcs"
            tiny_config = copy.deepcopy(tiny_config)            
            submenu = tiny_config["menu"].get(
                MAIN, {"title": "BBCode Snippets"}
            )
            submenu["items"] = " ".join(items)
            tiny_config["menu"][MAIN] = submenu

            if MAIN not in tiny_config["menubar"]:
                tiny_config["menubar"].append(MAIN)

    return tiny_config


TinyMCESettingsGenerator.get_tiny_config = _patched_get_tiny_config
