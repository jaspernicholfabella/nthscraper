from enum import Enum
from typing import Tuple, Dict


class By(Enum):
    ID = "ID"
    XPATH = "XPATH"
    TEXT = "TEXT_EQUALS"
    LINK_TEXT = "TEXT_CONTAINS"
    TAG_NAME = "TAG_NAME"
    CLASS_NAME = "CLASS_NAME"


def selector_mode_values(
    by_mode: "By", to_search: str, tag: str = "node()"
) -> Tuple[str, str]:

    selectors: Dict[str, Tuple[str, str]] = {
        "ID": (
            f"<Error: ID '{to_search}' not found in HTML>",
            f'//*[@id="{to_search}"]',
        ),
        "XPATH": (
            f"<Error: XPath '{to_search}' not found in HTML>",
            to_search,
        ),
        "TEXT_EQUALS": (
            f"<Error: No exact text match for '{to_search}'",
            f'//{tag}[normalize-space(text())="{to_search}"]',
        ),
        "TEXT_CONTAINS": (
            f"<Error: No partial text match for '{to_search}'",
            f'//{tag}[contains(text(), "{to_search}")]',
        ),
        "TAG_NAME": (
            f"<Error: Tag '{to_search}' not found in HTML>",
            f"//{to_search}",
        ),
        "CLASS_NAME": (
            f"<Error: Class '{to_search}' not found in HTML>",
            f'//*[contains(concat(" ", normalize-space(@class), " "), " {to_search} ")]',
        ),
    }

    return selectors.get(str(by_mode.value), ("<Error: Invalid search mode>", ""))
