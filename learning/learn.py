from string import ascii_lowercase, whitespace, digits
import json

ALLOWED_ALPHABET = ascii_lowercase + ',.'

# For learning replace everyting with '.'
PUNC_SUBSTITUTIONS = {
    '?': ',.,',
    '!': ',.',
    ':': '..',
    ';': '.,',
    '-': ',',
    ',': ',',
}
LETTER_SUBSTITUTION = {
        'á': 'a',
        'č': 'c',
        'ď': 'd',
        'é': 'e',
        'ě': 'e',
        'ň': 'n',
        'ř': 'r',
        'š': 's',
        'ť': 't',
        'ú': 'u',
        'ů': 'u',
        'ý': 'y',
        'ž': 'z',

}


def main():
    import sys
    print(sys.argv)

    if len(sys.argv) < 2:
        print('Enter file as argument')
        raise ValueError
    elif len(sys.argv) < 3:
        reverse = False
    elif sys.argv[2].lower() == "true":
        reverse = True

    filename = sys.argv[1]

    lines = []
    with open(filename) as file:
        lines = file.readlines()

    conjoined = ' '.join(lines)
    conjoined = conjoined.replace('\n', '')
    conjoined = normalize_text(conjoined)

    normalized_lines = [line.strip()
                        for line in conjoined.split('.')
                        if len(line.strip()) > 0]
    # print(normalized_lines)

    ngrams = {}
    for idx, line in enumerate(normalized_lines):
        ng = find_ngrams(line)

        for ngram, count in ng.items():
            val = ngrams.get(ngram, 0)
            ngrams[ngram] = val + 1

        # if idx > 10:
        #     break
        pass

    sorted_ngrams = sorted(
        ngrams.items(),
        key=lambda item: item[1]**len(item[0]),
        reverse=True
    )

    print(*sorted_ngrams, sep='\n', end='\n\n\n')

    marked_letters = []
    for key, _ in sorted_ngrams:
        for char in key:
            if char in marked_letters:
                break
        else:
            # the loop not encountered break
            print(key)
            marked_letters += key

            if len(marked_letters) >= 26:
                break
    marked_letters = sorted(marked_letters)
    print("MARKED:", marked_letters)

    return reverse


def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = text.lstrip()

    for key, val in LETTER_SUBSTITUTION.items():
        if key not in text:
            continue
        text = text.replace(key, val)
    for key in PUNC_SUBSTITUTIONS.keys():
        if key not in text:
            continue
        text = text.replace(key, '.')
    normalized = ""

    for a in text:
        if a in ALLOWED_ALPHABET:
            normalized += a
        elif a in whitespace:
            normalized += ' '
    return normalized


def find_ngrams(line: str):
    ngrams = {}

    def add_ngram(ngram: str):
        ngram = ngram.strip()
        if not ngram:
            return

        val = ngrams.get(ngram, 0)
        ngrams[ngram] = val + 1

    line = line.replace(' ', '')
    line = line + '  '

    for x, y, z in zip(line, line[1:], line[2:]):
        add_ngram(x)
        add_ngram(x+y)
        # add_ngram(x+y+z)

    return ngrams


if __name__ == "__main__":
    main()
