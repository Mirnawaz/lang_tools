# Language Tools

This set of scripts will parse text and provide suggestions for spelling
and grammatical corrections. The scripts may be used on the command line with
verbose console output, or to produce JSON formatted output.

These scripts are intended to be merged into the _Immediate Feeback System_ as
part of the core tools.

## Prequisites

#### Python Hunspell
The spell check script makes use of Hunspell dictionaries and correction.
```
$ sudo apt install hunspell
```

You also need the python wrapper:
```
$ sudo -H pip install hunspell
```

#### Language Tool
Install LanguageTool and its python wrapper by:
```
$ sudo -H pip install --upgrade 3to2
$ sudo -H pip install --upgrade language-check
```

## Usage

### spell\_check.py

Run check on a file called `misspellings` against Canadian English dictionaries
with output to the console. If the `--lang` or short `-l` option isn't
specified, then the default language that is used is Canadian English.
```
spell_check.py --lang=en_CA -i mispellings
```

Run check on a file called `misspellings` against US English dictionaries, with
output to `corrections.json`.
```
spell_check.py --lang=en_US --outfile=corrections.json --infile=mispellings
spell_check.py -l en_US -o corrections.json -i misspellings
```

Note that if Hunspell is not installed at the default path
`/usr/share/hunspell`, then you may specify the path with either the `-p` or
the  `--path` option.

For instance:
```
spell_check.py --path=/opt/hunspell --infile=misspellings
spell_check.py -p /opt/hunspell -i misspellings
```

By default the list of correctly spelled words is suppressed from the output,
however this can be revealed by specifying either the `-c` or `--correct`
option.
```
spell_check.py --correct --ifile=misspellings
spell_check.py -c -i misspellings
```

For alternative, simplified plain English output, pass the `--english` flag.

To suppress output to console when an output file is specified, pass either
`-q` or `--quiet`.

For help:
```
spell_check.py --help
```

### grammar.py

Run check on a file called `bad_grammar` against Canadian English rules with
output to the console. If the `--lang` option isn't specified, then the
default language rules that are used belong to Canadian English.
```
grammar.py --lang=en_CA --ifile bad_grammar
grammar.py -l -i bad_grammar
```

Run check on a file called `bad_grammar` against US English rules, with output
to `grammatical.json`.
```
grammar.py --lang=en_US --json=grammatical.json --ifile bad_grammar
grammar.py -l en_US -j grammatical.json -i bad_grammar
```

For help:
```
grammar.py --help
```

## Caveats

### spell\_check.py

By nature of the engine, hyphenated compound words that are correct on each
side of the hyphen will pass the spellcheck even if the compound is not in the
given language's lexicon. Ex. "cat-dog" is not an English word, but will pass.

### grammar.py

Kind of slow?

## License Information

These scripts are
[free software](https://www.gnu.org/philosophy/free-sw.en.html), and are
licensed permissively under the ISC License. See the comment headers of each
script for additional information.

See also the license information attached to the libraries that were used for
this project.
