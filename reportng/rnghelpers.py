"""
Helper module for reportng
"""
import dominate.tags as tag


class JSCSS:
    """
    This class controls constants that can be modified by the user and can be pointed to local files to host them locally
    """

    #: bootswatch theme
    bootswatch = "https://bootswatch.com/4/lux/bootstrap.min.css"
    #: jquery: Constant that handles jqery.min.js
    jquery = "https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"
    #: bs4_js: Constant that handles bootstrap.min.js
    bs4_js = "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
    #: highlight_custom: Constant that handles the custom js that aids in highlighting
    highlight_custom = "https://cdn.rawgit.com/securisec/misc_things/f8d2b846/highlight.js"
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
                        a.innerHTML = headings[i].innerHTML;
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


class HelperFunctions:
    """
    Some helper functions that does not impact how enduser uses reportng
    """

    #: Valid options for colors/cards etc
    valid_tags = ['primary', 'secondary', 'success', 'danger',
                  'warning', 'info', 'light', 'dark', 'default']

    @staticmethod
    def convert_to_string(s):
        return '%s' % s

    @staticmethod
    # Function that creates to ol tags and populates with il tags for
    # carousel count indicator
    def slide_indicator(num):
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
        if k not in HelperFunctions.valid_tags:
            raise NotValidTag, '\n\n%s is not a valid tag. \nChoose one of the following: \n%s' % (
                k, '\n'.join([x for x in HelperFunctions.valid_tags]))
        # checks bool and determines styling
        if b_only:
            style = 'border'
            text = 'text-primary'
        else:
            style = 'bg'
            text = 'text-white'
        with tag.div(_class="card %s %s-%s m-3" % (text, style, k), style="width: 20rem;") as m:
            tag.div(h, _class='card-header')
            with tag.div(_class="card-body"):
                tag.p(v, _class="card-text")
        return m
