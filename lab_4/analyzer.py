from typing import Tuple, Iterable, Mapping, Callable

class StaticAnalyzer:
    def __init__(self, source: str):
        self._source = source
        self._tokens = self._tokenize(source)
        self._ast = self._construct_ast(self._tokens)

    def _tokenize(self, text: str) -> Tuple[str, ...]:
        result = []
        pos = 0
        while pos < len(text):
            if text[pos:min(pos + 2, len(text))] in ('**', '<=', '>=', '/>'):
                result.append(text[pos:min(pos + 2, len(text))])
                pos += 2
            elif text[pos] in ('+', '-', '*', '/', '>', '<', '=', '&', '(', ')', '{', '}', ';'):
                result.append(text[pos])
                pos += 1
            elif text[pos] in (' ', '\t', '\n', '\r'):
                pos += 1
            else:
                start = pos
                while pos < len(text) and (text[pos].isalpha() or text[pos].isnumeric() or text[pos] in ('_', '.')):
                    pos += 1
                result.append(text[start:pos])
                if start == pos:
                    print("ERROR")
                    break
        return result

    def _construct_ast(self, tokens: Tuple[str, ...]) -> Mapping[str, Callable[..., None]]:
        ast = {}
        for token in tokens:
            if token in ast:
                ast[token]()
            else:
                print(f"Unknown token: {token}")
        return ast

    def analyze(self) -> None:
        self._ast[self._tokens[0]]()
