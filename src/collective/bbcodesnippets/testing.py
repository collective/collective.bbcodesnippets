from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer


class CollectiveBbcodesnippetsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.bbcodesnippets
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.bbcodesnippets)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.bbcodesnippets:default")


BBCODESNIPPETS_FIXTURE = CollectiveBbcodesnippetsLayer()


BBCODESNIPPETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BBCODESNIPPETS_FIXTURE,),
    name="CollectiveBbcodesnippetsLayer:IntegrationTesting",
)


BBCODESNIPPETS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BBCODESNIPPETS_FIXTURE,),
    name="CollectiveBbcodesnippetsLayer:FunctionalTesting",
)
