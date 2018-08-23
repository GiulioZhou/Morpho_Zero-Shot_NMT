#!/bin/bash

declare -a lang=("de" "it" "en" "nl" "ro")
declare -a zero=("it-ro ro-it de-nl nl-de")

data=./data/140base
touch $data/corpus_zero.src
touch $data/corpus_zero.trg
touch $data/dev_zero.src
touch $data/dev_zero.trg

for SRC in "${lang[@]}"
	do
  for TRG in "${lang[@]}"
		do
      if [ "$SRC" = "$TRG" ]
  		then
  			continue
  		fi
			if [[ " ${zero[*]} " == *"$SRC-$TRG"* ]]; then
				continue
			fi

      cat $data/train.$SRC-$TRG.bpe.$SRC >> $data/corpus_zero.src
      cat $data/train.$SRC-$TRG.bpe.$TRG >> $data/corpus_zero.trg
			echo $SRC-$TRG
      cat $data/dev.$SRC-$TRG.bpe.$SRC >> $data/dev_zero.src
      cat $data/dev.$SRC-$TRG.bpe.$TRG >> $data/dev_zero.trg
done
done
