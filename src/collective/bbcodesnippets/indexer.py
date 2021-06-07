from plone.app.textfield.interfaces import IRichText
from plone.app.textfield.interfaces import IRichTextValue
from plone.dexterity.content import iterSchemata
from plone.indexer.decorator import indexer
from Products.CMFPlone.utils import safe_text
from zope.interface import Interface
from zope.schema.interfaces import IText

import re
import six


_DETECTOR_RE = re.compile(r".*\[[a-z].*?\]")


@indexer(Interface)
def has_bbcode(obj):
    for schema in iterSchemata(obj):
        for field_name in schema:
            field = schema.get(field_name, None)
            value = getattr(obj, field_name, None)
            if isinstance(value, bytes):
                value = safe_text(value)
            elif IRichText.providedBy(field):
                if not IRichTextValue.providedBy(value):
                    continue
                value = value.raw
            if isinstance(value, six.text_type) and _DETECTOR_RE.search(value):
                return True
    return False
