#!/bin/bash

declare -a lang=("de" "en" "it" "nl" "ro")

data=./data/alltrg

touch $data/corpus.src
touch $data/corpus.trg
touch $data/dev.src
touch $data/dev.trg

for SRC in "${lang[@]}"
	do
  for TRG in "${lang[@]}"
		do
      if [ "$SRC" = "$TRG" ]
  		then
  			continue
  		fi
      cat $data/train.$SRC-$TRG.bpe.$SRC >> $data/corpus.src
      cat $data/train.$SRC-$TRG.bpe.$TRG >> $data/corpus.trg
			echo $SRC-$TRG
      cat $data/dev.$SRC-$TRG.bpe.$SRC >> $data/dev.src
      cat $data/dev.$SRC-$TRG.bpe.$TRG >> $data/dev.trg
done
done
