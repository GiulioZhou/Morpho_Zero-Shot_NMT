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
chrF/chrF++.py -R ../testref/test17.$SRC-$TRG.$TRG -H ../postprocessed/$SRC-$TRG.$TRG -b 3
done
done
