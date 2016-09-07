try:  # pragma: no cover
    from pygments import token
except:  # pragma: no cover
    pygments_style = []
else:  # pragma: no cover
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
