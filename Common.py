from typing import List


def split_string(in_str: str, splitter: str = ',') -> List[str]:
    quotes = ('"', "'")

    res = ['']
    cur_quote = None

    for s in in_str:
        if cur_quote:
            if s == cur_quote:
                cur_quote = None
            res[-1] += s
        else:
            if s in quotes:
                cur_quote = s
                res[-1] += s
            else:
                if s == splitter:
                    res.append('')
                else:
                    res[-1] += s

    return list(map(lambda x: x.strip(), res))
