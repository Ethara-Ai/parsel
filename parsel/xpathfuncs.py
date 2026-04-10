from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from lxml import etree
from w3lib.html import HTML5_WHITESPACE

if TYPE_CHECKING:
    from collections.abc import Callable

regex = f"[{HTML5_WHITESPACE}]+"
replace_html5_whitespaces = re.compile(regex).sub


def set_xpathfunc(fname: str, func: Callable | None) -> None:  # type: ignore[type-arg]
    """Register a custom extension function to use in XPath expressions.

    The function ``func`` registered under ``fname`` identifier will be called
    for every matching node, being passed a ``context`` parameter as well as
    any parameters passed from the corresponding XPath expression.

    If ``func`` is ``None``, the extension function will be removed.

    See more `in lxml documentation`_.

    .. _`in lxml documentation`: https://lxml.de/extensions.html#xpath-extension-functions

    """
    ns_fns = etree.FunctionNamespace(None)
    if func is not None:
        ns_fns[fname] = func
    else:
        del ns_fns[fname]


def setup() -> None:
    set_xpathfunc("has-class", has_class)


def has_class(context: Any, *classes: str) -> bool:
    """has-class function.

    Return True if all ``classes`` are present in element's class attr.

    """
    pass
