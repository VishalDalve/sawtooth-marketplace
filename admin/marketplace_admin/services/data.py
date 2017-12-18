# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import re
import yaml
import logging
from argparse import ArgumentParser


LOGGER = logging.getLogger(__name__)
REF_REG_EX = re.compile('^\$REF=(.+)\[(.+):(.+)\]\.(.+)$')


def get_parser():
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-d', '--data',
                        help='The path to the YAML data file',
                        required=True)
    return parser


def load(path):
    return yaml.load(open(path, 'r'))


def swap_refs(resource, data):
    for key, value in resource.items():
        try:
            match = REF_REG_EX.fullmatch(value)
        except TypeError:
            continue

        if match is None:
            continue

        list_name = match.group(1)
        filter_key = match.group(2)
        filter_value = match.group(3)
        swap_key = match.group(4)

        try:
            swap_value = next(r[swap_key] for r in data[list_name]
                              if r[filter_key] == filter_value)
        except StopIteration:
            LOGGER.warn('Unable to find match for ref: %s', value)
            continue

        resource[key] = swap_value
