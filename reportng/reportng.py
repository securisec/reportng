# -*- coding: utf-8 -*-
"""
Python report generator that wraps around bootstrap 4 using dominate. 
Usage is simple. Follows header, body..., footer structure
"""
import os
import dominate
import dominate.tags as tag
from dominate.util import raw

# ugly way to address unicode encode issues
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'securisec'


class NotValidTag(Exception):
    pass


class ReportWriter:
    """
    The main class that is used. Modifiable parameters are report_name,
    theme, brand and highlight_color
    """

    def __init__(self, report_name, brand):
        """
        Assign theme and report name
        :brand str: Name of the company/tester
        :report_name str: Name of report. Default is Sample report
        """
        self.report_name = report_name
        self.brand = brand
        self.document = dominate.document(title=self.report_name)

    def convert_to_string(self, s):
        return '%s' % s

    def report_header(self, theme='lux',
                      highlight_color='#f1c40f'):
        """
        Controls the link and script tags in the head. This method should always be called
        at the top
        :theme str: Name of any bootswatch theme. Default is litera
        :highlight_color str: any rgb color. default is #f1c40f 
        :return: The head tag for the report.
        """
        with self.document.head as report_head:
            # link and script builder for bootstrap 4
            tag.comment('Created using easyreport by securisec')
            tag.meta(charset="utf-8", name="viewport",
                     content="width=device-width, initial-scale=1")
            tag.script(
                src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js")
            tag.script(
                src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js")
            tag.script(
                src="https://cdn.rawgit.com/securisec/misc_things/f8d2b846/highlight.js")
            # JS for search highlighting
            tag.script(raw(
                """
                function clickHighlight() {
                    document.getElementById("performbutton").click();
                }
                """
            ))
            # JS to populate the navbar dropdown
            tag.script(raw(
                """
                function populateDropdown() {
                    var headings = $('h1')
                    var select = document.getElementById("ddmenu");
                    for (var i = 0; i < headings.length; i++){
                        var a = document.createElement("a")
                        a.setAttribute("class", "dropdown-item " + headings[i].className);
                        a.setAttribute("href", "#" + headings[i].id)
                        a.innerHTML = headings[i].innerHTML;
                        select.appendChild(a);
                    }
                }
                window.onload = populateDropdown
                """
            ))
            # script that allows for smooth scrolling and adds padding for navbar
            tag.script(raw(
                """
                $(document).on('click', 'a[href^="#"]', function (event) {
                    event.preventDefault();
                    $('html, body').animate({
                        scrollTop: $($.attr(this, 'href')).offset().top-150
                    }, 500);
                });
                """
            ))
            # js to filter in the dropdown menu
            tag.script(raw(
                """
                $(document).ready(function(){
                $("#ddfilter").on("keyup", function() {
                    var value = $(this).val().toLowerCase();
                    $(".dropdown-menu a").filter(function() {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                    });
                });
                });
                """
            ))
            # style sheets
            tag.link(rel="stylesheet", type="text/css",
                     href="https://bootswatch.com/4/%s/bootstrap.min.css" % theme)
            tag.link(href="https://use.fontawesome.com/releases/v5.0.6/css/all.css",
                     rel="stylesheet")

            # search highlight color control
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
                                    tag.input(_class="form-control", id="ddfilter",
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

    def report_section(self, title, content, pre_tag=True, tag_color='default'):
        """
        This form the main body of the report
        :title string: The h1/header title of the section
        :pre_tag bool: Default is True and treats content as monospaced. Set to False to use p tag
        :content string: The content for this section
        :tag_color str: The severity color of the section.
        :return: a jumbotron object
        """
        if tag_color not in ['primary', 'secondary', 'success',
                             'danger', 'warning', 'info', 'default']:
            raise NotValidTag, 'Valid tags are primary secondary success danger warning info'

        # create a space between body jumbotrons
        tag.br()
        # creates the jumbotron. User dictates if it is pre or p tag
        with tag.div(_class="jumbotron container context",
                     style="padding-bottom:3; padding-top:40") as r:  # padding mods
            tag.h1(title, _class="bg-%s" %
                                 tag_color, id="%s" % title.replace(' ', ''))
            if pre_tag:
                tag.pre(content)
            else:
                tag.p(content)
        return str(self.convert_to_string(r))

    def report_add_image_carousel(self, *args):
        """
        :*image_links list: A list of image paths
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

    def report_notes(self, content):
        """
        Simple method to added some center aligned text.
        :content str: content to add
        """
        with tag.div(_class="container text-center", style="margin-top:-30;") as s:
            tag.p(content)
        return str(self.convert_to_string(s))

    def report_footer(self, message='', **kwargs):
        """
        Returns the footer object. Supports social media
        :message: A message in the footer
        :kwargs: Supported paramters are email, linkedin, github and twitter 
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

    def save_report(self, all_objects, path):
        """
        Saves the html file to disk
        :all_objects: The tally of all the objects
        :path: path to save the file
        """
        with open(os.path.expanduser(path), 'w+') as save:
            save.write(str(all_objects))

# TODO: add a brand image that is resized with the navbar
# TODO: option to add captions to images
# TODO: keep the image jumbotron static no matter the size of the picture
# TODO: something that will allow user to loop and add content
# TODO: integrate components of mark.js
# TODO: make header method mandatory
