#!/usr/bin/env python3

from ruamel.yaml import YAML
import argparse
import os
import socket

DEFAULT_CONFIG_FILE = 'config/default.yaml'

# Sometimes I train on my local 'halide' GPU worker,
# other times I rent instances from LambdaLabs.
DEFAULT_DATA_DIRECTORY_LOCAL = '/home/bt/datasets/'
DEFAULT_DATA_DIRECTORY_REMOTE = '/home/ubuntu/data/'

def read_yaml(filename):
  contents = None
  with open(filename) as f:
    contents = f.read()
  yaml = YAML(typ='rt')
  loaded = yaml.load_all(contents) # handle multi-doc YAML stream
  return list(loaded)

def write_yaml(filename, config_dict):
  yaml = YAML(typ='rt')
  with open(filename, 'w') as f:
    yaml.dump_all(config_dict, f)

def get_data_directory():
  hostname = socket.gethostname()
  if hostname == 'halide':
    return DEFAULT_DATA_DIRECTORY_LOCAL
  else:
    return DEFAULT_DATA_DIRECTORY_REMOTE

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--speaker_dir', type=str, required=True,
                      help='Directory name for speaker training data (dirname or absolute)')
  args = parser.parse_args()

  print('Speaker directory: {}'.format(args.speaker_dir))

  data_directory = get_data_directory()

  print('Data directory: {}'.format(data_directory))

  speaker_dir = 'melgan_{}'.format(args.speaker_dir)
  speaker_dir = os.path.join(data_directory, speaker_dir)

  training_directory = os.path.join(speaker_dir, 'training')
  validation_directory = os.path.join(speaker_dir, 'validation')

  print('Training directory: {}'.format(training_directory))
  print('Validation directory: {}'.format(validation_directory))

  # We read in a multi-doc YAML stream.
  # Only the first document needs adjustment.
  configs = read_yaml(DEFAULT_CONFIG_FILE)

  configs[0]['data']['train'] = training_directory
  configs[0]['data']['validation'] = validation_directory

  write_yaml(DEFAULT_CONFIG_FILE, configs)

if __name__ == '__main__':
  main()

