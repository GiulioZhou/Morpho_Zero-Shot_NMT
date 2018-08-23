
declare -a lang=("de" "en" "it" "nl" "ro")
# declare -a lang=("de" "en" "it")

# path to subword segmentation scripts: https://github.com/rsennrich/subword-nmt
subword_nmt=../../subword-nmt

# path to nematus ( https://www.github.com/rsennrich/nematus )
nematus=../../nematus

# path to moses decoder: https://github.com/moses-smt/mosesdecoder
mosesdecoder=../../mosesdecoder

data_dir=./test17/alltrg
# path to the datasets
dataset=./test17

model_dir=./alltrg


# echo Morph segmentation
# # apply suffix and prefix segmentation
# for SRC in "${lang[@]}"
# 	do
#   for TRG in "${lang[@]}"
# 		do
# 		if [ "$SRC" = "$TRG" ]
# 		then
# 			continue
# 		fi
# 		echo $SRC-$TRG
#    for prefix in test17.$SRC-$TRG
#     do
# 			 ./morphoSegmenter.py $SRC $dataset/$prefix.$SRC $data_dir/$prefix.morph.$SRC
#  		done
# done
# done
#
# echo Train merge BPE
# cat ./data/morph/train*.morph.* | ./learn_bpe_merge.py -s $bpe_merge_operations > $model_dir/all_morph.bpe
#
# echo Apply merge BPE
# for SRC in "${lang[@]}"
# 	do
#   for TRG in "${lang[@]}"
# 		do
#     # tokenize
# 		if [ "$SRC" = "$TRG" ]
# 		then
# 			continue
# 		fi
#
#    for prefix in test17.$SRC-$TRG
#     do
# 			 ./apply_bpe_merge.py -c $model_dir/all_morph.bpe < $dataset/$prefix.morph.$SRC > $data_dir/$prefix.merge.$SRC
# 		done
# done
# done
#
# echo tokenizer and normalisation
#  for SRC in "${lang[@]}"
#  	do
#    for TRG in "${lang[@]}"
#   		do
#      # tokenize
#   		if [ "$SRC" = "$TRG" ]
#   		then
#   			continue
#   		fi
#
#      for prefix in test17.$SRC-$TRG
#       do
# 				#  cat $dataset/$prefix.$SRC | \
# 				cat $data_dir/$prefix.merge.$SRC | \
#          $mosesdecoder/scripts/tokenizer/normalize-punctuation.perl -l $SRC | \
#          $mosesdecoder/scripts/tokenizer/tokenizer.perl -a -l $SRC > $data_dir/$prefix.tok.$SRC
# done
#  done
#  done
#
# #
# echo Aplly truecaser
#  for SRC in "${lang[@]}"
#  	do
#   for TRG in "${lang[@]}"
#  		do
#  		if [ "$SRC" = "$TRG" ]
#  		then
#  			continue
#  		fi
# 		echo $SRC-$TRG
#
#
#
#  		for prefix in test17.$SRC-$TRG
#      do
#  		  $mosesdecoder/scripts/recaser/truecase.perl -model $model_dir/truecase-model.$SRC < $data_dir/$prefix.tok.$SRC > $data_dir/$prefix.tc.$SRC
# 		done
#
# done
# done
#
# echo Fixing especial token
# sed -i -e 's/ # #/##/g' $data_dir/*tc*
# sed -i -e 's/§ § /§§/g' $data_dir/*tc*
#
echo Apply BPE
for SRC in "${lang[@]}"
	do
  for TRG in "${lang[@]}"
		do
    # tokenize
		if [ "$SRC" = "$TRG" ]
		then
			continue
		fi

    for prefix in test17.$SRC-$TRG
 	   do
			#  $subword_nmt/apply_bpe.py -c $model_dir/all.bpe < $data_dir/$prefix.tc.$SRC > $data_dir/$prefix.bpe.$SRC
			 $subword_nmt/apply_bpe.py -c $model_dir/allsrc.bpe < $dataset/$prefix.tc.$SRC > $data_dir/$prefix.bpe.$SRC


			#  cp $data_dir/$prefix.bpe.$SRC $data_dir/test17.$TRG-$SRC.bpe.$SRC
			#  sed -i -e 's/^......//' $data_dir/test17.$TRG-$SRC.bpe.$SRC
 		done
done
done
