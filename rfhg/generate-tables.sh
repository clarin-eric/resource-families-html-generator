#bin/bash

set -e

echo "CORPORA"
# process Corpora
for D in ./static/resource_families/Corpora/*/; do 
        [ -d "$D" ] && python -m rfhg -i "$D" -o "./../tables/$(basename "$D")" -r static.rules/rules.json
        trap "echo Corpora that failed to process: $D" 1 
done

echo "LEXICAL RESOURCES"
# process Lexical_Resources
for D in ./static/resource_families/Lexical_Resources/*/; do 
	[ -d "$D" ] && python -m rfhg -i "$D" -o "./../tables/$(basename "$D")" -r static.rules/rules.json
	trap "echo Corpora that failed to process: $D" 1 
done

echo "TOOLS"
# process Tools
python -m rfhg -i static.resource_families/Tools/"Named entity recognition" -o "./../tables/Tools/Named entity recognition" -r static.rules/rules_ner.json
python -m rfhg -i static.resource_families/Tools/"Normalization" -o "./../tables/Tools/Normalization" -r static.rules/rules_norm.json
python -m rfhg -i static.resource_families/Tools/"Part-of-speech tagging and lemmatization" -o "./../tables/Tools/Part-of-speech tagging and lemmatization" -r static.rules/rules_pos.json
python -m rfhg -i static.resource_families/Tools/"Tools for sentiment analysis" -o "./../tables/Tools/Tools for sentiment analysis" -r static.rules/rules_senti.json
echo "prior"
python -m rfhg -i static.resource_families/Tools/"Corpus query tools" -o "./../tables/Tools/Corpus query tools" -r static.rules/rules_query.json
echo "posterior"
