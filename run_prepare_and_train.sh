#!/bin/bash

model_name=$1
data_path="/home/ubuntu/data/melgan_${model_name}/"
existing_checkpoint="/home/ubuntu/data/melgan_checkpoint.pt"

python preprocess.py \
  --config=config/default.yaml \
  --data_path="${data_path}"

python trainer.py \
  --config=config/default.yaml \
  --checkpoint_path="${existing_checkpoint}" \
  --name="melgan_${model_name}"


