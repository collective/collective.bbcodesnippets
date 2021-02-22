from . import _
from plone.app.registry.browser import controlpanel
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import provider
from z3c.form.browser.checkbox import CheckBoxFieldWidget

@provider(IVocabularyFactory)
def available_formatters_vocabulary_factory(context):
    return SimpleVocabulary([SimpleTerm("foo", title=_("Foo"))])


class IBBCodeSnippetsSettings(Interface):
    formatters = schema.List(
        title=_("Active Formatters"),
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
        self.fields['formatters'].widgetFactory = CheckBoxFieldWidget

class BBCodeControlPanel(controlpanel.ControlPanelFormWrapper):
    form = BBCodeControlPanelForm
