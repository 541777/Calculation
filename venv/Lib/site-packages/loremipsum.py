import argparse
from urllib import request, error
import pyperclip

URL = 'https://loripsum.net/api/'


class ParagraphLength():
    """Constants for the ``paragraph_length`` parameter in generate()"""

    #: List of values for paragraph lengths. Used internally.
    OPTIONS = [
        'short',
        'medium',
        'long',
        'verylong',
    ]

    SHORT = 0
    MEDIUM = 1
    LONG = 2
    VERY_LONG = 3

    @classmethod
    def get_option(cls, index):
        """Returns the string value that corresponds to the constants declared
        in this class. Used internally.

        :param index: One of the constants declared in this class
            (``SHORT``, ``MEDIUM``, ``LONG``, ``VERY_LONG``)

        :return: The corresponding string value for the loripsum.net API or
            None if the index is invalid
        """
        if isinstance(index, int) and index < len(cls.OPTIONS):
            return cls.OPTIONS[index]
        # Previous version of the class used strings instead of a list
        elif isinstance(index, str) and index in cls.OPTIONS:
            return index
        else:
            return None


#: Valid keys for html_options
HTML_OPTIONS = [
    'decorate',  # Add bold, italic and marked text.
    'link',  # Add links.
    'ul',  # Add unordered lists.
    'ol',  # Add numbered lists.
    'dl',  # Add description lists.
    'bq',  # Add blockquotes.
    'code',  # Add code samples.
    'headers',  # Add headers.
]


def _request_url_string(request_args):
    url_string = URL
    for arg in request_args:
        url_string += '{}/'.format(arg)
    return url_string


def _generate(request_url):
    placeholder_text = request.urlopen(request_url).read().decode('utf8')
    return placeholder_text


def generate(paragraph_count=None, paragraph_length=None, allcaps=False,
             prude=False, plaintext=True, html_options=None,
             trailing_newlines=False):
    """Generate Lorem Ipsum placeholder text using the https://loripsum.net API.

    Further documentation of parameters can be found at `loripsum.net <https://loripsum.net>`_

    :param paragraph_count: (Optional) The number of paragraphs to generate. If
        unspecified, API defaults to 4
    :param paragraph_length: (Optional) The average length of a paragraph. Possible
        values are declared as attributes in ``loremipsum.ParagraphLength``
        (``SHORT``, ``MEDIUM``, ``LONG``, ``VERY_LONG``). If unspecified, API
        defaults to 'long'
    :param allcaps: (Default = False) Use ALL CAPS
    :param prude: (Default = False) Prude version. From the API documentation:
        "The original text contains a few instances of words like 'sex' or 'homo'.
        Personally, we don't mind, because these are just common latin words
        meaning 'six' and 'man'. However, some people (or your clients) might be
        offended by this, so if you select the 'Prude version', these words will be
        censored."
    :param plaintext: (Default = True) Return plain text, no HTML
    :param html_options: (Default = None) List of html options to specify in
        request. This will be ignored if plaintext = True. The following options
        are accepted

            - 'decorate' - Add bold, italic and marked text.
            - 'link'- Add links.
            - 'ul' - Add unordered lists.
            - 'ol' - Add numbered lists.
            - 'dl' - Add description lists.
            - 'bq' - Add blockquotes.
            - 'code' - Add code samples.
            - 'headers' - Add headers.
    :param trailing_newlines: (Default = False) If False, strip trailing new lines
        in generated text. If True, leave trailing new lines in.

    :return: Result of querying loripsum.net API using the specified options
    """
    request_args = []
    paragraph_length = ParagraphLength.get_option(paragraph_length)
    if paragraph_count is not None:
        request_args.append(paragraph_count)
    if paragraph_length:
        request_args.append(paragraph_length)
    if allcaps:
        request_args.append('allcaps')
    if prude:
        request_args.append('prude')
    if plaintext:
        request_args.append('plaintext')
    # If not plaintext and html_options is specified, add those args as well
    elif html_options is not None:
        # Ignore invalid options
        valid_html_options = [
            option for option in html_options if option in HTML_OPTIONS
        ]
        request_args.extend(valid_html_options)
    request_url = _request_url_string(request_args)
    placeholder_text = _generate(request_url)
    return placeholder_text if trailing_newlines else placeholder_text.rstrip()


# Command Line Functions

def _parser(description=None):
    """Returns common ArgumentParser for command line functions"""
    parser = argparse.ArgumentParser(
        description=description,
        epilog='For more information, visit <https://connordelacruz.com/py-loremipsum/>'
    )
    parser.add_argument(
        'paragraph_count', type=int, nargs='?', default=1,
        help='(Default: 1) The number of paragraphs to generate'
    )
    parser.add_argument(
        '-l', '--length', dest='paragraph_length', type=str.lower, choices=ParagraphLength.OPTIONS,
        help='Specify the average length of a paragraph. API defaults to "long"'
    )
    parser.add_argument(
        '-C', '--allcaps', action='store_true', default=False,
        help='Use ALL CAPS'
    )
    parser.add_argument(
        '-p', '--prude', action='store_true', default=False,
        help='Omit Latin words that may be inappropriate in English'
    )
    # TODO: take html options? (using subparser or append w/ default=None and nargs='*'?)
    parser.add_argument(
        '-H', '--html', dest='plaintext', action='store_false', default=True,
        help='Generate HTML instead of plain text'
    )
    parser.add_argument(
        '-n', '--trailing-newlines', action='store_true', default=False,
        help='Keep trailing new lines'
    )
    return parser


def main():
    """Prints generated text using parsed args"""
    description = 'Generate "Lorem ipsum" text'
    args = _parser(description).parse_args()
    print(generate(**vars(args)))

def copy():
    """Copies generated text using parsed args to clipboard"""
    description = 'Generate "Lorem ipsum" text and copy to clipboard'
    args = _parser(description).parse_args()
    text = generate(**vars(args))
    try:
        pyperclip.copy(text)
    except pyperclip.PyperclipException as e:
        print(str(e), 'Generated text:\n', text, sep='\n')
    else:
        print('Generated text copied to clipboard.')


if __name__ == '__main__':
    main()


