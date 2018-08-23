
declare -a lang=("de" "en" "it" "nl" "ro")

source=out_dir
# source=test17
reference=../../../reference
base=../../B
morph=../../M


for SRC in "${lang[@]}"
	do
  for TRG in "${lang[@]}"
		do
		if [ "$SRC" = "$TRG" ]
		then
			continue
		fi
		# rm  compare/$SRC-\>$TRG

		 while read line; do
			# 	echo >> compare/$SRC-\>$TRG
			# 	echo SRC: >> compare/test17.$SRC-\>$TRG
			# 	sed $line'q;d' $source/test17.$SRC-$TRG.$SRC >> compare/$SRC-\>$TRG
			# 	echo REF: >> compare/$SRC-\>$TRG
			# 	sed $line'q;d' $reference/test17.$SRC-$TRG.$TRG >>  compare/$SRC-\>$TRG
			# 	echo Sys1: >> compare/$SRC-\>$TRG
			# 	sed $line'q;d' $base/$SRC-$TRG.$TRG >>  compare/$SRC-\>$TRG
			# 	echo Sys2: >> compare/$SRC-\>$TRG
			# 	sed $line'q;d' $morph/$SRC-$TRG.$TRG >>  compare/$SRC-\>$TRG
			echo >> compare/$SRC-\>$TRG
		 	echo SRC: >> compare/$SRC-\>$TRG
		 	sed $line'q;d' $source/test.$SRC-$TRG.$SRC >> compare/$SRC-\>$TRG
		 	echo REF: >> compare/$SRC-\>$TRG
		 	sed $line'q;d' $reference/test.$SRC-$TRG.$TRG >>  compare/$SRC-\>$TRG
		 	echo Sys1: >> compare/$SRC-\>$TRG
		 	sed $line'q;d' $base/$SRC-$TRG.$TRG >>  compare/$SRC-\>$TRG
		 	echo Sys2: >> compare/$SRC-\>$TRG
		 	sed $line'q;d' $morph/$SRC-$TRG.$TRG >>  compare/$SRC-\>$TRG
		 done < rare/$SRC-\>$TRG.rare

		sed -i -e ':r;$!{N;br};s/SRC:\n/SRC:/g' compare/$SRC-\>$TRG
		sed -i -e ':r;$!{N;br};s/REF:\n/REF:/g' compare/$SRC-\>$TRG
		sed -i -e ':r;$!{N;br};s/Sys1:\n/Sys1:/g' compare/$SRC-\>$TRG
		sed -i -e ':r;$!{N;br};s/Sys2:\n/Sys2:/g' compare/$SRC-\>$TRG
		sed -i -e 's/-2en-  //g' compare/$SRC-\>$TRG
		sed -i -e 's/-2it-  //g' compare/$SRC-\>$TRG
		sed -i -e 's/-2de-  //g' compare/$SRC-\>$TRG
		sed -i -e 's/-2nl-  //g' compare/$SRC-\>$TRG
		sed -i -e 's/-2ro-  //g' compare/$SRC-\>$TRG

done
done
