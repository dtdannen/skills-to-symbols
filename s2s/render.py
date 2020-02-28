from collections import defaultdict
from typing import List, Dict, Tuple

import numpy as np

from s2s.env import S2SEnv
from s2s.image import Image
from s2s.partitioned_option import PartitionedOption
from s2s.utils import show, exists, make_dir, make_path


def visualise_partitions(env: S2SEnv,
                         option_partitions: Dict[int, List[PartitionedOption]],
                         verbose=False) \
        -> Dict[int, Dict[int, Tuple[np.ndarray, List[Tuple[float, np.ndarray, np.ndarray]]]]]:
    """
    Visualise a set of partitions
    :param env: the domain
    :param option_partitions: a dictionary listing, for each option, a list of partitions
    :param verbose: the verbosity level
    :return: a mapping that stores for each option and partition, an image of the start and end states
    (with associated probabilities)
    """

    images = defaultdict(dict)
    for option, partitions in option_partitions.items():

        show("Visualising option {} with {} partition(s)".format(option, len(partitions)), verbose)

        for partition in partitions:
            start = Image.merge([env.render_state(state) for state in partition.states])
            effects = list()
            for probability, _, next_states, mask, in partition.effects():
                end = Image.merge([env.render_state(state) for state in next_states])
                effects.append((probability, mask, end))
            images[option][partition.partition] = (start, effects)
    return images


def save_visualised_partitions(directory: str,
                               visualised_partitions: Dict[
                                   int, Dict[int, Tuple[np.ndarray, List[Tuple[float, np.ndarray, np.ndarray]]]]],
                               verbose=False,
                               **kwargs) -> None:
    """
    Given visualised partitions, save them to file
    :param directory: the directory to save them to
    :param visualised_partitions: the set of partitions
    :param verbose: the verbosity level
    """
    option_descriptor = kwargs.get('option_descriptor',
                                   lambda option: 'Option-{}'.format(option))  # a function that describes the operator

    make_dir(directory)  # make directory if not exists
    for option, partitions in visualised_partitions.items():
        for partition, (start, effects) in partitions.items():
            show("Visualising option {}, partition {}".format(option, partition), verbose)
            filename = '{}-{}-init.bmp'.format(option_descriptor(option), partition)
            Image.save(start, make_path(directory, filename), mode='RGB')
            for i, (probability, masks, effect) in enumerate(effects):
                filename = '{}-{}-eff-{}-{}-{}.bmp'.format(option_descriptor(option), partition, i,
                                                           round(probability * 100), list(np.unique(masks)))
                Image.save(effect, make_path(directory, filename), mode='RGB')