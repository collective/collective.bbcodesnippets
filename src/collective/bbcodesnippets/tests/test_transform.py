from plone.testing.zca import UNIT_TESTING

import unittest


class TestTranformer(unittest.TestCase):
    """Test Transformer."""

    layer = UNIT_TESTING

    def _do_transform(self, source):
        from collective.bbcodesnippets.transform import BBCodeSnippetsTransform

        class DummyResponse:
            
            def getHeader(self, name):
                if name == "Content-Type":
                    return "text/html"
                return ""

        class DummyRequest:
            @property
            def response(self):
                return DummyResponse()

        transformer = BBCodeSnippetsTransform(None, DummyRequest())
        result =  transformer.transformIterable(source, None)
        return result

    def _register_formatter(self):
        def dummy_formatter(name, value, options, parent, context):
            return "DUMMY"

        from collective.bbcodesnippets.interfaces import IFormatterFactory
        from zope.component import provideUtility
        from zope.interface import provider

        @provider(IFormatterFactory)
        def dummy_factory():
            return dummy_formatter, {"standalone": True}

        provideUtility(dummy_factory, name="dummy")

    def test_no_html_xml__no_formatter_transform(self):
        """Test if nothing is done w/o xml/html"""

        source = "[foo]"
        transformed = source

        self._do_transform(source)
        self.assertEqual(source, transformed)

    def test_html_no_formatter(self):
        """Test if nothing is done w/o formaters"""

        source = "<X>[dummy]</X>"
        transformed = source

        self._do_transform(source)
        self.assertEqual(source, transformed)

    def test_no_html_xml_with_formatter_transform(self):
        """Test if nothing is done with formaters but on non-xml/html"""

        source = "[dummy]"
        transformed = source

        self._register_formatter()
        self._do_transform(source)
        self.assertEqual(source, transformed)

    def test_html_xml_with_formatter_transform(self):
        """Test if nothing is done with formaters but on non-xml/html"""

        source = "<x>[dummy]</x>"
        transformed = "<x>DUMMY</x>"

        self._register_formatter()
        result = self._do_transform(source)
        self.assertIn(transformed.encode('utf8'), result.serialize())
