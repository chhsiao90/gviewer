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
        """Check that current state is editing or not

        Override this method if that widget had Edit widget in its content
        and return True if the focus widget is the Edit widget

        Returns:
            True if in editing, False if not in editing
        """
        return False

    def update_info(self):
        """Callback when view is being displayed"""
        pass


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
        if key == "enter" and self._w.edit_text:
            self.search_func(self._w.edit_text)
            return None
        if key == "esc" or (key == "enter" and not self._w.edit_text):
            self.clear()
            self.clear_func()
            return None
        return super(SearchWidget, self).keypress(size, key)


class SearchableText(BasicWidget):
    """ Searchable text let its content could be search and hightlight

    Attributes:
        text: str or unicode or text_markup
    """
    def __init__(self, text, **kwargs):
        if isinstance(text, tuple):  # NOTE: not accept tuple type markup
            raise NotImplementedError("not accept tuple type markup")

        super(SearchableText, self).__init__(
            widget=urwid.Text(text), **kwargs)

        self.text = text
        self.prev_index = (0, len(text))

    def search_next(self, keyword):
        prev_index = self.prev_index[0]
        if isinstance(keyword, bytes):
            keyword = keyword.decode("utf8")

        if isinstance(self.text, str):
            if keyword in self.text[prev_index:]:
                start_index = self.text[prev_index:].index(keyword) + prev_index
                self._handle_match_plain_text(keyword, start_index)
                return True
        else:
            for index in range(prev_index, len(self.text)):
                plain_text, _ = decompose_tagmarkup(self.text[index])
                if keyword in plain_text:
                    self._handle_match_markup(keyword, plain_text, index)
                    return True

        self.clear()
        return False

    def search_prev(self, keyword):
        prev_index = self.prev_index[1]
        if isinstance(keyword, bytes):
            keyword = keyword.decode("utf8")

        if isinstance(self.text, str):
            if keyword in self.text[:prev_index]:
                start_index = self.text[:prev_index].rindex(keyword)
                self._handle_match_plain_text(keyword, start_index)
                return True
        else:
            for index in reversed(range(0, prev_index)):
                plain_text, _ = decompose_tagmarkup(self.text[index])
                if keyword in plain_text:
                    self._handle_match_markup(keyword, plain_text, index)
                    return True

        self.clear()
        return False

    def _handle_match_plain_text(self, keyword, start_index):
        end_index = start_index + len(keyword)
        self.display(urwid.Text([
            self.text[:start_index], ("match", keyword), self.text[end_index:]]))
        self.prev_index = (end_index, start_index)

    def _handle_match_markup(self, keyword, plain_text, index):
            match_index = plain_text.index(keyword)
            match_end_index = match_index + len(keyword)
            match_markup = []
            if plain_text[:match_index]:
                match_markup.append(plain_text[:match_index])
            match_markup.append(("match", keyword))
            if plain_text[match_end_index:]:
                match_markup.append(plain_text[match_end_index:])
            new_markup = self.text[:index] + match_markup + self.text[index + 1:]
            self.display(urwid.Text(new_markup))
            self.prev_index = (index + 1, index)

    def get_plain_text(self):
        text, _ = decompose_tagmarkup(self.text)
        if isinstance(text, bytes):
            return text.decode("utf8")
        else:
            return text

    def clear(self):
        self.prev_index = (0, len(self.text))
        self.display(urwid.Text(self.text))
