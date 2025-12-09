from string import ascii_lowercase, whitespace
import json


def main():
    import sys

    if len(sys.argv) < 2:
        print('Enter file as argument')
        raise
    elif len(sys.argv) < 3:
        reverse = False
    elif sys.argv[2].lower() == "true":
        reverse = True

    wanted_bigrams = list(set('HasturKingInYellow'.lower()))
    for a in ascii_lowercase:
        for b in ascii_lowercase:
            if a == b:
                continue
            bigram = a+b
            if bigram in wanted_bigrams \
                    or similar_exists(bigram, wanted_bigrams):
                continue
            wanted_bigrams.append(bigram)

    freqs = find_ngrams(sys.argv[1], wanted_bigrams, reverse_text=reverse)

    ngram2grid = {}
    a = 0
    while freqs:
        try:
            for x in range(a+1):
                ngram, _ = freqs.pop(0)
                ngram2grid[ngram] = (x, a)
            for y in range(a):
                ngram, _ = freqs.pop(0)
                ngram2grid[ngram] = (a, y)
            a += 1
        except IndexError:
            break

    ngram2grid_json = json.dumps(ngram2grid, sort_keys=False, indent=4)
    print(ngram2grid_json)


def first_letter_contained(text: str, arr: list[str]) -> bool:
    if not arr or not text:
        return False
    for a in arr:
        if text.startswith(a[0]):
            return True
    return False


def similar_exists(text: str, arr: list[str]) -> bool:
    if not arr or not text:
        return False
    if text in arr:
        return True
    for a in arr:
        if text.startswith(a):
            return True
    return False


def normalize_text(text: str) -> str:
    text = text.strip().lower()
    normalized = ""

    for a in text:
        if a in ascii_lowercase:
            normalized += a
        elif a in whitespace:
            normalized += ' '
    return normalized


def find_ngrams(filename: str, keys: list[str], reverse_text: bool = False):
    try:
        with open(filename) as file:
            lines = file.readlines()
    except FileNotFoundError:
        print('File does not exist.')
        return

    ngrams = {k: 0 for k in keys}

    def add_ngram(ngram: str):
        val = ngrams.get(ngram, 0)
        ngrams[ngram] = val + 1

    for line in lines:
        line = normalize_text(line)
        if reverse_text:
            line = line[::-1]

        words = line.split(' ')

        for w in words:
            if not w:
                continue
            for double in zip(w, w[1:]):
                bigram = ''.join(double)
                if bigram not in keys:
                    continue
                add_ngram(bigram)
            if w[-1] in keys:
                add_ngram(w[-1])

    sorted_ngrams = sorted(
        ngrams.items(),
        key=lambda item: item[1] if len(item[0]) > 1 else item[1] / 10,
        reverse=True
    )

    return sorted_ngrams


if __name__ == "__main__":
    main()
