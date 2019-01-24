#!/bin/sh
# input back up download from blogger
# 1. replace '&lt;' with '<' and replace '&gt;' with '>'
# 2. put each 'entry' on a separate line
sed 's/&lt;/</g; s/&gt;/>/g; s#</entry><entry>#</entry>\n<entry>#g' $1 > entries.xml
python entries_parser.py -i entries.xml
rm entries.xml
python calc_stats.py -i entries.csv
