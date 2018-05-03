# -*- coding: utf-8 -*-

# Author: Eric Kow
# License: BSD3

"""
Create an .aam file from a .seg.txt file.

The empty set is represented by '?' and the whole set is
represented by 'All'

Usage:
    debates_create-glozz-aam.py input.seg.txt output.aam
"""

from __future__ import print_function
import argparse
from itertools import chain, combinations
import sys
import xml.etree.ElementTree as ET


# ---------------------------------------------------------------------
# template
# ---------------------------------------------------------------------
ANNO_SURFACE_ACTS = ['Assertion', 'Question']

ANNO_REACT = ['+', '0', '-']

TURN_ATTRS = ['Identifier', 'Emitter']

SPEECH_ACTS = [
    ('Proposition', ['recipient', 'emitter', 'reaction_public',
                     'reaction_emitter', 'reaction_recipient']),
    ('Attack', ['recipient', 'emitter', 'reaction_public',
                'reaction_emitter', 'reaction_recipient']),
    ('Counterattack', ['recipient', 'emitter', 'reaction_public',
                       'reaction_emitter', 'reaction_recipient']),
    ('Question', ['reaction_public', 'reaction_emitter',
                  'reaction_recipient']),
    ('Change_of_subject', []),
    ('Taking_part', ['recipient']),
    ('Other', []),
]

DISCOURSE_REL_TYPES = [
    'Attack',
    'Avoidance',
    'Conditional',
    'Continuation',
    'Elaboration',
    'Explanation',
    'Q-Elab',
    'Q-clar',  # 'Clarification_question',
    'Question-answer_pair',
    'Result',
]


# ---------------------------------------------------------------------
# template
# ---------------------------------------------------------------------

def mk_feature(name, default='', type='free'):
    feature = ET.Element('feature', name=name)
    value = ET.Element('value', type=type, default=default)
    feature.append(value)
    return feature


def mk_value(val):
    elm = ET.Element('value')
    elm.text = val
    return elm


def mk_comments():
    return mk_feature('Comments', default='Please write in remarks...')


def mk_radio(name, choices):
    elm = ET.Element('feature', name=name)
    pv = ET.Element('possibleValues', default='Please choose...')
    pv.extend(list(map(mk_value, choices)))
    elm.append(pv)
    return elm


def mk_featureSet(features):
    elm = ET.Element('featureSet')
    elm.extend(features)
    return elm


def mk_type(name, groups, features):
    elm = ET.Element('type', name=name, groups=groups)
    if features is not None:
        elm.append(mk_featureSet(features))
    return elm


def mk_speech_act(name, feature_names, speaker_combos):
    feats = [mk_radio('Surface_act', ANNO_SURFACE_ACTS)]
    for fname in feature_names:
        if fname in ('recipient', 'emitter'):
            fvals = speaker_combos
        elif fname.startswith('reaction_'):
            fvals = ANNO_REACT
        feats.append(mk_radio(fname, fvals))
    return mk_type(name, 'Complex_discourse_unit', feats)


def mk_discourse_relation(name):
    feats = [
        # mk_radio('Argument_scope', anno_argument_scope),
        mk_comments()
    ]
    elm = mk_type(name, 'Discourse', feats)
    elm.attrib['oriented'] = 'true'
    return elm


def create_model(speakers):
    """Create the annotation model for Glozz.

    Parameters
    ----------
    speakers : list of str
        List of speakers, for 'emitter' and 'recipient'.
    """
    # local copy of the list of discourse relations
    disc_rel_types = list(DISCOURSE_REL_TYPES)

    combos_ = emitter_combinations(speakers)
    combos = [', '.join(sorted(list(c))) for c in combos_]

    root = ET.Element('annotationModel')
    units = ET.Element('units')
    relations = ET.Element('relations')
    schemas = ET.Element('schemas')

    # units
    ty_turn_feats = list(map(mk_feature, TURN_ATTRS)) + [mk_comments()]
    ty_turn = mk_type('Turn', 'Bargaining_block', ty_turn_feats)

    ty_segment = mk_type('Segment', 'Complex_discourse_unit', None)

    units.extend([ty_turn, ty_segment])
    units.extend([mk_speech_act(x, fnames, combos)
                  for x, fnames in SPEECH_ACTS])

    # resources
    relations.extend([mk_discourse_relation(x) for x in disc_rel_types])

    # schemas
    ty_bblock = mk_type('Bargaining_block', 'Blocks', [])
    ty_cdus = mk_type('Complex_discourse_unit', 'CDUs', [])

    schemas.extend([ty_bblock, ty_cdus])

    root.extend([units, relations, schemas])
    return root


# in-place prettyprint formatter
# taken from http://effbot.org/zone/element-lib.htm
def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# ---------------------------------------------------------------------
# reading soclog (csv)
# ---------------------------------------------------------------------

def read_speakers(filename):
    """Get the list of players for the game from a CSV file.

    Parameters
    ----------
    filename: string
        Path to the (segmented) text file.

    Returns
    -------
    speakers: set of string
        Set of speaker names.
    """
    speakers = set()
    with open(filename, 'r') as infile:
        for line in infile:
            if not line.strip():
                continue
            speaker = line.split(':', 1)[0]
            speakers.add(speaker)
    speakers = frozenset(speakers)
    return speakers


def emitter_combinations(s):
    """
    emitter_combinations(['a','b','c']) ~~>
        ('?') ('1') ('2') ('3') ('1','2') ('1','3') ('2','3') ('All')

    Note, `~~>` because input is expected to be a frozenset, and
    output is a list of frozensets, ordered by size
    """
    sizes = range(1, len(s))
    almost_pset = chain.from_iterable(
        combinations(s, r) for r in sizes)
    results = [['All'], ['?']]
    results.extend(almost_pset)
    return list(map(frozenset, results))


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------

def main():
    "no surprises"
    psr = argparse.ArgumentParser("Create Debates .aam")
    psr.add_argument("input", metavar="INFILE_SEG_TXT",
                     help="seg.txt file")
    psr.add_argument("output", metavar="OUTFILE_AAM",
                     help="output aam file")
    psr.add_argument("--speakers", nargs='+', metavar="NAME",
                     help="override speaker set")

    args = psr.parse_args(sys.argv[1:])  # ugh, assume Python interpreter

    players = args.speakers or read_speakers(args.input)
    model = create_model(players)
    indent(model)  # sigh, imperative
    model_tree = ET.ElementTree(model)
    model_tree.write(args.output,
                     encoding='utf-8',  # was 'utf-8' for py2 ?! and unicode for py3
                     xml_declaration=True)


if __name__ == '__main__':
    main()
