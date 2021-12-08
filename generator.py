import random
import string

INF = 1000000000000000000


def gen(text_len, pattern_len, path):
    texts = []
    pos = 0
    pattern = ''.join(random.choices(string.ascii_letters, k=pattern_len))
    while pos < text_len:
        gap = ''.join(random.choices(string.ascii_letters, k=random.randint(0, 15 * pattern_len)))
        texts.append(gap)
        pos += len(gap)
        texts.append(pattern)
        pos += len(pattern)

    with open(path, 'w+') as f:
        f.write(''.join(texts) + '\n')
        f.write(pattern + '\n')

    return ''.join(texts), pattern


def gen_expected(_text, _pattern, path):
    result = 0
    combined = _pattern + '#' + _text
    pi = [0]
    for i in range(1, len(combined)):
        j = pi[i - 1]
        while j > 0 and combined[i] != combined[j]:
            j = pi[j - 1]
        if combined[i] == combined[j]:
            j += 1
        pi.append(j)
    for i in range(len(_pattern), len(combined)):
        if pi[i] == len(_pattern):
            result += 1
    with open(path, 'w+') as f:
        f.write(str(result))


if __name__ == '__main__':
    text, pattern = gen(10000000, 500, "input10000000.txt")
    gen_expected(text, pattern, "expected_output.txt")
