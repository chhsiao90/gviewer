try:
    from pygments import token
except:  # pragma: no cover
    pygments_style = []
else:
    pygments_style = [
        (token.Token.Text, "white", "black"),
        (token.Token.Name, "white", "black"),
        (token.Token.Name.Builtin, "light magenta", "black"),
        (token.Token.Name.Function, "light magenta", "black"),
        (token.Token.Name.Class, "light magenta", "black"),
        (token.Token.Comment, "dark gray", "black"),
        (token.Token.Literal, "brown", "black"),
        (token.Token.Literal.String, "brown", "black"),
        (token.Token.Literal.String.Number, "light cyan", "black"),
        (token.Token.Literal.String.Double, "light cyan", "black"),
        (token.Token.Literal.String.Escape, "light cyan", "black"),
        (token.Token.Literal.Number.Integer, "brown", "black"),
        (token.Token.Operator, "white", "black"),
        (token.Token.Error, "white", "black"),
        (token.Token.Other, "white", "black"),
        (token.Token.Keyword, "dark cyan", "black"),
        (token.Token.Keyword.Namespace, "light green", "black"),
        (token.Token.Generic, "white", "black")
    ]

palette = [
    ("header", "white", "dark green", "bold"),
    ("footer helper", "white", "dark blue", "bold"),
    ("footer info", "white", "black"),
    ("summary", "white", "black"),
    ("summary focus", "black", "light gray"),
    ("view-item", "white", "black"),
    ("view-item key", "light cyan", "black"),
    ("view-item value", "white", "black"),
    ("view-title", "yellow", "black", "bold"),
    ("tabs", "white", "black", "bold"),
    ("tabs focus", "white", "dark blue", "bold"),
    ("match", "black", "light gray"),
    ("help title", "white", "black", "bold"),
    ("help key", "light cyan", "black"),
    ("help value", "white", "black")
] + pygments_style
