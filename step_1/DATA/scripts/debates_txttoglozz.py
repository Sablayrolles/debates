#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
The program takes (optionally segmented) CSV files as inputs, processes
the segment information (the "&"s) if applicable, and outputs an
(.ac, .aa) pair of Glozz files.

The output files contain:
  - the .ac file will contain the text attributes of the dialogue turns
    (without the '&', one turn on a line).
    - the .aa file will contain:
        - a pre-annotation in terms of:
            - dialogue information:
                - TODO define for this corpus
            - turn information:
                - borders (implicit)
                - Identifier (implicit)
                - Emitter
            - segment (EDU) information:
                - positioning: borders (implicit)
                - characterisation/type:
                    Task dialogue act: Offer | Counteroffer | Accept |
                                       Refusal | Strategic_comment | Other
                    - TODO define for this corpus
                - characterisation/feature/Surface_act:
                    Shallow dialogue act: Question | Request | Assertion
                    - TODO define for this corpus

Usage:
>>> ./debates_csvtoglozz.py -f <CSV file name>

@note: The output file names are formed by appending the .ac and .aa
extensions to the input CSV file basename.
Example: for an input filename like 2.seg.txt, the pair (2.ac, 2.aa) is
generated.
@note: The program supports filenames with empty spaces in them.
@note: Glozz is 0-indexed (but our .ac files systematically start with a
space)
'''

from __future__ import print_function
from xml.etree.ElementTree import Element, SubElement, Comment
from collections import namedtuple
import argparse
import codecs
import csv
import datetime
import itertools
import re
import sys
import time

from educe.stac.util.prettifyxml import prettify
from educe.stac.util.stac_csv_format import Turn


# ---------------------------------------------------------------------
# timestamps
# ---------------------------------------------------------------------
def mk_id(author=None):
    """Create a pair containing a brand new id and (false) creation-date.

    Parameters
    ----------
    author : string, optional
        If no author is given, use 'debates'.

    Returns
    -------
    the_id : str
        New identifier.

    fake_timestamp : int
        (False) creation date.
    """
    if author is None:
        author = 'debates'
    mk_id.counter += 1
    fake_timestamp = mk_id.starting_time + mk_id.counter
    the_id = '_'.join([author, str(fake_timestamp)])
    return (the_id, fake_timestamp)


def init_mk_id(start=None):
    """Initalise our glozz id/timestamp generator.

    Should be called once.

    Parameters
    ----------
    start : int, optional
        Starting time for timestamps ; If `None`, use the current time.
    """
    # not sure why this is preferable to time.time()
    # inherited it from the old version of the code
    now = time.mktime(datetime.datetime.now().timetuple())
    mk_id.starting_time = int(now) if start is None else start
    mk_id.counter = 0


# ---------------------------------------------------------------------
# building output
# ---------------------------------------------------------------------
def append_span(parent, left, right):
    """Append a positioning element to its parent (part of a span)
    """
    def single(elm, name, idx):
        "single position"
        sub = SubElement(elm, name)
        SubElement(sub, 'singlePosition', {'index': str(idx)})

    elm = SubElement(parent, 'positioning')
    single(elm, 'start', left)
    single(elm, 'end', right)


def append_unit(root, utype, features, left, right, author=None):
    """Append a new unit level annotation to the given root element.

    Note that this generates a new identifier behind the scenes.
    Effectively mutates root.

    Parameters
    ----------
    root : xml.etree.ElementTree.Element
        Root

    utype : str
        Unit type

    features : list of tuple of (str, str)
        Features

    left : int
        Position of the beginning of the unit span.

    right : int
        Position of the end of the unit span.

    author: string, optional
        If None, 'debates' is used (default value).
    """
    if author is None:
        author = 'debates'
    unit_id, date = mk_id(author=author)
    if right < left:
        raise Exception("Span with right boundary less than left")

    metadata = [('author', author),
                ('creation-date', str(date)),
                ('lastModifier', 'n/a'),
                ('lastModificationDate', '0')]
    elm_unit = SubElement(root, 'unit', {'id': unit_id})
    elm_metadata = SubElement(elm_unit, 'metadata')
    for key, val in metadata:
        SubElement(elm_metadata, key).text = val
    elm_charact = SubElement(elm_unit, 'characterisation')
    SubElement(elm_charact, 'type').text = utype

    elm_features = SubElement(elm_charact, 'featureSet')
    for key, val in features:
        f_elm = SubElement(elm_features, 'feature', {'name': key})
        f_elm.text = val

    append_span(elm_unit, left, right)


# ---------------------------------------------------------------------
# output
# ---------------------------------------------------------------------
def save_output(basename, dialoguetext, root):
    """Save output to a pair of files with a given name prefix.

    The pair of files has extensions .ac (for text) and .aa (for
    annotations).

    Parameters
    ----------
    basename : string
        Basename for files.
    dialoguetext : string
        Text that supports the annotation.
    root : xml.etree.Element
        XML representation of the annotation on `dialoguetext`.
    """
    with codecs.open(basename + ".ac", "w", "utf-8") as out:
        out.write(dialoguetext)
    with codecs.open(basename + ".aa", "w", "ascii") as out:
        out.write(prettify(root))


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------
def process_turn(root, dialoguetext, turn):
    """Process a single turn and return the augmented text.

    Any resulting annotations are appended to the root element (which is
    therefore mutated).

    Parameters
    ----------
    root : xml.etree.ElementTree.Element
        Root

    dialoguetext : str
        Text of the dialogue before this point.

    turn : tuple of (str, str, str)
        Turn described as a tuple of turn id, emitter, message.

    Returns
    -------
    dialoguetext : str
        Augmented dialogue text.
    """
    turn_id, emitter, msg = turn
    # store the beginning position of the turn
    turn_beg = len(dialoguetext)

    # append the prefix of the turn: "turn_id : emitter : "
    prefix = " : ".join([turn_id, emitter, ""])
    dialoguetext += prefix

    # split message into segments delimited by '&'
    # NEW except if it is escaped (preceded by '\'); then delete the
    # escaping character to restore the original text
    # this pattern uses "negative lookbehind" (?<!...),
    # see doc of the `re` module
    segs = [x for x in re.split('(?<![\\\])&', msg) if x]
    segs = [x.replace('\&', '&') for x in segs]
    # store a clean version of the turn text
    turn_text = ''.join(segs)

    # find the beginning and end position of each segment
    # alternative: use edu_spans() (see irit-stac/intake/csvtoglozz.py)
    seg_begs = [len(dialoguetext)]  # was: 0 (turn-relative)
    seg_ends = []
    for seg in segs:
        # adjust position of first character: skip one (if relevant) leading
        # whitespace
        if seg[0] == ' ':
            seg = seg[1:]
            seg_begs[-1] += 1
        seg_ends.append(seg_begs[-1] + len(seg))
        seg_begs.append(seg_ends[-1])
    seg_begs = seg_begs[:-1]  # drop the last beg
    # end find the beginning and end position of each segment

    # .ac buffer
    dialoguetext += turn_text + " "
    # .aa typographic annotations
    turn_end = len(dialoguetext) - 1  # exclude whitespace appended above

    # .aa actual pre-annotations (Turn ID, Timestamp, Emitter)
    # - append turn
    #   + add one paragraph per turn (better display in glozz)
    append_unit(root, utype='paragraph', features=[],
                left=turn_beg, right=turn_end)
    #   + add the turn itself
    feats = [('Identifier', turn_id), ('Emitter', emitter)]
    append_unit(root, utype='Turn', features=feats,
                left=turn_beg, right=turn_end)
    # - append each segment, ie. EDU
    for seg_beg, seg_end in zip(seg_begs, seg_ends):
        append_unit(root, utype='Segment', features=[],
                    left=seg_beg, right=seg_end)

    return dialoguetext


def process_turns(turns):
    """Process a list of Turns and return a pair of:

    * text
    * standoff annotations (an XML element)

    Parameters
    ----------
    turns : list of (int, str, str)
        List of turns, where each turn is a tuple (turn_idx, emitter,
        message).

    Returns
    -------
    dialoguetext : str
        Text

    root : xml.etree.ElementTree.Element
        Annotation on the text
    """
    root = Element('annotations')
    root.append(Comment('Generated by debates_csvtoglozz.py'))

    dialoguetext = " "  # for the .ac file

    for turn in turns:
        dialoguetext = process_turn(root, dialoguetext, turn)

    append_unit(root, utype='Dialogue', features=[], left=0,
                right=len(dialoguetext) - 1, author=None)

    return dialoguetext, root


def parse_args():
    "parse command line arguments"
    parser = argparse.ArgumentParser(
        description=("from an optionally segmented debate debate transcript"
                     "to a pair of Glozz files")
    )
    parser.add_argument('-f', '--file',
                        required=True,
                        help="specify input file")
    parser.add_argument('--start',
                        type=int,
                        help="starting timestamp (default: current time)")
    return parser.parse_args()


def main():
    """parse command line and handle file"""
    args = parse_args()
    init_mk_id(args.start)
    filename = args.file
    with open(filename, 'rb') as file_in:
        turns = []
        turn_idx = 0
        for line in file_in:
            line = line.strip()
            if not line:
                continue
            turn_idx += 1
            emitter, msg = line.split(': ', 1)
            turn = (str(turn_idx), emitter, msg)
            turns.append(turn)
    txt, xml = process_turns(turns)
    save_output(filename.split(".")[0], txt, xml)


if __name__ == '__main__':
    main()
