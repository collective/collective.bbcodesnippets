from collective.ftw.upgrade import UpgradeStep
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging
import re

logger = logging.getLogger(__name__)


class Plone6Upgrade(UpgradeStep):
    """Plone 6 upgrade."""

    def __call__(self):
        self.install_upgrade_profile()
        self.cleanup_resource_registry()

    def cleanup_resource_registry(self):
        """Remove remaining deprecated Plone 5 resource registry records."""
        # Regex for deprecated resource registry keys.
        resource_regex = re.compile(
            r"plone.bundles/collective-bbcodesnippets-app.("
            "compile|"
            "develop_css|"
            "develop_javascript|"
            "last_compilation|"
            "merge_with|"
            "resources|"
            "stub_js_modules"
            ")"
        )
        registry = getUtility(IRegistry)

        # Create a static list of registry keys to not operate on a live iterator
        # which changes size when deleting keys.
        keys = list(registry.records.keys())
        for key in keys:
            # Remove "plone.resources", "plone.lessvariables" and deprecated bundle keys.
            if (
                "plone.resources" == key[:15]
                or key == "plone.lessvariables"
                or resource_regex.match(key)
            ):
                del registry.records[key]
                logger.info("Removed deprecated registry record %s.", key)
