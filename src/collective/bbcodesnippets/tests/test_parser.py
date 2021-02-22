from plone.testing.zca import UNIT_TESTING

import unittest


class TestParserBasic(unittest.TestCase):
    """Test parser creation."""

    def test_empty_create_parser(self):
        """Test if a naked parser is created"""
        from collective.bbcodesnippets.parser import create_parser

        import bbcode

        parser = create_parser()
        self.assertIsInstance(parser, bbcode.Parser)


class TestParserBasic(unittest.TestCase):
    """Test parser creation."""

    layer = UNIT_TESTING

    def test_empty_create_parser(self):
        """Test if a naked parser is created"""

        def dummy_formatter(name, value, options, parent, context):
            return "DUMMY"

        from collective.bbcodesnippets.interfaces import IFormatterFactory
        from zope.interface import provider

        @provider(IFormatterFactory)
        def dummy_factory():
            return dummy_formatter, {}

        from zope.component import provideUtility

        provideUtility(dummy_factory, name="dummy")

        from collective.bbcodesnippets.parser import create_parser

        parser = create_parser()

        self.assertEqual(parser.format("[dummy]"), "DUMMY")
