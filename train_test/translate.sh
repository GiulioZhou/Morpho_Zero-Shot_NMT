#!/bin/bash

declare -a lang=("it" "ro" "de" "en" "nl")

data=data/morph
model=models/morph
translation=translations/morph

# Aplly truecaser
for SRC in "${lang[@]}"
        do
  for TRG in "${lang[@]}"
                do
                if [ "$SRC" = "$TRG" ]
                then
                    	continue
                fi
    echo $SRC-$TRG
CUDA_VISIBLE_DEVICES=2 /fs/elli0/zgiulio/experiments/projects/nematus/translate.py \
      --models $model/model.npz\
      --input $data/test.$SRC-$TRG.bpe.$SRC \
      --output $translation/$SRC-$TRG.$TRG
done
done





