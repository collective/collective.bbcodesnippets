from .interfaces import IFormatterFactory
from zope.interface import provider

import bbcode
import re


# parts of this code are inspired by and partly taken from
# https://github.com/dcwatson/bbcode/blob/master/bbcode.py


# b 	[b]test[/b] 	<strong>test</strong>
# i 	[i]test[/i] 	<em>test</em>
# u 	[u]test[/u] 	<u>test</u>
# s 	[s]test[/s] 	<strike>test</strike>
# hr 	[hr] 	<hr />
# br 	[br] 	<br />
# sub 	x[sub]3[/sub] 	x<sub>3</sub>
# sup 	x[sup]3[/sup] 	x<sup>3</sup>
# list/* 	[list][*] item[/list] 	<ul><li>item</li></ul>
# quote 	[quote]hello[/quote] 	<blockquote>hello</blockquote>
# code 	[code]x = 3[/code] 	<code>x = 3</code>
# center 	[center]hello[/center] 	<div style="text-align:center;">hello</div>
# color 	[color=red]red[/color] 	<span style="color:red;">red</span>
# url 	[url=www.apple.com]Apple[/url] 	<a href="http://www.apple.com">Apple</a>

TEMPLATES = {
    "url": '<a rel="nofollow" href="{href}">{text}</a>',
}


def make_simple_formatter(tag_name, format_string, **kwargs):
    """
    Creates a formatter that takes the tag options dictionary, puts a value key
    in it, and uses it as a format dictionary to the given format string.
    """

    def _render(name, value, options, parent, context):
        fmt = {}
        if options:
            fmt.update(options)
        fmt.update({"value": value})
        return format_string % fmt

    return _render


@provider(IFormatterFactory)
def b_factory():
    """Bold or strong text: <pre>A [b]bold[/b] text.</pre><br />
    Example:<br />
    A [b]bold[/b] text.
    """
    return make_simple_formatter("b", "<strong>%(value)s</strong>"), {}


@provider(IFormatterFactory)
def i_factory():
    """Italic or emphasised text: <pre>An [i]italic/emphasised[/i] text.</pre><br />
    Example:<br />
    An [i]italic/emphasised[/i] text.
    """
    return make_simple_formatter("i", "<em>%(value)s</em>"), {}


@provider(IFormatterFactory)
def u_factory():
    """Underlined or unarticulated text: <pre>An [u]underlined[u] text.</pre><br />
    Example:<br />
    An [u]underlined[/u] text.
    """
    return make_simple_formatter("u", "<u>%(value)s</u>"), {}


@provider(IFormatterFactory)
def s_factory():
    """Strike through or deleted text: [s]test[/s]"""
    return make_simple_formatter("s", "<del>%(value)s</del>"), {}


@provider(IFormatterFactory)
def sub_factory():
    """Subscript text: <pre>H[sub]2[/sub]O</pre><br />
    Example:<br />
    H[sub]2[/sub]O
    """
    return make_simple_formatter("sub", "<sub>%(value)s</sub>"), {}


@provider(IFormatterFactory)
def sup_factory():
    """Superscript text: <pre>r[sup]2[/sup]</pre><br />
    Example:<br />
    r[sup]2[/sup]
    """
    return make_simple_formatter("sup", "<sup>%(value)s</sup>"), {}


@provider(IFormatterFactory)
def hr_factory():
    """Horizontal ruler: <pre>Above ruler[hr]Below ruler</pre><br />
    Example:<br />

    Above ruler[hr]Below ruler
    """
    return make_simple_formatter("hr", "<hr />"), {"standalone": True}


@provider(IFormatterFactory)
def br_factory():
    """Line break in text: <pre>A line[br]break in the text.</pre><br />
    Example:<br />
    A line[br]break in the text.
    """
    return make_simple_formatter("br", "<br />"), {"standalone": True}


@provider(IFormatterFactory)
def list_factory():
    """List with bullets or numbers. Use '*' for bullet points or for numbers one out of '1', '01, 'a', 'A', 'i' or 'I'.
    Bullet points: [list][*] item[/list]
    Numbered: [list][1] item[/list]
    """

    def _render_list(name, value, options, parent, context):
        list_type = options["list"] if (options and "list" in options) else "*"
        css_opts = {
            "1": "decimal",
            "01": "decimal-leading-zero",
            "a": "lower-alpha",
            "A": "upper-alpha",
            "i": "lower-roman",
            "I": "upper-roman",
        }
        tag = "ol" if list_type in css_opts else "ul"
        css = (
            ' style="list-style-type:%s;"' % css_opts[list_type]
            if list_type in css_opts
            else ""
        )
        return "<%s%s>%s</%s>" % (tag, css, value, tag)

    return _render_list, {
        "transform_newlines": False,
        "strip": True,
        "swallow_trailing_newline": True,
    }


@provider(IFormatterFactory)
def list_item_factory():
    # no doc string, so will not appear in documentation, helper for list
    def _render_list_item(name, value, options, parent, context):
        if not parent or parent.tag_name != "list":
            return "[*]%s<br />" % value

        return "<li>%s</li>" % value

    return _render_list_item, {
        "newline_closes": True,
        "transform_newlines": False,
        "same_tag_closes": True,
        "strip": True,
    }


@provider(IFormatterFactory)
def quote_factory():
    return make_simple_formatter("quote", "<blockquote>%(value)s</blockquote>"), {
        "strip": True,
        "swallow_trailing_newline": True,
    }


@provider(IFormatterFactory)
def code_factory():
    """Code text: <pre>Some random Code: [code]print("Hello World")[/code]</pre><br />
    Example:<br />
    Some random Code: [code]print("Hello World")[/code]
    """

    return make_simple_formatter("code", "<code>%(value)s</code>"), {
        "render_embedded": False,
        "transform_newlines": False,
        "swallow_trailing_newline": True,
        "replace_cosmetic": False,
    }


@provider(IFormatterFactory)
def color_factory():
    def _render_color(name, value, options, parent, context):
        if "color" in options:
            color = options["color"].strip()
        elif options:
            color = list(options.keys())[0].strip()
        else:
            return value
        match = re.match(r"^([a-z]+)|^(#[a-f0-9]{3,6})", color, re.I)
        color = match.group() if match else "inherit"
        return '<span style="color:%(color)s;">%(value)s</span>' % {
            "color": color,
            "value": value,
        }

    return _render_color(), {}


@provider(IFormatterFactory)
def center_factory():
    """Centered text: <pre>[center]centered text[/center]</pre><br />
    Example:<br />
    [center]centered text[/center]
    """

    return (
        make_simple_formatter(
            "center", '<div style="text-align:center;">%(value)s</div>'
        ),
        {},
    )


@provider(IFormatterFactory)
def url_factory():
    """A hyper link in the text: <pre>Welcome to [url=www.plone.org]Plone[/url]!</pre><br />
    Example:<br />
    Welcome to [url=www.plone.org]Plone[/url]!
    """

    def _render_url(name, value, options, parent, context):
        if options and "url" in options:
            href = options["url"]
            # Option values are not escaped for HTML output.
            for find, repl in bbcode.Parser.REPLACE_ESCAPE:
                value = value.replace(find, repl)
        else:
            href = value
        # Completely ignore javascript: and data: "links".
        if re.sub(r"[^a-z0-9+]", "", href.lower().split(":", 1)[0]) in (
            "javascript",
            "data",
            "vbscript",
        ):
            return ""
        # Only add the missing https:// if it looks like it starts with a domain name.
        if "://" not in href and bbcode._domain_re.match(href):
            href = "https://" + href
        return TEMPLATES["url"].format(href=href.replace('"', "%22"), text=value)

    return _render_url, {"replace_links": False, "replace_cosmetic": False}
