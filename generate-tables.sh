#/bin/bash

set -e

# process Corpora
for D in ./resource_families/Corpora/*/; do 
	[ -d "$D" ] && ./run.py -i "$D" -o "$D" -r ./rules.json
	trap "echo Corpora that failed to process: $D" 1 
done

# process Lexical_Resources
for D in ./resource_families/Lexical_Resources/*/; do 
	[ -d "$D" ] && ./run.py -i "$D" -o "$D" -r ./rules.json
	trap "echo Corpora that failed to process: $D" 1 
done

# process Tools
./run.py -i ./resource_families/Tools/"Named entity recognition" -o ./resource_families/Tools/"Named entity recognition" -r ./rules_ner.json
./run.py -i ./resource_families/Tools/"Normalization" -o ./resource_families/Tools/"Normalization" -r ./rules_norm.json
./run.py -i ./resource_families/Tools/"Part-of-speech tagging and lemmatization" -o ./resource_families/Tools/"Part-of-speech tagging and lemmatization" -r ./rules_pos.json
./run.py -i ./resource_families/Tools/"Tools for sentiment analysis" -o ./resource_families/Tools/"Tools for sentiment analysis" -r ./rules_senti.json
./run.py -i ./resource_families/Tools/"Corpus query tools" -o ./resource_families/Tools/"Corpus query tools" -r ./rules_query.json
