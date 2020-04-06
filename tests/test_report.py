# -*- coding: utf-8 -*-
from reportng import Reportng, Assets
from pathlib import Path

Assets.download(download_path="./tests/dtest/", rel_path="/", theme="pulse")
print("download_assets")

r = Reportng(
    report_name="pytest",
    brand="test",
    use_asciinema=True,
    highlight_code=True,
    show_progress_bar=True,
    theme_preview=True,
)

content = (
    """
        # fasfdds
        # fdsfsfsd
        # fdsfasdfsd
        # fdsfsdf
        # Malmö
        # 아름다운
        # 你好"""
    * 100
)


def test_section():

    r.section(
        title="title",
        content=content,
        keep_formatting=True,
        section_color="red",
        text_color="primary",
        add_alert={"color": "green", "message": "some message here"},
        is_section=False,
        add_badge=[{"color": "red", "message": "red badge"}],
        add_reference={"color": "green", "link": "https://google.com"},
    )


def test_listgroup():
    r.list_group(
        "some title", ["some nonsense", "some other nonense", "hello world"],
    )

    r.section(
        title="title",
        content=content,
        keep_formatting=True,
        section_color="red",
        is_section=False,
        text_color="red",
        use_h2_title=True,
    )


def test_imagegroup():
    r.image_carousel([{"path": "a", "caption": ""}, {"path": "b", "caption": "sdaa"}])


def test_asciinema():
    r.asciinema(
        asciinema_link="https://asciinema.org/a/123683",
        title="title",
        add_alert={"color": "green", "message": "some message here"},
    )


def test_code():
    r.code(
        title="title",
        content="""
        $(document).ready(function() {
        $('pre code').each(function(i, block) {
            hljs.highlightBlock(block);
        });
        });)""",
        add_alert={"color": "green", "message": "some message here"},
    )


def test_collapsible():
    r.section_collapsible("some title", content, "green")


def test_caption():
    r.captions("test")


def test_table():
    r.table(
        data=[
            [
                "a data",
                "b data",
                "c data",
                "e data",
                "f data",
                "e data",
                "f data",
                "e data",
                "f data",
                "e data",
                "f data",
            ],
            [
                "a data",
                "b data",
                "c data",
                "e data",
                "f data",
                "e data",
                "f data",
                "e data",
                "f data",
                "e data",
            ],
        ],
        table_header=[
            "1st header",
            "2nd header",
            "3rd header",
            "4th header",
            "5th header",
            "5th header",
            "5th header",
            "5th header",
            "5th header",
            "5th header",
            "5th header",
        ],
        section_title="Tables are nonsense",
        add_alert={"color": "green", "message": "some message here"},
        is_section=True,
        header_color="red",
    )


def test_cards():
    r.cards(
        [
            {"color": "primary", "title": "a", "message": "a"},
            {"color": "danger", "title": "a", "message": "a"},
        ],
        is_section=True,
        section_title="title",
        border_only=True,
    )


def test_customhtml():
    r.custom_html("<p>some text</p>")


def test_footer():
    r.footer(
        message="message", github="a", linkedin="a", email="a", twitter="a",
    )


# def test_save():
r.save("./tests/dtest/test.html")
