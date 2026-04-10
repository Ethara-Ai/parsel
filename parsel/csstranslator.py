from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, Any, Protocol

from cssselect import GenericTranslator as OriginalGenericTranslator
from cssselect import HTMLTranslator as OriginalHTMLTranslator
from cssselect.parser import Element, FunctionalPseudoElement, PseudoElement
from cssselect.xpath import ExpressionError
from cssselect.xpath import XPathExpr as OriginalXPathExpr

if TYPE_CHECKING:
    # typing.Self requires Python 3.11
    from typing_extensions import Self


class XPathExpr(OriginalXPathExpr):
    textnode: bool = False
    attribute: str | None = None

    @classmethod
    def from_xpath(
        cls,
        xpath: OriginalXPathExpr,
        textnode: bool = False,
        attribute: str | None = None,
    ) -> Self:
        pass

    def __str__(self) -> str:
        path = super().__str__()
        if self.textnode:
            if path == "*":
                path = "text()"
            elif path.endswith("::*/*"):
                path = path[:-3] + "text()"
            else:
                path += "/text()"

        if self.attribute is not None:
            if path.endswith("::*/*"):
                path = path[:-2]
            path += f"/@{self.attribute}"

        return path

    def join(
        self: Self,
        combiner: str,
        other: OriginalXPathExpr,
        *args: Any,
        **kwargs: Any,
    ) -> Self:
        pass


# e.g. cssselect.GenericTranslator, cssselect.HTMLTranslator
class TranslatorProtocol(Protocol):
    def xpath_element(self, selector: Element) -> OriginalXPathExpr:
        pass

    def css_to_xpath(self, css: str, prefix: str = ...) -> str:
        pass


class TranslatorMixin:
    """This mixin adds support to CSS pseudo elements via dynamic dispatch.

    Currently supported pseudo-elements are ``::text`` and ``::attr(ATTR_NAME)``.
    """

    def xpath_element(self: TranslatorProtocol, selector: Element) -> XPathExpr:
        # https://github.com/python/mypy/issues/14757
        pass

    def xpath_pseudo_element(
        self, xpath: OriginalXPathExpr, pseudo_element: PseudoElement
    ) -> OriginalXPathExpr:
        """
        Dispatch method that transforms XPath to support pseudo-element
        """
        pass

    def xpath_attr_functional_pseudo_element(
        self, xpath: OriginalXPathExpr, function: FunctionalPseudoElement
    ) -> XPathExpr:
        """Support selecting attribute values using ::attr() pseudo-element"""
        pass

    def xpath_text_simple_pseudo_element(self, xpath: OriginalXPathExpr) -> XPathExpr:
        """Support selecting text nodes using ::text pseudo-element"""
        pass


class GenericTranslator(TranslatorMixin, OriginalGenericTranslator):
    @lru_cache(maxsize=256)
    def css_to_xpath(self, css: str, prefix: str = "descendant-or-self::") -> str:
        pass


class HTMLTranslator(TranslatorMixin, OriginalHTMLTranslator):
    @lru_cache(maxsize=256)
    def css_to_xpath(self, css: str, prefix: str = "descendant-or-self::") -> str:
        pass


_translator = HTMLTranslator()


def css2xpath(query: str) -> str:
    """Return translated XPath version of a given CSS query"""
    pass
