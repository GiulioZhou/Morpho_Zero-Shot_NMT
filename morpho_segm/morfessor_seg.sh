#!/bin/sh


# declare -a lang=("en" "it")
declare -a lang=("de" "en" "it" "ro" "nl")

# path to the datasets
# dataset=../testnem/wmt16-scripts/sample/data/base
dataset=./data
data=./data_m
model=.
morfessor=./scripts



# while read p; do
#   echo $p > tmp
# 	./scripts/morfessor-segment -l model.it -o ./test tmp --output-newlines --output-format-separator ' §§' --output-format "{analysis} "
# 	cat ./test >> train.it3
# 	echo $p
# 	wc -l train.it3
# done <x08 #data/train.en-it.tc.it
#



for SRC in "${lang[@]}"
	do
  for TRG in "${lang[@]}"
		do
		if [ "$SRC" = "$TRG" ]
		then
			continue
		fi

    for prefix in train.$SRC-$TRG dev.$SRC-$TRG test.$SRC-$TRG
     do

		# 	 sed -i -e 's/^/@@@ /' $data/$prefix.tc.$TRG
		#
		# $morfessor/morfessor-segment -l $model/model.$SRC -o $data/$prefix.morfessor.$SRC $dataset/$prefix.tc.$SRC  --output-newlines --output-format-separator ' §§' --output-format "{analysis} "
 	# 	$morfessor/morfessor-segment -l $model/model.$TRG -o $data/$prefix.morfessor.$TRG $dataset/$prefix.tc.$TRG  --output-newlines --output-format-separator ' §§' --output-format "{analysis} "
		#
		# sed -i -e 's/@ §§@ §§@/ /g' $data/$prefix.morfessor.$TRG
		# sed -i -e 's/@@@/ /' $data/$prefix.tc.$TRG

		# ./morfessor_preproc.py $data/$prefix.morfessor.$SRC  $data/$prefix.morf.$SRC
		# ./morfessor_preproc.py $data/$prefix.morfessor.$TRG  $data/$prefix.morf.$TRG

		# wc -l $data/$prefix.tc.$SRC
		# wc -l $data/$prefix.morfessor.$SRC
		# wc -l $data/$prefix.morfessor.$TRG


		if [ "en" = "$TRG" ]
		then
			 sed -i -e 's/- §§2 §§en §§-/-2en-/g' $data/$prefix.fix.$SRC
			 sed -i -e 's/- §§2 §§e §§n §§-/-2en-/g' $data/$prefix.fix.$SRC

		fi
		if [ "de" = "$TRG" ]
		then
			sed -i -e 's/- §§2 §§de §§-/-2de-/g' $data/$prefix.fix.$SRC
			sed -i -e 's/- §§2 §§d §§e §§-/-2de-/g' $data/$prefix.fix.$SRC

		fi
		if [ "it" = "$TRG" ]
		then
			sed -i -e 's/- §§2 §§it §§-/-2it-/g' $data/$prefix.fix.$SRC
			sed -i -e 's/- §§2 §§i §§t §§-/-2it-/g' $data/$prefix.fix.$SRC

		fi
		if [ "nl" = "$TRG" ]
		then
			sed -i -e 's/- §§2 §§n §§l §§-/-2nl-/g' $data/$prefix.fix.$SRC
			sed -i -e 's/- §§2 §§nl §§-/-2nl-/g' $data/$prefix.fix.$SRC

		fi
		if [ "ro" = "$TRG" ]
		then
			sed -i -e 's/- §§2 §§ro §§-/-2ro-/g' $data/$prefix.fix.$SRC
			sed -i -e 's/- §§2 §§r §§o §§-/-2ro-/g' $data/$prefix.fix.$SRC
		fi

     done

done
done

# rm $data/*.morfessor.*
