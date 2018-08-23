#/bin/sh

# path to moses decoder: https://github.com/moses-smt/mosesdecoder
mosesdecoder=./mosesdecoder
translations=../translations/morfessorfix
# suffix of target language files

declare -a lang=("de" "en" "it" "nl" "ro")

for SRC in "${lang[@]}"
	do
  for TRG in "${lang[@]}"
		do
    # tokenize
		if [ "$SRC" = "$TRG" ]
		then
			continue
		fi
echo $SRC-$TRG.$TRG
sed -i -e 's/\#\# //g' $translations/$SRC-$TRG.$TRG
sed -i -e 's/ \§\§//g' $translations/$SRC-$TRG.$TRG
sed -i -e 's/\@\@ //g' $translations/$SRC-$TRG.$TRG
sed -r 's/\@\@ //g' $translations/$SRC-$TRG.$TRG | \
$mosesdecoder/scripts/recaser/detruecase.perl | \
$mosesdecoder/scripts/tokenizer/detokenizer.perl -l $TRG > ../postprocessed/$SRC-$TRG.$TRG
done
done
