#!/bin/bash

set -euxo pipefail

model_name=$1

if [ -z "$model_name" ]; then
  echo "Model name was not set."
  exit
fi

data_path="/home/ubuntu/data/melgan_${model_name}/"
existing_checkpoint="/home/ubuntu/data/melgan_checkpoint.pt"

if [ ! -d "$data_path" ]; then
  echo "Training directory does not exist: ${data_path}"
  exit
fi

if [ ! -f "$existing_checkpoint" ]; then
  echo "Previous checkpoint does not exist: ${existing_checkpoint}"
  exit
fi

# use venv context
source python/bin/activate

python preprocess.py \
  --config=config/default.yaml \
  --data_path="${data_path}"

python trainer.py \
  --config=config/default.yaml \
  --checkpoint_path="${existing_checkpoint}" \
  --name="melgan_${model_name}"

