from .mocks import mock_get_registry_record
from plone.testing.zca import UNIT_TESTING
from unittest import TestCase


try:
    from unittest import mock
except ImportError:
    import mock


@mock.patch(
    "plone.api.portal.get_registry_record", new_callable=mock_get_registry_record
)
class TestParserBasic(TestCase):
    """Test parser creation."""

    def test_empty_create_parser(self, *args):
        """Test if a naked parser is created"""
        from collective.bbcodesnippets.parser import create_parser

        import bbcode

        parser = create_parser()
        self.assertIsInstance(parser, bbcode.Parser)


@mock.patch(
    "plone.api.portal.get_registry_record", new_callable=mock_get_registry_record
)
class TestParserBasic(TestCase):
    """Test parser creation."""

    layer = UNIT_TESTING

    def test_non_empty_create_parser(self, *args):
        """Test if a naked parser is created"""
        from collective.bbcodesnippets.interfaces import IFormatterFactory
        from collective.bbcodesnippets.parser import create_parser
        from zope.component import provideUtility
        from zope.interface import provider

        TRANSFORMED = "DUMMY"

        def dummy_formatter(name, value, options, parent, context):
            return TRANSFORMED

        @provider(IFormatterFactory)
        def dummy_factory():
            return dummy_formatter, {"standalone": True}

        # breakpoint()
        provideUtility(dummy_factory, name="dummy")

        parser = create_parser()

        self.assertEqual(parser.format("[dummy]"), TRANSFORMED)
