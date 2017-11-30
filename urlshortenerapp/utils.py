
ALPHABETS = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
base = len(ALPHABETS)


def encode(num):
    """ Converts base 10 integer to base 58 string """
    if (not isinstance(num, int) or num < 0):
        return ''
    encoded = ''
    while (num):
        remainder = num % base
        num = num // base
        encoded = str(ALPHABETS[remainder])+encoded
    return encoded


def decode(s):
    """ Converts base 58 string into base 10 integer """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * ALPHABETS.index(char)
        multi = multi * base
    return decoded


def gethashkeyfromurl(url):
    """ Retrieves hash key from url """
    if url:
        url = url.strip("/")
        url.rsplit('/', 1)
    return url
