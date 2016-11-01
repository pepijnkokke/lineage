import json
import re
import sys

class JSONListDecoder(json.JSONDecoder):
    """Streaming decoder for JSONList files."""

    def get_decoded_and_remainder(self, input_data):
        """Decode JSON value at the top of the input, and continue."""
        obj, end = self.raw_decode(input_data)
        remaining = input_data[end:]
        return (obj, remaining)


def read_ancestor_list(filename):
    """
    Read a list of JSON objects of the form {url: .., name: .., child: ..}.
    Return a dictionary from urls to names and children.
    """
    re_whitespace = re.compile(ur'\s+')
    decoder = JSONListDecoder()
    ancestry = dict()
    with open(filename, 'r') as file_handle:
        contents = file_handle.read()
        try:
            while True:
                obj, remaining = decoder.get_decoded_and_remainder(contents)
                contents = remaining.lstrip()
                obj['name'] = re_whitespace.sub(' ', obj['name'][0])
                ancestry[obj['url']] = obj
        except ValueError:
            pass
    return ancestry


def common_ancestors(ancestry1, ancestry2):
    """
    Compare two ancestor dictionaries. Return a list of common ancestors.
    """
    common_ancestor_ids = set(ancestry1.keys()) & set(ancestry2.keys())

    return [
        (ancestry1[ancestor_id]['name'], ancestry1[ancestor_id]['url'])
        for ancestor_id in common_ancestor_ids
        if  ancestry1[ancestor_id]['child'] != ancestry2[ancestor_id]['child']
    ]


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "usage: python common_ancestors.py <ancestry1.>jl <ancestry2>.jl"
    else:
        ANCESTRY1 = read_ancestor_list(sys.argv[1])
        ANCESTRY2 = read_ancestor_list(sys.argv[2])
        for common_ancestor in common_ancestors(ANCESTRY1, ANCESTRY2):
            print "%s (%s)" % common_ancestor
