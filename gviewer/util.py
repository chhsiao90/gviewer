try:
    import pygments
except:  # pragma: no cover
    pass


def pygmentize(content, lexer):
    if not pygments:  # pragma: no cover
        raise ImportError("no pygments")
    pygments_list = list(pygments.lex(content, lexer))
    return _join(pygments_list, (pygments.token.Token.Text, u"\n"))


def _join(markup_list, join_tag):
    combined_list = []
    while markup_list:
        if join_tag not in markup_list:
            combined_list.append(markup_list)
            break
        index = markup_list.index(join_tag)
        if index:
            combined_list.append(markup_list[:index])
        else:
            combined_list.append("")
        markup_list = markup_list[index + 1:]
    return combined_list
