from . import _
from .interfaces import IFormatterFactory
from operator import itemgetter
from plone.app.registry.browser import controlpanel
from plone.app.vocabularies.terms import TermWithDescription
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component import getUtilitiesFor
from zope.interface import Interface
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def available_formatters_vocabulary_factory(context):
    terms = []
    for name, factory in sorted(getUtilitiesFor(IFormatterFactory), key=itemgetter(0)):
        terms.append(TermWithDescription(name, name, name, description=factory.__doc__))
    return SimpleVocabulary(terms)


class IBBCodeSnippetsSettings(Interface):
    formatters = schema.List(
        title=_("Available Formatters"),
        description=_("Selected formatters will be enabled in the portal."),
        value_type=schema.Choice(
            vocabulary="bbcodesnippets.available_formatters_vocabulary",
        ),
        default=[],
        missing_value=[],
        required=False,
    )


class BBCodeControlPanelForm(controlpanel.RegistryEditForm):

    id = "BBCodeControlPanel"
    label = _("BBCode Snippets")
    description = _("BBCode snippets settings.")
    schema = IBBCodeSnippetsSettings
    schema_prefix = "bbcodesnippets"

    def updateFields(self):
        super().updateFields()
        self.fields["formatters"].widgetFactory = CheckBoxFieldWidget


class BBCodeControlPanel(controlpanel.ControlPanelFormWrapper):
    form = BBCodeControlPanelForm
