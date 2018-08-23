
declare -a lang=("de" "en" "it" "nl" "ro")
# declare -a lang=("de" "en" "it")

# path to subword segmentation scripts: https://github.com/rsennrich/subword-nmt
subword_nmt=../../subword-nmt

# path to nematus ( https://www.github.com/rsennrich/nematus )
nematus=../../nematus

# path to moses decoder: https://github.com/moses-smt/mosesdecoder
mosesdecoder=../../mosesdecoder

data_dir=./data/morph64k32
# path to the datasets
dataset=./out_dir

model_dir=./model/morph64k32

# number of merge operations. Network vocabulary should be slightly larger (to include characters),
# or smaller if the operations are learned on the joint vocabulary
bpe_operations=32000
bpe_merge_operations=128000

echo Morph segmentation
# apply suffix and prefix segmentation
for SRC in "${lang[@]}"
	do
  for TRG in "${lang[@]}"
		do
		if [ "$SRC" = "$TRG" ]
		then
			continue
		fi
		echo $SRC-$TRG
  #  for prefix in train.$SRC-$TRG dev.$SRC-$TRG test.$SRC-$TRG
 #    do
#			 ./morphoSegmenter.py $SRC $dataset/$prefix.$SRC $data_dir/$prefix.morph.$SRC
#			 ./morphoSegmenter.py $TRG $dataset/$prefix.$TRG $data_dir/$prefix.morph.$TRG
 #		done
done
done
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
#    for prefix in train.$SRC-$TRG dev.$SRC-$TRG test.$SRC-$TRG
#     do
# 			 ./apply_bpe_merge.py -c $model_dir/all_morph.bpe < ./data/morph/$prefix.morph.$SRC > $data_dir/$prefix.merge.$SRC
# 			 ./apply_bpe_merge.py -c $model_dir/all_morph.bpe < ./data/morph/$prefix.morph.$TRG > $data_dir/$prefix.merge.$TRG
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
#      for prefix in train.$SRC-$TRG dev.$SRC-$TRG test.$SRC-$TRG
#       do
#         if [ "$SRC" = "ro" ]
#         then
#           cat $data_dir/$prefix.merge.$SRC | \
#           $mosesdecoder/scripts/tokenizer/normalize-punctuation.perl -l $SRC | \
#          #  ../preprocess/normalise-romanian.py | \
#          #  ../preprocess/remove-diacritics.py | \
#           $mosesdecoder/scripts/tokenizer/tokenizer.perl -a -l $SRC > $data_dir/$prefix.tok.$SRC
#        else
#          cat $data_dir/$prefix.merge.$SRC | \
#          $mosesdecoder/scripts/tokenizer/normalize-punctuation.perl -l $SRC | \
#          $mosesdecoder/scripts/tokenizer/tokenizer.perl -a -l $SRC > $data_dir/$prefix.tok.$SRC
#        fi
#
#        if [ "$TRG" = "ro" ]
#        then
#          cat $data_dir/$prefix.merge.$TRG | \
#          $mosesdecoder/scripts/tokenizer/normalize-punctuation.perl -l $TRG | \
#          # ../preprocess/normalise-romanian.py | \
#          # ../preprocess/remove-diacritics.py | \
#          $mosesdecoder/scripts/tokenizer/tokenizer.perl -a -l $TRG > $data_dir/$prefix.tok.$TRG
#       else
#         cat $data_dir/$prefix.merge.$TRG | \
#         $mosesdecoder/scripts/tokenizer/normalize-punctuation.perl -l $TRG | \
#         $mosesdecoder/scripts/tokenizer/tokenizer.perl -a -l $TRG > $data_dir/$prefix.tok.$TRG
#       fi
#       done
#
#  #     clean empty and long sentences, and sentences with high source-target ratio (training corpus only)
#   		$mosesdecoder/scripts/training/clean-corpus-n.perl $data_dir/train.$SRC-$TRG.tok $SRC $TRG $data_dir/train.$SRC-$TRG.tok.clean 1 80
#  done
#  done
#
#
#  echo Train one truecaser
#  for lang in "${lang[@]}"
#  do
#  		cat $data_dir/*.clean.$lang > $data_dir/tmp.$lang #NOTE is there a way to avoid saving this file?
#      $mosesdecoder/scripts/recaser/train-truecaser.perl -corpus $data_dir/tmp.$lang -model $model_dir/truecase-model.$lang
#  		rm $data_dir/tmp.$lang
#  done

#
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
#     for prefix in train.$SRC-$TRG
#      do
#  		  $mosesdecoder/scripts/recaser/truecase.perl -model $model_dir/truecase-model.$SRC < $data_dir/$prefix.tok.clean.$SRC > $data_dir/$prefix.tc.$SRC
#  		  $mosesdecoder/scripts/recaser/truecase.perl -model $model_dir/truecase-model.$TRG < $data_dir/$prefix.tok.clean.$TRG > $data_dir/$prefix.tc.$TRG
#  		done
#
#  		for prefix in dev.$SRC-$TRG test.$SRC-$TRG
#      do
#  		  $mosesdecoder/scripts/recaser/truecase.perl -model $model_dir/truecase-model.$SRC < $data_dir/$prefix.tok.$SRC > $data_dir/$prefix.tc.$SRC
# 			$mosesdecoder/scripts/recaser/truecase.perl -model $model_dir/truecase-model.$TRG < $data_dir/$prefix.tok.$TRG > $data_dir/$prefix.tc.$TRG
# 		done
#
# done
# done
#
# # #rm $data_dir/*.tok*
#
# echo Fixing especial token
# sed -i -e 's/ # #/##/g' $data_dir/*tc*
# sed -i -e 's/§ § /§§/g' $data_dir/*tc*

# echo Train BPE
#
#  cat $data_dir/*.tc.* | $subword_nmt/learn_bpe.py -s $bpe_operations > $model_dir/all.bpe

# echo Apply BPE
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
#     for prefix in dev.$SRC-$TRG test.$SRC-$TRG train.$SRC-$TRG
#  	   do
# 			 $subword_nmt/apply_bpe.py -c $model_dir/all.bpe < $data_dir/$prefix.tc.$SRC > $data_dir/$prefix.bpe.$SRC
# 			 $subword_nmt/apply_bpe.py -c $model_dir/all.bpe < $data_dir/$prefix.tc.$TRG > $data_dir/$prefix.bpe.$TRG
#  		done
# done
# done
#
# # rm data/*.tc.*
# #
# echo build network dictionary
# cat $data_dir/*.bpe.* > $data_dir/sentences.bpe
# $nematus/data/build_dictionary.py $data_dir/sentences.bpe
#
# rm $data_dir/sentences.bpe
