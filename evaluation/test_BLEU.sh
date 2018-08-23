declare -a lang=("de" "en" "it" "nl" "ro")

postprocessed=postprocessed

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
mosesdecoder/scripts/generic/multi-bleu-detok.perl ../testref/test17.$SRC-$TRG.$TRG < ../$postprocessed/$SRC-$TRG.$TRG
done
done
