import urwid
from urwid.util import decompose_tagmarkup


class BasicWidget(urwid.WidgetWrap):
    """ Basic widget for GViewer

    Define the basic attr and basic behavior how GViewer widget to display or act

    Attributes:
        controller: a Controller instance
        context: a Context instance
        widget: a urwid Widget
        attr_map: non-focus attribute
        focus_map: focus attribute
    """
    def __init__(self, controller=None, context=None, widget=None,
                 attr_map=None, focus_map=None):
        widget = widget or urwid.Text("")
        if attr_map:
            widget = urwid.AttrMap(widget, attr_map, focus_map=focus_map)
        super(BasicWidget, self).__init__(widget)
        self.controller = controller
        self.context = context

    def display(self, widget):
        """ Display the widget

        Args:
            widget: urwid Widget
        """
        if isinstance(self._w, urwid.AttrMap):
            self._w.original_widget = widget
        else:
            self._w = widget

    def keypress(self, size, key):
        """ Define default keypress action for GViewer """
        if self.controller:
            self.controller._run_before_keypress()

        if (not self.is_editing() and self.context and
                key in self.context.config.keys):
            return super(BasicWidget, self).keypress(size, self.context.config.keys[key])
        try:
            return super(BasicWidget, self).keypress(size, key)
        except AttributeError:  # pragma: no cover
            return key

    def is_editing(self):
        """ Check that current state is editing or not

        Override this method if that widget had Edit widget in its content
        and return True if the focus widget is the Edit widget

        Returns:
            True if in editing, False if not in editing
        """
        return False


class FocusableText(BasicWidget):
    """ Text widget that will highlight correctly

    Attributes:
        text_markup: urwid Text Markup instance
    """
    def __init__(self, text_markup, **kwargs):
        widget = urwid.Text(text_markup)
        super(FocusableText, self).__init__(
            widget=widget, **kwargs)
        self.text_markup = text_markup

    def render(self, size, focus=False):
        """ Override original render function

        Display the widget in different way depend on that the widget is focus or not
        """
        if focus:
            plain_text = self.get_plain_text()
            self.display(urwid.Text(plain_text))
        else:
            self.display(urwid.Text(self.text_markup))
        return super(FocusableText, self).render(size, focus)

    def get_plain_text(self):
        """ Retrieve the plain text from text_markup """
        if isinstance(self.text_markup, str) or \
           isinstance(self.text_markup, unicode):
            return self.text_markup
        text, _ = decompose_tagmarkup(self.text_markup)
        return text

    def selectable(self):
        return True


class SearchWidget(BasicWidget):
    """ Edit widget to handle searching

    Attributes:
        search_func: a callback function that will be called when search is invoke
        clear_func: a callback function that will be called when search is cancelled
    """
    def __init__(self, search_func, clear_func, **kwargs):
        super(SearchWidget, self).__init__(
            widget=urwid.Edit("/"), **kwargs)
        self.search_func = search_func
        self.clear_func = clear_func

    def clear(self):
        self.display(urwid.Edit("/"))

    def get_keyword(self):
        return self._w.edit_text

    def keypress(self, size, key):
        if key == "enter":
            self.search_func(self._w.edit_text)
            return None
        if key == "esc":
            self.clear()
            self.clear_func()
            return None
        return super(SearchWidget, self).keypress(size, key)


class SearchableText(BasicWidget):
    """ Searchable text let its content could be search and hightlight

    Attributes:
        plain_text: str or unicode
    """
    def __init__(self, plain_text, **kwargs):
        self.plain_text = plain_text or u""
        if isinstance(plain_text, str):
            plain_text = plain_text.decode("utf8")

        widget = urwid.Text(plain_text)
        super(SearchableText, self).__init__(
            widget=widget, **kwargs)

        self.plain_text = plain_text
        self.prev_index = (0, len(plain_text))

    def search_next(self, keyword):
        prev_index = self.prev_index[0]
        if isinstance(keyword, str):
            keyword = keyword.decode("utf8")
        if keyword in self.plain_text[prev_index:]:
            start_index = self.plain_text[prev_index:].index(keyword) + prev_index
            end_index = start_index + len(keyword)
            self.display(urwid.Text([
                self.plain_text[:start_index],
                ("match", keyword),
                self.plain_text[end_index:]
            ]))

            self.prev_index = (end_index, start_index)
            return True
        else:
            self.clear()
            return False

    def search_prev(self, keyword):
        prev_index = self.prev_index[1]
        if keyword in self.plain_text[:prev_index]:
            start_index = self.plain_text[:prev_index].rindex(keyword)
            end_index = start_index + len(keyword)
            self.display(urwid.Text([
                self.plain_text[:start_index],
                ("match", keyword),
                self.plain_text[end_index:]
            ]))

            self.prev_index = (end_index, start_index)
            return True
        else:
            self.clear()
            return False

    def clear(self):
        self.prev_index = (0, len(self.plain_text))
        self.display(urwid.Text(self.plain_text))
