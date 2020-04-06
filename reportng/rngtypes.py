from typing_extensions import TypedDict, Literal


class ImageCarouselType(TypedDict):
    path: str
    caption: str


class Alert(TypedDict):
    color: str
    message: str


class Reference(TypedDict):
    color: str
    link: str


class Message(TypedDict):
    color: str
    message: str


class Modal(TypedDict):
    button: str
    title: str
    message: str

class Badge(TypedDict):
    color: str
    message: str


class Cards(TypedDict):
    color: Literal[
        "primary",
        "secondary",
        "success",
        "danger",
        "warning",
        "info",
        "light",
        "dark",
        "default",
        "red",
        "green",
        "blue",
        "yellow",
        "light",
    ]
    title: str
    message: str
