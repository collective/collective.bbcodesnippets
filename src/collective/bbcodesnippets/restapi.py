from plone.restapi.services import Service
from plone import api
from zope.component import getUtilitiesFor
from .interfaces import IFormatterFactory

class EnabledSnippetsGet(Service):
    def reply(self):
        """get enabled bbcode snippets
        """
        result = []
        enabled = api.portal.get_registry_record("bbcodesnippets.formatters")
        for name, factory in getUtilitiesFor(IFormatterFactory):
            if name not in enabled or not factory.__doc__:
                continue
            result.append( 
                {
                    "name": name,
                    "snippet": factory.__bbcode_copy_snippet__,
                }
            )
        return result
