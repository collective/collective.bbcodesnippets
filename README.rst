`collective.bbcodesnippets <http://pypi.python.org/pypi/collective.bbcodesnippets>`_ provides pervasive, generic and extensible `BBCode Markup <https://en.wikipedia.org/wiki/BBCode>`_ integration for Plone.

Functionality
=============

*collective.bbcodesnippets* replaces BBCode in the whole generated HTML output.
BBCode snippets can be placed everywhere in the site. 

At transform time at the end of the chain, before or after Diazo (configurable), the output is parsed and all BBCode will be replaced.

The BBCode parser only replaces configured BBCode snippets. 
At the control panel all registered BBCodes are listed to be activated.
By default all codes are inactive.

This package utilizes the excellent `bbcode package <https://pypi.org/project/bbcode/>`_  from Dan Watson to parse and replace.
We register all `default formatters <https://dcwatson.github.io/bbcode/tags/>`_ as named utilities which are used as factories for the formatter using the Zope Component Architecture (ZCA). 
Custom parsers can be provided by registering an own named utility.
Before parsing at transform time new Parser is created using the configured adapters only.


Installation
------------

Install collective.bbcodesnippets by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.bbcodesnippets


and then running ``buildout``.

Afterwards (re)start Plone, go to the controlpanel and install the addon. 

Then there is a conrol-panel to control the allowed BBcodes.


Source Code
===========

.. image:: https://github.com/collective/collective.bbcodesnippets/actions/workflows/tests.yaml/badge.svg
    :target: https://github.com/collective/collective.bbcodesnippets/actions/workflows/tests.yaml
    :alt: Build and Test

The sources are in a GIT DVCS with its main branches at `github <http://github.com/collective/collective.bbcodesnippets>`_.

We'd be happy to see many forks and pull-requests to make collective.bbcodesnippets even better.


Contributors
============

- `Jens W. Klein, Klein & Partner KG  <https://github.com/jensens>`_- Author

- `Michael Graf, FH St.Pölten <https://github.com/2silver>`_ - Idea and Use Case

Thanks to `St. Pölten University of Applied Sciences <https://www.fhstp.ac.at>`_ for initial funding.
