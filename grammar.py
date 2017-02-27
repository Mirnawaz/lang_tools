#!/usr/bin/env python

# This script uses LanguageTool to process arbitrary text strings and provide
# suggestions for grammatical improvements.
#
# Copyright (c) 2017 Keefer Rourke <mail@krourke.org>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import sys
import getopt
import os
import io
import json
import re
import language_check


# grcheck(string to_check, string lang, language_check.LanguageTool ltool,
#         bool console)
def grcheck(to_check, lang, ltool, console):
    json_string = ''
    matches = ltool.check(to_check)
    num_matches = len(matches)

    if console is True:
        print 'lang: ', lang
        print 'matches: ', num_matches
        for i in range(num_matches):
            print "On line:", matches[i].fromy, "at char:", matches[i].fromx,
            print "rule violated:", matches[i].ruleId
            print "Message:", matches[i].msg
            print "Problem category:", matches[i].category
            print "Issue type:", matches[i].locqualityissuetype
            print "Possible replacements:",
            for j in range(len(matches[i].replacements)):
                print matches[i].replacements[j],
            print
            print "Context:", matches[i].context
            print
    # LanguageTool.check.Match type is not JSON serializeable
    # build a JSON string from the array of Match objects
    else:
        json_string += ('{ '
                        + '"lang": ' + '"' + lang + '", '
                        + '"num_matches": ' + str(num_matches) + ', '
                        + '"matches": { ')
        for i in range(num_matches):
            json_string += ('"' + str(i) + '": { '
                            + '"fromy": ' + str(matches[i].fromy) + ', '
                            + '"fromx": ' + str(matches[i].fromx) + ', '
                            + '"ruleId": ' + '"' + str(matches[i].ruleId)
                            + '", '
                            + '"msg": ' + '"' + str(matches[i].msg) + '", '
                            + '"category": ' + '"' + str(matches[i].category)
                            + '", '
                            + '"issuetype": ' + '"'
                            + str(matches[i].locqualityissuetype) + '", ')
            j_array = json.dumps(matches[i].replacements)
            json_string += ('"replacements": ' + j_array + ', '
                            + '"context": ' + '"' + str(matches[i].context)
                            + '"'
                            + ' }')
            if i != (num_matches - 1):
                json_string += ','
        json_string += ' } }'

        # make formatting prettier
        json_obj = json.loads(json_string)
        json_string = json.dumps(json_obj, indent=2, sort_keys=True)
        json_string += '\n'

        return json_string


# main program that takes arguments
def main(argv):
    supported_langs = language_check.get_languages()

    # options
    lang = 'en_CA'  # default language
    json_path = ''
    ifile = ''
    console = True

    # define command line arguments and check if the script call is valid
    opts, args = getopt.getopt(argv, 'l:j:i:h', ['lang=', 'json=', 'ifile=',
                               'help'])

    for opt, arg in opts:
        if opt in ('--lang', '-l'):
            lang = arg
            if lang not in supported_langs:
                sys.stderr.write('Error. Language ' + lang
                                 + ' not supported.\n')
                sys.stderr.write('Available languages:\n')
                for i in range(len(supported_langs)):
                    sys.stderr.write(supported_langs[i])
                    sys.stderr.write(' ')
                sys.stderr.write('\n')
                sys.exit()
        elif opt in ('--json', '-j'):
            json_path = arg
            console = False
        elif opt in ('--ifile', '-i'):
            ifile = arg
            if not (os.path.isfile(ifile)):
                sys.stderr.write('Error. File' + ifile + 'does not exist.')
                sys.exit()
        elif opt in ('--help', '-h') or opt not in ('--ifile', '-i'):
            print 'Usage:'
            print 'grammar.py [--lang=LANG] [--json=OUT.json]',
            print '--ifile=INPUTFILE'
            print
            print 'grammar.py [-l LANG] [-j OUT.json] -i INPUTFILE'
            print
            print 'Supported languages on this system:'
            for i in range(len(supported_langs)):
                print supported_langs[i],
            print
            sys.exit()
    # init language check
    ltool = language_check.LanguageTool(lang)

    # open infile for reading
    f_in = open(ifile, 'r')
    text = f_in.read()

    # perform analysis on file and return json_data for writing to file
    json_data = grcheck(text, lang, ltool, console)
    if console is False and json_data != '':
        json_out = open(json_path, 'w')
        json_out.write(json_data)
        json_out.close()

    f_in.close()

if __name__ == '__main__':
    main(sys.argv[1:])
