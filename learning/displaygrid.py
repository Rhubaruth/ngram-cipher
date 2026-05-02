import json

def main():
    import sys

    if len(sys.argv) < 2:
        print('Enter file as argument')
        return

    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except FileExistsError as e:
        print(e, '\nError with a file.')

    ngram2grid = dict(data)
    for key, item in ngram2grid.items():
        print(key, item)

    pass


if __name__ == "__main__":
    main()
