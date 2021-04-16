from .interfaces import IBBCodeSnippetesMainMenuItem
from .interfaces import IBBCodeSnippetesMenu
from .interfaces import IFormatterFactory
from plone import api
from zope.browsermenu.menu import BrowserMenu
from zope.browsermenu.menu import BrowserSubMenuItem
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer


_ = MessageFactory("my.fancy")


@implementer(IBBCodeSnippetesMainMenuItem)
class BBCodeSnippetesMainMenuItem(BrowserSubMenuItem):
    # This is in fact a submenu item of the parent menu, thus the name
    # of the inherited class tells it, don't be confused.

    title = _(u"label_bbcodesnippets_menu", default=u"BBCode Snippets")
    description = _(
        u"title_bbcodesnippets_menu", default=u"Copy BBCode snippets to clipboard"
    )
    submenuId = "bbcodesnippets_menu"

    order = 1000
    extra = {
        "id": "bbcodesnippets-menu",
        "li_class": "plonetoolbar-content-bbcodesnippets",
    }

    @property
    def action(self):
        # return the url to be loaded if clicked on the link.
        # even if a submenu exists it will be active if javascript is disabled
        return self.context.absolute_url()

    def available(self):
        # check if the menu is available and shown or not
        return bool(
            {name for name, factory in getUtilitiesFor(IFormatterFactory)}
            & set(api.portal.get_registry_record("bbcodesnippets.formatters"))
        )

    def selected(self):
        # check if the menu should be shown as selected
        return False


@implementer(IBBCodeSnippetesMenu)
class BBCodeSnippetesMenu(BrowserMenu):
    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []
        enabled = api.portal.get_registry_record("bbcodesnippets.formatters")
        for name, factory in getUtilitiesFor(IFormatterFactory):
            if name not in enabled or not factory.__doc__:
                continue
            results.append(
                {
                    "title": name,
                    "description": "Copy {0} to clipboard.".format(
                        factory.__bbcode_copy_snippet__
                    ),
                    "action": "javascript:navigator.clipboard.writeText('{0}');document.getElementById('bbcodesnippets-menu').classList.remove('active');".format(
                        factory.__bbcode_copy_snippet__
                    ),
                    "selected": False,
                    "icon": "",
                    "submenu": None,
                    "extra": {
                        "id": "plone-contentmenu-my-fancy-one",
                        "separator": None,
                    },
                }
            )

        return results
