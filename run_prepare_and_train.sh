#!/bin/bash

set -euxo pipefail

model_name=$1

if [ -z "$model_name" ]; then
  echo "Model name was not set."
  exit
fi

data_path="/home/ubuntu/data/melgan_${model_name}/"
existing_checkpoint="/home/ubuntu/data/melgan_checkpoint.pt"

# use venv context
source python/bin/activate

python preprocess.py \
  --config=config/default.yaml \
  --data_path="${data_path}"

python trainer.py \
  --config=config/default.yaml \
  --checkpoint_path="${existing_checkpoint}" \
  --name="melgan_${model_name}"

