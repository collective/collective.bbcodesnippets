from collective.ftw.upgrade import UpgradeStep


class Plone6Upgrade(UpgradeStep):
    """Plone 6 upgrade."""

    def __call__(self):
        self.install_upgrade_profile()
