"""
Helper module for reportng
"""
import dominate.tags as tag
from dominate.util import raw
import logging


class JSCSS:
    """
    This class controls constants that can be modified by the user and can be
    pointed to local files to host them locally. Can be used with
    ``DownloadAssets(download_path, rel_path)`` class to save all files locally and point them
    correctly
    """

    #: bootswatch theme
    bootswatch = "https://bootswatch.com/4/lux/bootstrap.min.css"
    #: jquery: Constant that handles jqery.min.js
    jquery = "https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"
    #: bs4_js: Constant that handles bootstrap.min.js
    bs4_js = "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
    # highlight_custom: Constant that handles the custom js that aids in highlighting
    # comment highlight_custom = "https://cdn.rawgit.com/securisec/reportng/master/js/highlight.js"
    #: font_awesome: Constant that handles font awesomes all.min.js
    font_awesome = "https://use.fontawesome.com/releases/v5.0.6/css/all.css"
    #: asciinema_css: Constant that handles asciinema-player.min.js
    asciinema_css = "https://cdnjs.cloudflare.com/ajax/libs/asciinema-player/2.4.1/asciinema-player.min.css"
    #: asciinema_js: Constant that handles asciinema-player.min.js
    asciinema_js = "https://cdnjs.cloudflare.com/ajax/libs/asciinema-player/2.4.1/asciinema-player.min.js"
    #: highlighjs_css: Constant that handles highlight.js default.min.js
    highlightjs_css = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/default.min.css"
    #: highlight_js: Constant that handles highlight.min.js
    highlightjs_js = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"
    #: progressbar: Constant that handles progressbar.js
    progressbar_js = "https://cdn.rawgit.com/securisec/reportng/master/js/progressbar.js"
    #: mark_js: Constant that handles mark.js
    mark_js = "https://cdnjs.cloudflare.com/ajax/libs/mark.js/8.11.1/jquery.mark.min.js"


class CSSControl:
    """
    CSS control
    """

    #: css_overflow: This value can be modified globally so that all containers are the same size similar to the output report_code_section. Can be modified directly, or using overflow option in report_section
    css_overflow = "max-height: 70%; overflow: auto; margin-bottom: 20"
    #: jumbotron_style: Style attribute values of jumbotron
    jumbotron_style = "padding-bottom:3; padding-top:40"
    #: sticky_section_css: Controls if section should sticky with preceeding section
    sticky_section_css = "padding:0; margin-top:-2rem;"
    #: not_stick_section: Controls if the section is not a sticky
    not_sticky_section = "padding-bottom:3; padding-top:40;"


class JSCustom:
    """
    Class that handles all the custom JS code. It is best not to modify any of this code.
    """

    highlight_js = """
                function clickHighlight() {
                    document.getElementById("performbutton").click();
                }
                """

    populate_navbar_onload = """
                function populateDropdown() {
                    var headings = $('h1')
                    var select = document.getElementById("ddmenu");
                    for (var i = 0; i < headings.length; i++){
                        var a = document.createElement("a")
                        a.setAttribute("class", "dropdown-item " + headings[i].className);
                        a.setAttribute("href", "#" + headings[i].id)
                        a.innerHTML = headings[i].innerText;
                        select.appendChild(a);
                    }
                }
                window.onload = populateDropdown
                """

    smoothscroll_navbar_pad = """
                $(document).on('click', 'a[href^="#"]', function (event) {
                    event.preventDefault();
                    $('html, body').animate({
                        scrollTop: $($.attr(this, 'href')).offset().top-150
                    }, 500);
                });
                """

    dropdown_filter = """
                $(document).ready(function(){
                $("#ddfilter").on("keyup", function() {
                    var value = $(this).val().toLowerCase();
                    $(".dropdown-menu a").filter(function() {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                    });
                });
                });
                """

    progress_bar = """
                $(function() {
                $("body").prognroll({
                    height: 7
                });
                });
                """

    markjs_script = """
                    $(function () {
                        var $input = $("input[type='search']"),
                            $clearBtn = $("button[data-search='clear']"),
                            $prevBtn = $("button[data-search='prev']"),
                            $nextBtn = $("button[data-search='next']"),
                            $content = $(".context"),
                            $results,
                            currentClass = "current",
                            offsetTop = 150,
                            currentIndex = 0;
                        function jumpTo() {
                            if ($results.length) {
                                var position,
                                    $current = $results.eq(currentIndex);
                                $results.removeClass(currentClass);
                                if ($current.length) {
                                    $current.addClass(currentClass);
                                    position = $current.offset().top - offsetTop;
                                    window.scrollTo(0, position);
                                }
                            }
                        }
                        $input.on("input", function () {
                            var searchVal = this.value;
                            $content.unmark({
                                done: function () {
                                    $content.markRegExp(RegExp(searchVal), {
                                        separateWordSearch: false,
                                        done: function () {
                                            $results = $content.find("mark");
                                            currentIndex = 0;
                                            var c = document.getElementById('searchcount');
                                            c.innerHTML = $results.length;
                                            jumpTo();
                                        }
                                    });
                                }
                            });
                        });
                        $clearBtn.on("click", function () {
                            $content.unmark();
                            $input.val("").focus();
                        });
                        $nextBtn.add($prevBtn).on("click", function () {
                            if ($results.length) {
                                currentIndex += $(this).is($prevBtn) ? -1 : 1;
                                if (currentIndex < 0) {
                                    currentIndex = $results.length - 1;
                                }
                                if (currentIndex > $results.length - 1) {
                                    currentIndex = 0;
                                }
                                jumpTo();
                            }
                        });
                    });
                    """


class NotValidTag(Exception):
    """
    Exception to handle invalid tag for background color control
    """
    pass


class ObjectNotInitiated(Exception):
    """
    Exception when a method is called but not initiated
    """
    pass


class TooManyValues(Exception):
    """
    Exception when too many args are passed
    """
    pass


class TableError(Exception):
    """
    Exception when there are problems with creating a table
    """
    pass


class HelperFunctions:
    """
    Some helper functions that does not impact how enduser uses reportng
    """

    #: Valid options for colors/cards etc
    valid_tags = ['primary', 'secondary', 'success', 'danger',
                  'warning', 'info', 'light', 'dark', 'default',
                  'red', 'green', 'blue', 'yellow', 'light']

    @staticmethod
    def color_to_tag(s):
        """
        Maps colors to their appropriate tags
        """
        if s == 'red':
            s = 'danger'
        elif s == 'green':
            s = 'success'
        elif s == 'yellow':
            s = 'warning'
        elif s == 'blue':
            s = 'info'
        elif s == 'light':
            s = 'secondary'
        else:
            s = s
        return s

    @staticmethod
    def convert_to_string(s):
        """
        Converts an object to string
        """
        return '%s' % s

    @staticmethod
    # Function that creates to ol tags and populates with il tags for
    # carousel count indicator
    def slide_indicator(num):
        """
        Helper function that controls how image slide count works
        """
        with tag.ol(_class="carousel-indicators") as o:
            for cnt in range(num):
                if cnt == 0:
                    tag.li(data_target="#carousel_controls",
                           data_slide_to="0", _class="active")
                else:
                    tag.li(data_target="#carousel_controls",
                           data_slide_to="%s" % str(cnt))
        return o

    @staticmethod
    # Function to create the cards
    def make_cards(b_only, k, h, v):
        """
        Helper function that helps making cards
        """
        if k not in HelperFunctions.valid_tags:
            raise NotValidTag('\n\n%s is not a valid tag. \nChoose one of the following: \n%s' % (
                k, '\n'.join([x for x in HelperFunctions.valid_tags])))
        # checks bool and determines styling
        if b_only:
            style = 'border'
            text = 'text-primary'
        else:
            style = 'bg'
            text = 'text-white'
        with tag.div(_class="card %s %s-%s m-3" % (text, style, HelperFunctions.color_to_tag(k)),
                     style="width: 20rem;") as m:
            tag.div(h, _class='card-header')
            with tag.div(_class="card-body"):
                tag.p(v, _class="card-text")
        return m

    @staticmethod
    # Function to create alerts in sections
    def make_alert(*args):
        """
        Helper function that creates dismissable alerts
        """
        if len(args[0]) == 2 and isinstance(args, tuple):
            color = args[0][0]
            message = args[0][1]
            with tag.div(message, _class="alert alert-dismissible alert-%s" % HelperFunctions.color_to_tag(color)) as a:
                raw('<button type="button" class="close" data-dismiss="alert">&times;</button>')
        else:
            raise NotValidTag('Use two values in the tuple')
        return a

    @staticmethod
    def ref_button(*args):
        """
        Places a button with href on it.
        """
        if len(args[0]) == 2 and isinstance(args, tuple):
            color = args[0][0]
            link = args[0][1]
            b = tag.a("Reference", _class="btn btn-outline-%s btn-sm float-right" % HelperFunctions.color_to_tag(color),
                      href=link, role="button", target='_blank')
            return b
        else:
            raise NotValidTag('Use two values in the tuple')

    @staticmethod
    def create_badges(b):
        """
        Creates badges at the bottom of a section
        """
        total = ''
        if not isinstance(b, dict):
            raise NotValidTag('Use a dictionary to pass badge values')
        for k, v in b.items():
            if k not in HelperFunctions.valid_tags:
                raise NotValidTag('Choose a valid tag color from\n%s' % ' '.join(HelperFunctions.valid_tags))
            if len(v) > 14:
                logging.warning('Do you really want a badge that long?')
            total += str(tag.span(v, _class="badge badge-%s float-right" % HelperFunctions.color_to_tag(k)))
        return total
