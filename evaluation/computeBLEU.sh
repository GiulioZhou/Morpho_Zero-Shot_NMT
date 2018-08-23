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
mosesdecoder/scripts/generic/multi-bleu-detok.perl ../reference/test.$SRC-$TRG.$TRG < ../postprocessed/$SRC-$TRG.$TRG
#mosesdecoder/scripts/generic/multi-bleu-detok.perl  ../postprocessed/$SRC-$TRG.$TRG <  ../reference/test.$SRC-$TRG.$TRG

done
done
