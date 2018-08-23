#!/bin/sh

echo "The script you are running has basename `basename $0`, dirname `dirname $0`"
echo "The present working directory is `pwd`"

mydir=`dirname $0`
data=data/morph4k32
model=models/4k32
cd $mydir
. ./vars

CUDA_VISIBLE_DEVICES=1 python $nematus/nmt.py \
    --model $working_dir/$model/model.npz \
    --datasets $working_dir/$data/corpus.src \
               $working_dir/$data/corpus.trg \
    --valid_datasets $working_dir/$data/dev.src \
                     $working_dir/$data/dev.trg \
    --dictionaries $working_dir/$data/sentences.bpe.json \
                   $working_dir/$data/sentences.bpe.json \
    --reload latest_checkpoint \
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
    --dec_base_recurrence_transition_depth 8 \
    --enc_recurrence_transition_depth 4 \
    --use_dropout \
    --dropout_source 0.1 \
    --dropout_target 0.1 \
    --dropout_embedding 0.2 \
    --dropout_hidden 0.2
