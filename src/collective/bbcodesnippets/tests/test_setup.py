from collective.bbcodesnippets.testing import BBCODESNIPPETS_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.bbcodesnippets is properly installed."""

    layer = BBCODESNIPPETS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.bbcodesnippets is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.bbcodesnippets")
        )

    def test_browserlayer(self):
        """Test that ICollectiveBookmarksLayer is registered."""
        from collective.bbcodesnippets.interfaces import IBBCodeSnippetsLayer
        from plone.browserlayer import utils

        self.assertIn(IBBCodeSnippetsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    """Test that collective.bbcodesnippets is properly uninstalled."""

    layer = BBCODESNIPPETS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get(userid=TEST_USER_ID).getRoles()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.bbcodesnippets")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.bbcodesnippets is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("collective.bbcodesnippets"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveBookmarksLayer is removed."""
        from collective.bbcodesnippets.interfaces import IBBCodeSnippetsLayer
        from plone.browserlayer import utils

        self.assertNotIn(IBBCodeSnippetsLayer, utils.registered_layers())
