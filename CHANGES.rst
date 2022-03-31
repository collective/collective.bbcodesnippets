
History
=======

1.0.0 (2022-03-31)
------------------

- Fix: prevent to transform ``\n`` to ``&#13;`` by replacing it with nothing.
  [jensens]

- Fix: Remove all settings on uninstall.
  [jensens]


1.0.0b1 (2021-06-07)
--------------------

- Added boolean index to catalog together with indexer detecting BBCodes in content.
  [jensens]


1.0.0a5 (2021-05-25)
--------------------

- Use lxml.html.fromstring for inner HTML parsing to ingest not-so-perfect HTML.
  [jensens]

- Remove explicit order of registration - it has no effect.
  [jensens]


1.0.0a4 (2021-05-23)
--------------------

- Enable explicit order of registration.
  [jensens]


1.0.0a3 (2021-05-19)
--------------------

- Explicit load plone.restapi ZCML to have profile available.


1.0.0a2 (2021-05-19)
--------------------

- Explicit load plone.rest ZCML to have "plone.service" defined.
  [jensens]


1.0.0a1 (2021-05-19)
--------------------

- Fix package configuration
  [jensens]


1.0.0a0 (2021-05-18)
--------------------

- Initial work
  [jensens]
