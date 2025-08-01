from typing import Protocol


class MenuButton(Protocol):
    def on_click(self) -> None: ...
    def clickable(self) -> bool: ...


class PopupButton(MenuButton):
    def on_close(self) -> None: ...
