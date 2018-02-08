"""
Helper module for reportng
"""


class JSCSS:
    """
    This class controls constants that can be modified by the user and can be pointed to local files to host them locally
    """

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
