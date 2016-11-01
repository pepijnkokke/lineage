import json
import sys
import re

class JSONListDecoder(json.JSONDecoder):
    """Streaming decoder for JSONList files."""

    def get_decoded_and_remainder(self, input_data):
        """Decode JSON value at the top of the input, and continue."""
        obj, end = self.raw_decode(input_data)
        remaining = input_data[end:]
        return (obj, remaining)


def read_ancestor_list(filename):
    """
    Read a list of JSON objects of the form {name: .., year: .., advisors: ..}.
    Return a dictionary from urls to names and children.
    """
    decoder = JSONListDecoder()
    people = dict()
    ancestry = dict()
    with open(filename, 'r') as file_handle:
        contents = file_handle.read()
        try:
            while True:
                person, remaining = decoder.get_decoded_and_remainder(contents)
                contents = remaining.lstrip()
                people.update({person['href']: person})
                for _, advisor_href in person['advisors'].iteritems():
                    ancestry.update({advisor_href: person['href']})
        except ValueError:
            pass
    return (people, ancestry)


def first_common_ancestors(people, ancestry1, ancestry2):
    """
    Compare two ancestor dictionaries. Return a list of common ancestors.
    """
    common_ids = set(ancestry1.keys()) & set(ancestry2.keys())

    return [people[a_id]
            for a_id in common_ids
            if ancestry1[a_id] != ancestry2[a_id]]

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "usage: python common_ancestors.py <ancestry1.>jl <ancestry2>.jl"
    else:
        RE_WHITESPACE = re.compile(ur'\s+')
        def trim_ws(s):
            return RE_WHITESPACE.sub(' ', s)

        URL = u'https://www.genealogy.math.ndsu.nodak.edu/id.php?id='
        ID1, ID2 = sys.argv[1:3]
        PEOPLE1, ANCESTRY1 = read_ancestor_list(ID1)
        PEOPLE2, ANCESTRY2 = read_ancestor_list(ID2)

        COMMON = first_common_ancestors(PEOPLE1, ANCESTRY1, ANCESTRY2)
        COMMON = sorted(COMMON, key=lambda x: x['year'], reverse=True)

        print "COMMON ANCESTORS OF:"
        print "  - ", trim_ws(PEOPLE1[URL+ID1.rstrip(".jl")]['name'])
        print "  - ", trim_ws(PEOPLE2[URL+ID2.rstrip(".jl")]['name'])
        print

        for ancestor in COMMON:
            print "%s: %s (%s)" % (
                str(ancestor['year']),
                trim_ws(ancestor['name']),
                ancestor['href'])
