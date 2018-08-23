#!/bin/sh

echo "The script you are running has basename `basename $0`, dirname `dirname $0`"
echo "The present working directory is `pwd`"

mydir=`dirname $0`
data=data/allsrc
datatrg=data/allsrc642
model=models/bi_en_it_target
SRC=en
TRG=it
cd $mydir
. ./vars

CUDA_VISIBLE_DEVICES=0 python $nematus/nmt.py \
    --model $working_dir/$model/model.npz \
    --datasets $working_dir/$data/train.$SRC-$TRG.bpe2.$SRC \
               $working_dir/$datatrg/train.$SRC-$TRG.bpe2.$TRG \
    --valid_datasets $working_dir/$data/dev.$SRC-$TRG.bpe.$SRC \
                     $working_dir/$datatrg/dev.$SRC-$TRG.bpe.$TRG \
    --dictionaries $working_dir/$data/$SRC-$TRG.bpe.src.json \
                   $working_dir/$datatrg/$SRC-$TRG.bpe.trg.json \
    --dim_word 512 \
    --dim 1024 \
    --lrate 0.0001 \
    --optimizer adam \
    --maxlen 50 \
    --batch_size 80 \
    --valid_batch_size 80 \
    --validFreq 10000 \
    --dispFreq 1000 \
    --saveFreq 30000 \
    --sampleFreq 10000 \
    --tie_decoder_embeddings \
    --layer_normalisation \
    --use_dropout \
    --dropout_source 0.1 \
    --dropout_target 0.1 \
    --dropout_embedding 0.2 \
    --dropout_hidden 0.2

