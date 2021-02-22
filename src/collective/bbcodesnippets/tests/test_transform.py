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
class TestTransformer(TestCase):
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
        result = transformer.transformIterable(source, None)
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

    def test_no_html_xml__no_formatter_transform(self, *args):
        """Test if nothing is done w/o xml/html"""
        source = "[foo]"
        transformed = source

        self._do_transform(source)
        self.assertEqual(source, transformed)

    def test_html_no_formatter(self, *args):
        """Test if nothing is done w/o formaters"""

        source = "<X>[dummy]</X>"
        transformed = source

        self._do_transform(source)
        self.assertEqual(source, transformed)

    def test_no_html_xml_with_formatter_transform(self, *args):
        """Test if nothing is done with formaters but on non-xml/html"""

        source = "[dummy]"
        transformed = source

        self._register_formatter()
        self._do_transform(source)
        self.assertEqual(source, transformed)

    def test_html_xml_with_formatter_transform(self, *args):
        """Test if nothing is done with formaters but on non-xml/html"""

        source = "<x>[dummy]</x>"
        transformed = b"<x>DUMMY</x>"

        self._register_formatter()
        result = self._do_transform(source)
        self.assertIn(transformed, result.serialize())

    def test_html_with_tail(self, *args):
        """Test if nothing is done with formaters but on non-xml/html"""

        source = "<p>1 [dummy] 2<br>3 [dummy] 4</p>"
        transformed = b"<p>1 DUMMY 2<br>3 DUMMY 4</p>"

        self._register_formatter()
        result = self._do_transform(source)
        self.assertIn(transformed, result.serialize())

    def test_complex_html(self, *args):
        """All should  be transformed."""

        source = '<div>[dummy]<article>1[dummy] 2<br>3[dummy] 4 <a href="">5 [dummy] 6</a>[dummy]</article><p>[dummy]</p>[dummy]</div>'
        transformed = b'<div>DUMMY<article>1DUMMY 2<br>3DUMMY 4 <a href="">5 DUMMY 6</a>DUMMY</article><p>DUMMY</p>DUMMY</div>'

        self._register_formatter()
        result = self._do_transform(source)
        self.assertIn(transformed, result.serialize())

    def test_deny_on_complex_html(self, *args):
        """Textarea should not be transformed."""

        source = '<div>[dummy]<textarea>1[dummy] 2<br>3[dummy] 4 <a href="">5 [dummy] 6</a>[dummy]</textarea><p>[dummy]</p>[dummy]</div>'
        transformed = b'<div>DUMMY<textarea>1[dummy] 2<br>3[dummy] 4 <a href="">5 [dummy] 6</a>[dummy]</textarea><p>DUMMY</p>DUMMY</div>'

        self._register_formatter()
        result = self._do_transform(source)
        self.assertIn(transformed, result.serialize())
