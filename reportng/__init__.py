# -*- coding: utf-8 -*-
"""
Python report generator that wraps around bootstrap 4 using dominate.
Usage is simple. Follows header, body..., footer structure
"""
import os
import logging
import urllib2
import rnghelpers as rng

try:
    import dominate
    import dominate.tags as tag
    from dominate.util import raw
except ImportError:
    print 'pip install dominate'

# ugly way to address unicode encode issues
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'securisec'
__version__ = '0.25'


class ReportWriter:
    """
    The main class that is used. Modifiable parameters are report_name,
    theme, brand and highlight_color
    """

    def __init__(self, report_name, brand, asciinema=False, code_highlight=False):
        """
        Assign theme and report name

        :param str brand: Name of the company/tester
        :param str report_name: Name of report. Default is Sample report
        :param bool asciinema: Set to true to use asciinema's in report. Default is False
        :param bool code_highlight: Set to True in order to use code highlighting
        """
        self.report_name = report_name
        self.brand = brand
        self.document = dominate.document(title=self.report_name)
        self.asciinema = asciinema
        self.code_highlight = code_highlight

    def convert_to_string(self, s):
        return '%s' % s

    def report_header(self, theme='lux', highlight_color='#f1c40f'):
        """
        Controls the link and script tags in the head. This method should always be called
        at the top

        :param str theme: Name of any bootswatch theme. Default is lux
        :param str highlight_color: any rgb color. default is #f1c40f
        :return: The head tag for the report.
        """

        with self.document.head as report_head:
            # link and script builder for bootstrap 4
            tag.comment('Created using reportng by securisec')
            tag.meta(charset="utf-8", name="viewport",
                     content="width=device-width, initial-scale=1")
            # main style components
            tag.script(src=rng.JSCSS.jquery)
            tag.script(src=rng.JSCSS.bs4_js)
            tag.script(src=rng.JSCSS.highlight_custom)

            # JS for search highlighting
            tag.comment('JS to highlight onkeyup')
            tag.script(raw(
                rng.JSCustom.highlight_js
            ))

            # JS to populate the navbar dropdown
            tag.comment('JS to populate the navbar dropdown')
            tag.script(raw(
                rng.JSCustom.populate_navbar_onload
            ))

            # script that allows for smooth scrolling and adds padding for navbar
            tag.comment(
                'script that allows for smooth scrolling and adds padding for navbar')
            tag.script(raw(
                rng.JSCustom.smoothscroll_navbar_pad
            ))

            # js to filter in the dropdown menu
            tag.comment('js to filter in the dropdown menu')
            tag.script(raw(
                rng.JSCustom.dropdown_filter
            ))

            # bootswatch style sheets
            tag.comment('style sheets')
            tag.link(rel="stylesheet", type="text/css",
                     href="https://bootswatch.com/4/%s/bootstrap.min.css" % theme)
            tag.link(href=rng.JSCSS.font_awesome, rel="stylesheet")

            # constructing this way to avoid loading un needed js and css
            # css for asciinema
            if self.asciinema:
                tag.comment('css for asciinema')
                tag.link(rel="stylesheet", type="text/css",
                         href=rng.JSCSS.asciinema_css)

            # css and js for highlight.js
            if self.code_highlight:
                tag.comment('css and js for highlight.js')
                tag.link(rel="stylesheet", href=rng.JSCSS.highlightjs_css)
                tag.script(src=rng.JSCSS.highlightjs_js)
                tag.script(raw(
                    """
                    hljs.initHighlightingOnLoad();
                    """
                ))

            # search highlight color control
            tag.comment('search highlight color control')
            tag.style('span.highlight{background:  %s;}' %
                      highlight_color)

            # Navbar on top with 2 margin to seperate from first jumbotron. add class mb-2
            with tag.nav(_class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top"):
                tag.a(self.brand, _class="navbar-brand", href="#")

                # Button for responsive navbar
                with tag.button(_class="navbar-toggler",
                                type="button", data_toggle="collapse", data_target="#navbarid",
                                aria_controls="navbarColor01", aria_expanded="false", aria_label="Toggle navigation"):
                    tag.span(_class="navbar-toggler-icon")

                # Search box and button on navbar
                # https://codepen.io/SitePoint/pen/oxOrxM
                # make sure to include the word context to div/p tags to make it searchable
                with tag.div(_class="navbar-collapse collapse justify-content-md-end", id="navbarid"):
                    # ul class to house the navbar navigation items
                    with tag.ul(_class="navbar-nav"):
                        with tag.li(_class="nav-item"):
                            # add dropdown menu to house h1 tags from sections
                            with tag.div(_class="dropdown"):
                                tag.button('sections', _class="btn btn-secondary btn-block dropdown-toggle",
                                           type="button", id="dropdownMenuButton", data_toggle="dropdown",
                                           aria_haspopup="true", aria_expanded="false")
                                with tag.ul(_class="dropdown-menu",
                                            aria_labelledby="dropdownMenuButton", id="ddmenu"):
                                    # input box for filtering dropdown
                                    tag.input(_class="form-control-sm", id="ddfilter",
                                              type="text", placeholder="Filter..")
                        # highlight box form starts here
                        with tag.li(_class="nav-item"):
                            with tag.form(_class="form-inline my-2 my-lg-0", id="form", autocomplete="off"):
                                tag.input(_class="form-control mr-sm-2", type="text", placeholder="Highlight",
                                          name="keyword", id="keyword", onkeyup="clickHighlight()")
                                # Button is hidden
                                tag.button("Highlight", _class="btn btn-secondary my-2 my-sm-0", type="button",
                                           style="display: none;", name="perform", id="performbutton")

        return str(report_head)

    def report_section(self, title, content, pre_tag=True, tag_color='default',
                       title_bg=True):
        """
        This form the main body of the report

        :param str title: The h1/header title of the section
        :param bool pre_tag: Default is True and treats content as monospaced. Set to False to use p tag
        :param str content: The content for this section
        :param str tag_color: The severity color of the section.
        :param bool title_bg: Controls if the header background or text is colored. Default is True and lets background color.
        :return: a jumbotron object
        """
        if title_bg:
            color = 'bg'
        else:
            color = 'text'
        if tag_color not in ['primary', 'secondary', 'success',
                             'danger', 'warning', 'info', 'default']:
            raise rng.NotValidTag, 'Valid tags are primary secondary success danger warning info'

        # create a space between body jumbotrons
        tag.br()
        # creates the jumbotron. User dictates if it is pre or p tag
        with tag.div(_class="jumbotron container context",
                     style="padding-bottom:3; padding-top:40") as r:  # padding mods
            # can change the text color, or the background color
            tag.h1(title, _class="%s-%s" %
                                 (color, tag_color), id="%s" % title.replace(' ', ''))
            if pre_tag:
                tag.pre(content)
            else:
                tag.p(content)
        return str(self.convert_to_string(r))

    def report_add_image_carousel(self, *args):
        """
        :param list args: A list of image paths
        :return: image jumbotron carousel container
        """

        # Function that creates to ol tags and populates with il tags for
        # carousel count indicator
        def carousel_slide_indicator(num):
            with tag.ol(_class="carousel-indicators") as o:
                for cnt in range(num):
                    if cnt == 0:
                        tag.li(data_target="#carousel_controls",
                               data_slide_to="0", _class="active")
                    else:
                        tag.li(data_target="#carousel_controls",
                               data_slide_to="%s" % str(cnt))
            return o

        # create jumbotron container
        with tag.div(_class="jumbotron jumbomargin container",
                     style="padding:0; margin-top:-2rem;") as i:
            with tag.div(_class="carousel slide", id="carousel_controls", data_interval="false",
                         data_ride="carousel"):
                # add the carousel image indicator based on the number of images
                carousel_slide_indicator(len(args))
                with tag.div(_class="carousel-inner"):
                    # iterate over *image_links
                    for index_num, image in enumerate(args):
                        # so that the first image is set to active
                        if index_num == 0:
                            with tag.div(_class="carousel-item active").add(
                                    tag.a(href=image, target="_blank")):
                                tag.img(
                                    src=image, _class="img-fluid img-thumbnail rounded mx-auto d-block")
                        # images 2+
                        else:
                            with tag.div(_class="carousel-item").add(
                                    tag.a(href=image, target="_blank")):
                                tag.img(
                                    src=image, _class="img-fluid img-thumbnail rounded mx-auto d-block")
                    # carousel button
                    with tag.a(_class="carousel-control-prev", href="#carousel_controls",
                               role="button", data_slide="prev"):
                        tag.span(_class="carousel-control-prev-icon",
                                 aria_hidden="true")
                        tag.span("Previous", _class="sr-only")
                    with tag.a(_class="carousel-control-next", href="#carousel_controls",
                               role="button", data_slide="next"):
                        tag.span(_class="carousel-control-next-icon",
                                 aria_hidden="true")
                        tag.span("Next", _class="sr-only")
        return str(i)

    def report_asciinema(self, asciinema_link, title=''):
        """
        Section creates a jumbotron to house an asciinema

        :param str asciinema_link: Link to asciinema. Could be http/s or local files
        :param str title: Set the title of the asciinema. If set, it will create its own section.
        """
        logging.warning('This method only works with asciinema links because of the way\n \
            browsers enforce CORS')
        # checks to see if asciinema has been intialized
        if not self.asciinema:
            raise rng.ObjectNotInitiated, 'To integrate asciinema, set asciinema=True in ReportWriter'

        # TODO: write a check here that validates the asciinema url

        # hacky way to bypass the CORS problem
        try:
            url = urllib2.urlopen('%s.json' % asciinema_link).geturl()
        except urllib2.URLError:
            logging.warning(
                'Need internet to get the proper url for %s' % asciinema_link)

        # adjusts section padding if h1 is to be set or not
        if title != '':
            style = "padding-bottom:3; padding-top:40"
        else:
            style = "padding:0; margin-top:-2rem;"

        with tag.div(_class="jumbotron jumbomargin container",
                     style=style) as a:
            if title != '':
                tag.h1(title, id="%s" % title.replace(' ', ''))
            raw('<asciinema-player src="%s"></asciinema-player>' % url)
            tag.script(
                src=rng.JSCSS.asciinema_js)
        return str(a)

    def report_code_section(self, title, code):
        """
        This section can use used to add code containers that will be lexed and highlighted using highlight.js

        :param str title: Title of the code section.
        :param str code: Code. Use pre and code tags so multiline code is fine
        :return: a string code section
        """
        if not self.code_highlight:
            raise rng.ObjectNotInitiated, 'To integrate code highlighting, set code_highlight=True in ReportWriter'
        with tag.div(_class="jumbotron container context",
                     style="padding-bottom:3; padding-top:40;") as c:  # padding mods
            tag.h1(title, id="%s" % title.replace(' ', ''))
            with tag.div(_class="container", style=" max-height: 70%; overflow: auto; margin-bottom: 20"):
                tag.pre().add(tag.code(code))
        return str(c)

    def report_notes(self, content):
        """
        Simple method to added some center aligned text.

        :param str content: content to add
        """
        with tag.div(_class="container text-center", style="margin-top:-30;") as s:
            tag.p(content)
        return str(self.convert_to_string(s))

    def report_footer(self, message='', **kwargs):
        """
        Returns the footer object. Supports social media

        :param str message: A message in the footer
        :param dict kwargs: Supported paramters are email, linkedin, github and twitter
        """
        # creates the footer
        with tag.footer(_class="page-footer") as footer:
            with tag.div(_class="container"):
                with tag.div(_class="row"):
                    with tag.div(_class="mb-4"):
                        # Looks through valid kwargs and creates appropiate a tag
                        for key, value in sorted(kwargs.iteritems()):
                            if key == 'twitter':
                                tag.a(_class="icons-sm tw-ic", href=value, target="_blank").add(
                                    tag.i(_class="fab fa-twitter fa-2x white-text mr-md-4"))
                            elif key == 'github':
                                tag.a(_class="icons-sm gh-ic", href=value, target="_blank").add(
                                    tag.i(_class="fab fa-github fa-2x white-text mr-md-4"))
                            elif key == 'linkedin':
                                tag.a(_class="icons-sm li-ic", href=value, target="_blank").add(
                                    tag.i(_class="fab fa-linkedin fa-2x white-text mr-md-4"))
                            elif key == 'email':
                                tag.a(_class="icons-sm", href=value).add(
                                    tag.i(_class="fas fa-at fa-2x white-text mr-md-4"))
                        # i tag for user message
                        tag.span(message, style="font-size: 125%;")

        return str(footer)

    def report_save(self, all_objects, path):
        """
        Saves the html file to disk

        :param str all_objects: The tally of all the objects
        :param str path: path to save the file
        """
        with open(os.path.expanduser(path), 'w+') as save:
            save.write(str(all_objects))

# TODO: add a brand image that is resized with the navbar
# TODO: option to add captions to images
# TODO: keep the image jumbotron static no matter the size of the picture
# TODO: something that will allow user to loop and add content
# TODO: integrate components of mark.js. Somehow to filter inside a section
# TODO: make header method mandatory