# coding: utf-8
"""
Python report generator that wraps around bootstrap 4 using dominate.
Usage is simple. Follows header, section..., footer structure. reportng
relies on JS for some of its dynamic properties and has been developed
using modern browsers.
"""
import logging
from pathlib import Path
from collections import OrderedDict
from typing_extensions import Literal, TypedDict
from typing import Union, Tuple, Dict, List
import dominate
import dominate.tags as tag
from dominate.util import raw

from . import rnghelpers as rng
from .rngtypes import *
from .__version__ import __author__, __version__


class Reportng:
    def __init__(
        self,
        report_name: str,
        brand: str,
        use_asciinema: bool = False,
        show_progress_bar: bool = True,
        show_search: bool = True,
        highlight_code: bool = True,
        theme_preview: bool = False,
        user_javascript: str = None,
        user_css: str = None,
        theme: str = "lux",
        use_bootstrap: bool = False,
        search_highlight_color: str = "#f1c40f",
        navbar_background: Literal[
            "primary", "red", "green", "yellow", "blue", "light"
        ] = "primary",
    ):
        """The __init__ method for the `Reportng` class. The init method is used 
        to set the `brand` and `report_name` for the report, along with 
        optional arguments that can control custom css, js, and other built in 
        features of Reportng. Features that can be enabled or disabled includes 
        asciinema, progress bar, search, highlight etc. 
        
        Args:
            report_name (str): The name of the report
            brand (str): The author/brand of the report. 
            use_asciinema (bool, optional): If asciinema player should be used. Defaults to False.
            show_progress_bar (bool, optional): Enable a top scrolling progress bar. Defaults to True.
            show_search (bool, optional): Enable search. Defaults to True.
            highlight_code (bool, optional): Enable code highlight. Defaults to True.
            theme_preview (bool, optional): Preview themes. Defaults to False.
            user_javascript (str, optional): Custom Javascript to inject in the header. Defaults to None.
            user_css (str, optional): Custom CSS to inject in the header. Defaults to None.
            theme (str, optional): A valid Bootstrap 4 theme. Defaults to "lux".
            use_bootstrap (bool, optional): Base Bootstrap 4 theme. Defaults to False.
            search_highlight_color (str, optional): Highlight color for matching search results. Defaults to "#f1c40f".
            navbar_background (Literal[, optional): Color for navbar. Defaults to "primary".
        """
        self.report: str = ""
        self.report_name = report_name
        self.brand = brand
        self.document = dominate.document(title=self.report_name)
        self.__asciinema = use_asciinema
        self.__highlight = highlight_code

        if len(self.report_name) > 40:
            logging.warning(
                "A report_name greater than 40 characters can \
            can cause the navbar to expand and break some functionality. Will use only the first 40 characters"
            )
            self.report_name = "{}...".format(self.report_name[0:37])

        with self.document.head as report_head:
            # link and script builder for bootstrap 4
            tag.comment("Created using reportng by securisec")
            tag.meta(
                charset="utf-8",
                name="viewport",
                content="width=device-width, initial-scale=1",
            )
            # main style components
            tag.script(src=rng.JSCSS.jquery)
            tag.script(src=rng.JSCSS.popper_js)
            tag.script(src=rng.JSCSS.bs4_js)
            if not show_search == False:
                tag.script(src=rng.JSCSS.mark_js)

            # JS for tooltip
            tag.command("JS for tooltip")
            tag.script(raw(rng.JSCustom.tooltip_js))

            # JS for mark_js
            tag.comment("JS for mark.js")
            tag.script(raw(rng.JSCustom.markjs_script))

            # JS to populate the navbar dropdown
            tag.comment("JS to populate the navbar dropdown")
            tag.script(raw(rng.JSCustom.populate_navbar_onload))

            # script that allows for smooth scrolling and adds padding for navbar
            tag.comment(
                "script that allows for smooth scrolling and adds padding for navbar"
            )
            tag.script(raw(rng.JSCustom.smoothscroll_navbar_pad))

            # js to filter in the dropdown menu
            tag.comment("js to filter in the dropdown menu")
            tag.script(raw(rng.JSCustom.dropdown_filter))

            # user insterted JS
            if user_javascript:
                tag.comment("User inserted JS")
                tag.script(raw(user_javascript))

            # bootswatch style sheets
            if use_bootstrap:
                tag.comment("style sheets")
                bootswatch = "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"
            elif theme != "lux":
                bootswatch = "https://bootswatch.com/4/%s/bootstrap.min.css" % theme
            else:
                bootswatch = rng.JSCSS.bootswatch
            tag.link(
                rel="stylesheet", type="text/css", href=bootswatch, id="bootswatch"
            )
            tag.link(href=rng.JSCSS.font_awesome, rel="stylesheet")

            # constructing this way to avoid loading un needed js and css
            # css for asciinema
            if self.__asciinema:
                tag.comment("css for asciinema")
                tag.link(
                    rel="stylesheet", type="text/css", href=rng.JSCSS.asciinema_css
                )

            # css and js for highlight.js
            if self.__highlight == True:
                tag.comment("css and js for highlight.js")
                tag.link(rel="stylesheet", href=rng.JSCSS.highlightjs_css)
                tag.script(src=rng.JSCSS.highlightjs_js)
                tag.script(
                    raw(
                        """
                    hljs.initHighlightingOnLoad();
                    """
                    )
                )

            # script for progress bar
            if show_progress_bar == True:
                tag.comment("js for progress bar")
                tag.script(src=rng.JSCSS.progressbar_js)
                tag.script(raw(rng.JSCustom.progress_bar))

            # search highlight color control
            tag.comment("search highlight color control")
            # tag.style('span.highlight{background:  %s;}' %
            #           highlight_color)
            tag.style(
                raw(
                    """
                mark {background: %s;}
                mark.current {background: orangered;}
                """
                    % search_highlight_color
                )
            )

            if user_css:
                tag.comment("Custom CSS starts here")
                tag.style(raw(user_css))

            # Navbar on top with 2 margin to seperate from first jumbotron. add class mb-2
            with tag.nav(
                _class="navbar navbar-expand-lg navbar-dark bg-%s sticky-top"
                % rng.HelperFunctions.color_to_tag(navbar_background)
            ):
                tag.a(self.brand, _class="navbar-brand", href="#")
                # sets the report title on the navbar
                tag.span(self.report_name, _class="navbar-text text-secondary")
                # theme previewer
                if theme_preview:
                    tag.comment("Theme previewer")
                    raw(rng.CustomHTML.themes_preview)
                # Button for responsive navbar
                with tag.button(
                    _class="navbar-toggler",
                    type="button",
                    data_toggle="collapse",
                    data_target="#navbarid",
                    aria_controls="navbarColor01",
                    aria_expanded="false",
                    aria_label="Toggle navigation",
                ):
                    tag.span(_class="navbar-toggler-icon")

                # Search box and button on navbar
                # make sure to include the word context to div/p tags to make it searchable
                with tag.div(
                    _class="navbar-collapse collapse justify-content-md-end",
                    id="navbarid",
                ):
                    # ul class to house the navbar navigation items
                    with tag.ul(_class="navbar-nav"):
                        with tag.li(_class="nav-item"):
                            # add dropdown menu to house h1 tags from sections
                            with tag.div(_class="dropdown"):
                                tag.button(
                                    "sections",
                                    _class="btn btn-secondary btn-block dropdown-toggle",
                                    type="button",
                                    id="dropdownMenuButton",
                                    data_toggle="dropdown",
                                    aria_haspopup="true",
                                    aria_expanded="false",
                                )
                                with tag.ul(
                                    _class="dropdown-menu dropdown-menu-right",
                                    aria_labelledby="dropdownMenuButton",
                                    id="ddmenu",
                                    style="max-height: 300px; height: auto; overflow: scroll",
                                ):
                                    # input box for filtering dropdown
                                    tag.input(
                                        _class="form-control-sm",
                                        id="ddfilter",
                                        type="text",
                                        placeholder="Filter..",
                                    )
                        # highlight box form starts here
                        # input for search box
                        if show_search:
                            tag.input(
                                _class="form-control mr-sm-2",
                                type="search",
                                placeholder="Search",
                                data_toggle="tooltip",
                                data_placement="bottom",
                                title="Regex capable. Case sensitive.",
                            )
                            # Show search hit count
                            tag.span(
                                "0",
                                id="searchcount",
                                style="color:%s; font-size: initial; padding-right: 8; align-self: center;"
                                % search_highlight_color,
                            )
                            raw(
                                """
                                <button data-search="next" class="btn btn-sm btn-secondary">&darr;</button>
                                <button data-search="prev" class="btn btn-sm btn-secondary">&uarr;</button>
                                """
                                # <button data-search="clear" class="btn btn-sm btn-secondary">✖</button>
                            )
            if theme_preview:
                # theme preview jquery
                tag.comment("theme preview jquery")
                tag.script(raw(rng.JSCustom.themes_preview))
        self.report += str(report_head)

    def _set_title_bg(self, title):
        if title:
            return "bg"
        else:
            return "text"

    def _append_section(self, append):
        if append:
            return rng.CSSControl.sticky_section_css
        else:
            return rng.CSSControl.not_sticky_section

    def _check_valid_color(self, color):
        if color in rng.HelperFunctions.valid_tags:
            return True
        return False

    def _add_decorators(
        self, tag, title, add_reference, add_alert, add_badge, add_modal
    ):
        if add_reference:
            tag.add(rng.HelperFunctions.ref_button(add_reference))
        if add_alert:
            rng.HelperFunctions.make_alert(add_alert)
        if add_badge:
            rng.HelperFunctions.create_badges(add_badge)
        if add_modal:
            assert isinstance(add_modal, dict), "Not a dict"
            rng.HelperFunctions.make_modals(title.replace(" ", ""), add_modal)

    def section(
        self,
        title: str,
        content: str,
        raw_html_content: Union[str, None] = None,
        keep_formatting: bool = True,
        section_color: Literal[
            "primary", "red", "green", "yellow", "blue", "light"
        ] = "primary",
        title_background: bool = False,
        overflow_control: str = rng.CSSControl.css_overflow,
        text_color: Literal[
            "primary", "red", "green", "yellow", "blue", "light"
        ] = "primary",
        use_h2_title: bool = False,
        is_section: bool = False,
        add_reference: Reference = None,
        add_alert: Alert = None,
        add_badge: List[Badge] = None,
        add_modal: Modal = None,
    ):
        """A section is considered the main container used by Reportng to hold values. 
        Any string type value can be passed into a section.
        
        Args:
            title (str): Title of the section
            content (str): Content for the section
            raw_html_content (Union[str, None], optional): Raw html content to include. Defaults to None.
            keep_formatting (bool, optional): Use a pre tag for the content to keep formatting. Defaults to True.
            section_color (Literal[, optional): Color of the section title bar. Defaults to "primary".
            title_background (bool, optional): If true, background color is applied. Else, text color is changed. Defaults to False.
            overflow_control (str, optional): Uses valid CSS to control overflow of data. Defaults to rng.CSSControl.css_overflow.
            text_color (Literal[, optional): Text color of section. Defaults to "primary".
            use_h2_title (bool, optional): Use h2 as title instead of h1. If h2, it will not allow jumping from navbar. Defaults to False.
            is_section (bool, optional): Add as extra data to the previous container. Defaults to False.
            add_reference (Reference, optional): Add a reference link. Argument is a dictionary with keys color and link Defaults to None.
            add_alert (Alert, optional): Add an alert. Argument is a dictionary with keys color and message Defaults to None.
            add_badge (List[Badge], optional): Add a reference link. Argument is a list of dictionaries with keys color and message Defaults to None.
            add_modal (Modal, optional): Add a modal message box. Argument is a dictionary with keys button, title and message Defaults to None.
        
        Returns:
            Reportng: The Reportng object
        """

        color = self._set_title_bg(title_background)

        assert self._check_valid_color(section_color)

        # create a space between body jumbotrons
        tag.br()

        style = self._append_section(is_section)
        # creates the jumbotron. User dictates if it is pre or p tag
        with tag.div(
            _class="jumbotron container context reportng-report-section-class",
            style=style,
        ) as div:  # padding mods
            # can change the text color, or the background color
            if use_h2_title:
                tag.h2(title)
            else:
                tag.h1(
                    title,
                    _class="%s-%s"
                    % (color, rng.HelperFunctions.color_to_tag(section_color)),
                    id="%s" % rng.HelperFunctions.id_with_random(5, title),
                )

            # creates a reference button with link
            with tag.div(_class="container", style=overflow_control):
                if keep_formatting:
                    tag.pre(
                        content,
                        _class="text-%s" % rng.HelperFunctions.color_to_tag(text_color),
                    )
                else:
                    tag.p(
                        content,
                        _class="text-%s" % rng.HelperFunctions.color_to_tag(text_color),
                    )
            self._add_decorators(
                tag=div,
                title=title,
                add_reference=add_reference,
                add_alert=add_alert,
                add_badge=add_badge,
                add_modal=add_modal,
            )
        self.report += str(rng.HelperFunctions.convert_to_string(div))
        return self

    def section_collapsible(
        self,
        title: str,
        content: str = "",
        section_color: str = "default",
        raw_html_content: str = "",
        keep_formatting: bool = True,
        **kwargs
    ):
        """Create a collapsed section. 
        
        Args:
            title (str): Title for section
            content (str, optional): Section Content. Defaults to "".
            section_color (str, optional): Section color. Defaults to "default".
            raw_html_content (str, optional): Raw html content. Defaults to "".
            keep_formatting (bool, optional): Preserve formatting. Defaults to True.
        
        Returns:
            Reportng: The Reportng object. 
        """
        color = "bg-%s" % rng.HelperFunctions.color_to_tag(section_color)
        self.report += rng.HelperFunctions.accordian_collapse(
            color,
            title=title,
            content=content,
            pre=keep_formatting,
            raw_html=raw_html_content,
            **kwargs
        )
        return self

    def image_carousel(self, images: List[ImageCarouselType]):
        """Create an image carousel
        
        Args:
            images (List[ImageCarouselType]): List of image paths
        
        Returns:
            Reportng: The Reportng object. 
        """

        # create jumbotron container
        with tag.div(
            _class="jumbotron jumbomargin container reportng-image-carousel-class",
            style=rng.CSSControl.sticky_section_css,
        ) as carousel:
            with tag.div(
                _class="carousel slide",
                id="carousel_controls",
                data_interval="false",
                data_ride="carousel",
            ):
                # add the carousel image indicator based on the number of images
                rng.HelperFunctions.slide_indicator(len(images))
                with tag.div(_class="carousel-inner"):
                    # iterate over *image_links
                    for index_num, image in enumerate(images):
                        # get caption if any
                        has_caption = image.get("caption")
                        # so that the first image is set to active
                        if index_num == 0:
                            with tag.div(_class="carousel-item active").add(
                                tag.a(href=image.get("path"), target="_blank")
                            ):
                                tag.img(
                                    src=image.get("path"),
                                    _class="img-fluid img-thumbnail rounded mx-auto d-block",
                                )

                                if has_caption:
                                    tag.div(_class="carousel-caption").add(
                                        tag.p(has_caption)
                                    )
                        # images 2+
                        else:
                            with tag.div(_class="carousel-item").add(
                                tag.a(href=image.get("path"), target="_blank")
                            ):
                                tag.img(
                                    src=image.get("path"),
                                    _class="img-fluid img-thumbnail rounded mx-auto d-block",
                                )
                                try:
                                    if has_caption:
                                        tag.div(
                                            _class="carousel-caption reportng-image-caption-class"
                                        ).add(tag.p(has_caption))
                                except IndexError:
                                    logging.exception("All captions needs to be set")
                    # carousel button
                    with tag.a(
                        _class="carousel-control-prev",
                        href="#carousel_controls",
                        role="button",
                        data_slide="prev",
                    ):
                        tag.span(
                            _class="carousel-control-prev-icon", aria_hidden="true"
                        )
                        tag.span("Previous", _class="sr-only")
                    with tag.a(
                        _class="carousel-control-next",
                        href="#carousel_controls",
                        role="button",
                        data_slide="next",
                    ):
                        tag.span(
                            _class="carousel-control-next-icon", aria_hidden="true"
                        )
                        tag.span("Next", _class="sr-only")
        self.report += str(carousel)
        return self

    def asciinema(
        self,
        asciinema_link: str,
        title: str = "",
        is_section: bool = False,
        add_reference: Reference = None,
        add_alert: Alert = None,
        add_badge: List[Badge] = None,
        add_modal: Modal = None,
    ):
        """Add an asciinema section
        
        Args:
            asciinema_link (str): Link to asciinema
            title (str, optional): Title for asciinema. Defaults to "".
            is_section (bool, optional): Add as extra data to previous section. Defaults to False.
            add_reference (Reference, optional): Add a reference link. Argument is a dictionary with keys color and link Defaults to None.
            add_alert (Alert, optional): Add an alert. Argument is a dictionary with keys color and message Defaults to None.
            add_badge (List[Badge], optional): Add a reference link. Argument is a list of dictionaries with keys color and message Defaults to None.
            add_modal (Modal, optional): Add a modal message box. Argument is a dictionary with keys button, title and message Defaults to None.
        
        Returns:
            Reportng: The Reportng object. 
        """
        from requests import get

        logging.warning(
            "This method only works with asciinema links because of the way\n \
            browsers enforce CORS"
        )
        # checks to see if asciinema has been intialized
        assert (
            self.__asciinema
        ), "To integrate asciinema, set asciinema=True in ReportWriter"

        # hacky way to bypass the CORS problem
        try:
            url = get("%s.json" % asciinema_link).url
        except:
            logging.warning(
                "Need internet to get the proper url for %s" % asciinema_link
            )

        # controls if sticky or not
        style = self._append_section(is_section)

        with tag.div(
            _class="jumbotron jumbomargin container reportng-acsiinema-class",
            style=style,
        ) as a:
            if title != "":
                tag.h1(title, id="%s" % rng.HelperFunctions.id_with_random(5, title))

            with tag.div(_class="container", style="text-align: center;" + style):
                raw('<asciinema-player src="%s"></asciinema-player>' % url)
                tag.script(src=rng.JSCSS.asciinema_js)
                tag.a(
                    "Asciinema link",
                    _class="btn btn-secondary row justify-content-center btn-sm",
                    role="button",
                    href=asciinema_link,
                    target="_blank",
                )
        self.report += str(a)
        return self

    def code(
        self,
        title: str,
        content: str,
        is_section: bool = True,
        add_reference: Reference = None,
        add_alert: Alert = None,
        add_badge: List[Badge] = None,
        add_modal: Modal = None,
    ):
        """Add a code section with highlighting
        
        Args:
            title (str): Title of section
            content (str): Section content
            is_section (bool, optional): Add as extra data to previous section. Defaults to False.
            add_reference (Reference, optional): Add a reference link. Argument is a dictionary with keys color and link Defaults to None.
            add_alert (Alert, optional): Add an alert. Argument is a dictionary with keys color and message Defaults to None.
            add_badge (List[Badge], optional): Add a reference link. Argument is a list of dictionaries with keys color and message Defaults to None.
            add_modal (Modal, optional): Add a modal message box. Argument is a dictionary with keys button, title and message Defaults to None.
        
        Returns:
            Reportng: The Reportng object. 
        """
        assert (
            self.__highlight
        ), "To integrate code highlighting, set code=True in ReportWriter"

        style = self._append_section(is_section)

        with tag.div(
            _class="jumbotron container context reportng-code-section-class",
            style=style,
        ) as c:  # padding mods
            t = tag.h1(title, id="%s" % rng.HelperFunctions.id_with_random(5, title))
            if add_reference:
                t.add(rng.HelperFunctions.ref_button(add_reference))
            # create dismissable alert box
            if add_alert:
                rng.HelperFunctions.make_alert(add_alert)
            with tag.div(
                _class="container",
                style="max-height: 70%; overflow: auto; margin-bottom: 20",
            ):
                tag.pre().add(tag.code(content))
                if add_badge:
                    rng.HelperFunctions.create_badges(add_badge)
            if (
                add_modal
                and isinstance(add_modal, dict)
                and rng.check_keys(["button", "title", "content"], dict(add_modal))
            ):
                rng.HelperFunctions.make_modals(title.replace(" ", ""), add_modal)
        self.report += str(c)
        return self

    def captions(
        self,
        content: str,
        text_color: Literal[
            "primary", "red", "green", "yellow", "blue", "light"
        ] = "primary",
        is_section: bool = True,
        raw_html: str = None,
    ):
        """Add captions to the previous section
        
        Args:
            content (str): Caption content
            text_color (Literal[, optional): Color of caption. Defaults to "primary".
            is_section (bool, optional): Add as extra data to previous section. Defaults to True.
            raw_html (str, optional): Add raw html. Defaults to None.
        
        Returns:
            Reportng: The Reportng object. 
        """
        style = self._append_section(is_section)

        with tag.div(
            _class="container text-center reportng-captions-class", style=style
        ) as div:
            tag.p(
                content, _class="text-%s" % rng.HelperFunctions.color_to_tag(text_color)
            )
            if raw_html:
                raw(raw_html)
        self.report += str(rng.HelperFunctions.convert_to_string(div))
        return self

    def table(
        self,
        table_header: List[str],
        data: List[List[str]],
        is_section: bool = False,
        section_title: str = "",
        header_color: Literal[
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
        ] = "dark",
        show_index: bool = False,
        add_reference: Reference = None,
        add_alert: Alert = None,
        add_badge: List[Badge] = None,
        add_modal: Modal = None,
    ):
        """Add a table section
        
        Args:
            table_header (List[str]): Table header. Should be a list of strings corresponding to the number of data points. 
            data (List[List[str]]): Table data. Should be a list of list of strings. For example [[1,2,3], ['a', 'b', 'c']].
            is_section (bool, optional): Add extra data to previous section. Defaults to False.
            section_title (str, optional): Title for section. Defaults to "".
            header_color (Literal[, optional): Title header color. Defaults to "dark".
            show_index (bool, optional): Show the table index. Defaults to False.
            add_reference (Reference, optional): Add a reference link. Argument is a dictionary with keys color and link Defaults to None.
            add_alert (Alert, optional): Add an alert. Argument is a dictionary with keys color and message Defaults to None.
            add_badge (List[Badge], optional): Add a reference link. Argument is a list of dictionaries with keys color and message Defaults to None.
            add_modal (Modal, optional): Add a modal message box. Argument is a dictionary with keys button, title and message Defaults to None.
        
        Returns:
            Reportng: The Reportng object. 
        """
        if is_section:
            style = rng.CSSControl.sticky_section_css
        else:
            style = "padding-bottom:3; padding-top:40;"
        assert header_color in rng.HelperFunctions.valid_tags, rng.NotValidTag(
            "Not a valid header color"
        )
        # Check to make sure it is args
        if not isinstance(table_header, list):
            raise TypeError("Table header should be a list of columns")
        # Saves length of first arg
        header_length = len(table_header)

        # starts building the table
        with tag.div(
            _class="jumbotron container context reportng-table-class", style=style
        ) as div:  # padding mods
            if section_title:
                tag.h1(
                    section_title,
                    id="%s" % rng.HelperFunctions.id_with_random(5, section_title),
                )
            # create dismissable alert box
            with tag.div(
                _class="container",
                style="overflow-x:auto; max-height: 70%; overflow: auto;",
            ):
                with tag.table(
                    _class="table table-striped display nowrap table-hover",
                    style="width: 90%",
                ):
                    # Make table header
                    if table_header:
                        with tag.thead(
                            _class="table-%s"
                            % rng.HelperFunctions.color_to_tag(header_color)
                        ).add(tag.tr()):
                            if show_index:
                                tag.th("Index")
                            for h in range(len(table_header)):
                                tag.th(table_header[h], scope="col")
                    for row_index in range(len(data)):
                        row = (data[row_index] + [""] * header_length)[:header_length]
                        with tag.tr():
                            if show_index:
                                tag.td(str(row_index + 1))
                            for t in range(len(row)):
                                tag.td(row[t])
            self._add_decorators(
                tag=div,
                title="",
                add_reference=add_reference,
                add_alert=add_alert,
                add_badge=add_badge,
                add_modal=add_modal,
            )
        self.report += rng.HelperFunctions.convert_to_string(div)
        return self

    def cards(
        self,
        cards: List[Cards],
        is_section: bool = False,
        border_only: bool = False,
        section_title: str = None,
        add_alert: Alert = None,
        add_modal: Modal = None,
    ):
        """Add a cards section
        
        Args:
            cards (List[Cards]): List of cards. Each card is a dictionary
            is_section (bool, optional): Add as data to previous section. Defaults to False.
            border_only (bool, optional): Show cards with borders only. Defaults to False.
            section_title (str, optional): Card title. Defaults to None.
            add_alert (Alert, optional): Add an alert. Argument is a dictionary with keys color and message Defaults to None.
            add_modal (Modal, optional): Add a modal message box. Argument is a dictionary with keys button, title and message Defaults to None.
        
        Raises:
            TypeError: Cards should be a list of cards
        
        Returns:
            Reportng: The Reportng object. 
        """
        # Check to see if args is a tuple
        if not isinstance(cards, list):
            raise TypeError("Card data should be a list of cards")

        # control if stick to previous section or not
        style = self._append_section(is_section)

        with tag.div(
            _class="jumbotron container context", style=style
        ) as div:  # padding mods
            if section_title:
                tag.h1(section_title)

            with tag.div(_class="row justify-content-center"):
                for i in range(len(cards)):
                    k = cards[i].get("color") or "primary"
                    h = cards[i].get("title")
                    v = cards[i].get("message")
                    rng.HelperFunctions.make_cards(border_only, k, h, v)

            self._add_decorators(
                tag=div,
                title="",
                add_reference=None,
                add_alert=add_alert,
                add_badge=None,
                add_modal=add_modal,
            )

        self.report += str(div)
        return self

    def footer(
        self,
        message: str = "",
        twitter: str = None,
        linkedin: str = None,
        github: str = None,
        email: str = None,
        raw_html: str = None,
    ):
        """Add a footer section
        
        Args:
            message (str, optional): Footer message. Defaults to "".
            twitter (str, optional): Twitter link. Defaults to None.
            linkedin (str, optional): Linkedin link. Defaults to None.
            github (str, optional): Github link. Defaults to None.
            email (str, optional): Email address. Defaults to None.
            raw_html (str, optional): Add raw html. Defaults to None.
        
        Returns:
            Reportng: The Reportng object. 
        """
        # creates the footer
        with tag.footer(_class="page-footer reportng-footer-class") as footer:
            with tag.div(_class="container"):
                with tag.div(_class="row"):
                    with tag.div(_class="mb-4"):

                        if twitter:
                            tag.a(
                                _class="icons-sm tw-ic", href=twitter, target="_blank"
                            ).add(
                                tag.i(_class="fab fa-twitter fa-2x white-text mr-md-4")
                            )
                        elif github:
                            tag.a(
                                _class="icons-sm gh-ic", href=github, target="_blank"
                            ).add(
                                tag.i(_class="fab fa-github fa-2x white-text mr-md-4")
                            )
                        elif linkedin:
                            tag.a(
                                _class="icons-sm li-ic", href=linkedin, target="_blank"
                            ).add(
                                tag.i(_class="fab fa-linkedin fa-2x white-text mr-md-4")
                            )
                        elif email:
                            tag.a(_class="icons-sm", href=email).add(
                                tag.i(_class="fas fa-at fa-2x white-text mr-md-4")
                            )
                        # i tag for user message
                        tag.span(message, style="font-size: 125%;")
                if raw_html:
                    raw(raw_html)

        self.report += str(footer)
        return self

    def list_group(
        self,
        section_title: str,
        items: List[str],
        is_section: bool = False,
        raw_html: str = None,
        add_reference: Reference = None,
        add_modal: Modal = None,
        add_alert: Alert = None,
        add_badge: List[Badge] = None,
    ):
        """Add a list group section. A list group is a collection of strings presented as a list
        
        Args:
            section_title (str): Section title
            items (List[str]): An array of list items as strings
            is_section (bool, optional): Add as data to previous section. Defaults to False.
            raw_html (str, optional): Add raw html. Defaults to None.
            add_reference (Reference, optional): Add a reference link. Argument is a dictionary with keys color and link Defaults to None.
            add_alert (Alert, optional): Add an alert. Argument is a dictionary with keys color and message Defaults to None.
            add_badge (List[Badge], optional): Add a reference link. Argument is a list of dictionaries with keys color and message Defaults to None.
            add_modal (Modal, optional): Add a modal message box. Argument is a dictionary with keys button, title and message Defaults to None.
        
        Returns:
            Reportng: The Reportng object. 
        """
        if not section_title:
            raise rng.NotValidTag("Need a title")
        if not isinstance(items, list):
            raise rng.NotValidTag("Data have to be in the form of a list")

        style = self._append_section(is_section)

        with tag.div(
            _class="jumbotron container context reportng-list-group-class", style=style
        ) as div:
            tag.h1(
                section_title,
                id="%s" % rng.HelperFunctions.id_with_random(5, section_title),
            )

            with tag.ul(_class="list-group"):
                for i in range(len(items)):
                    tag.li(
                        items[i],
                        _class="list-group-item d-flex justify-content-between align-items-center text-primary",
                    )

            if raw_html:
                raw(raw_html)

            self._add_decorators(
                tag=div,
                title=section_title,
                add_reference=add_reference,
                add_alert=add_alert,
                add_badge=add_badge,
                add_modal=add_modal,
            )

        self.report += rng.HelperFunctions.convert_to_string(div)
        return self

    def custom_html(self, html: str):
        """Add a custom section with raw html inside a jumbotron
        
        Args:
            html (str): Raw html
        
        Returns:
            Reportng: The Reportng object. 
        """
        with tag.div(
            _class="jumbotron container context reportng-custom-html-class",
            style="padding:0",
        ) as c:
            raw(html)
        self.report += rng.HelperFunctions.convert_to_string(c)
        return self

    def save(self, path: str) -> None:
        """Save the report
        
        Args:
            path (str): Path to save the report. 
        """
        with open(str(Path(path).resolve()), "w+", encoding="utf-8") as save:
            save.write(str(self.report))


class Assets:
    """
    Assets allows one to either download and map all dependent CSS and JS files, or
    use existing CSS and JS files
    """

    @staticmethod
    def local(rel_path: str):
        """
        This method allows one to map locally available asset files automatically.
        Themes are dicated by the locally available file

        :param str rel_path: The relative path from the report file. Usally is ./assets/

        Example:
            >>> from reportng import ReportWriter, Assets
            >>> Assets.local(rel_path='/tmp/assets/')
            >>> r = ReportWriter('Title', 'securisec')
        """
        change = vars(rng.JSCSS)
        for k, v in change.items():
            if not "__" in k:
                local_file = v.split("/")[-1]
                setattr(rng.JSCSS, k, rel_path + local_file)

    @staticmethod
    def download(download_path: str, rel_path: str, theme: str = "lux"):
        """
        This method is used to download all online assests like JS/CSS locally. This method
        also will change all the src and href links to the local files

        :param str download_path: Path to save the files in
        :param str rel_path: Relative path from where the html will be saved
        :param str theme: The name of the bootswatch theme. Defaults to Lux

        Example:
            >>> from reportng import ReportWriter, Assets
            >>> Assets.download(save_path='/tmp/assets/', rel_path='./assets/')
            >>> r = ReportWriter('Title', 'securisec')
        """

        from requests import get

        logging.warning(
            "Some files like font-awesome (all.css) does not work unless put into specific folders"
        )
        # Check to make sure path is a dir
        if not Path(download_path).is_dir():
            Path(download_path).mkdir()

        change = vars(rng.JSCSS)
        for k, v in change.items():
            if not "__" in k:
                local_file = v.split("/")[-1]
                if not Path(download_path + local_file).exists():
                    with open(download_path + local_file, "w+", encoding="utf8") as f:
                        if "https://bootswatch.com/4/" in v:
                            v = v.replace("lux", theme)
                            local_file = v.split("/")[-1]
                        headers = {
                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
                        }
                        f.write(get(v, headers=headers).text)
                        logging.info("Downloaded %s to %s" % (v, download_path))
                        setattr(rng.JSCSS, k, rel_path + local_file)
