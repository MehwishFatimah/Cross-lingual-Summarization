# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree. An additional grant of patent rights
# can be found in the PATENTS file in the same directory.


class FairseqTask(object):
    """
    A Task defines the data format, stores shared state (e.g., dictionaries) and
    provides helpers for building the model/criterion and calculating the loss.
    """

    @staticmethod
    def add_args(parser):
        """Add task-specific arguments to the parser."""
        pass

    def __init__(self, args):
        self.args = args
        self.datasets = {}

    @classmethod
    def setup_task(cls, args, **kwargs):
        raise NotImplementedError

    def load_dataset(self, split, combine=False):
        raise NotImplementedError

    def dataset(self, split):
        """Return a dataset split."""
        from fairseq.data import FairseqDataset
        if split not in self.datasets:
            raise KeyError('Dataset not loaded: ' + split)
        if not isinstance(self.datasets[split], FairseqDataset):
            raise TypeError('Datasets are expected to be of type FairseqDataset')
        return self.datasets[split]

    def build_model(self, args, teacher=False):
        from fairseq import models
        return models.build_model(args, self, teacher)

    def build_criterion(self, args):
        from fairseq import criterions
        return criterions.build_criterion(args, self)

    def get_loss(self, model, criterion, sample, teacher_model, eval):
        return criterion(model, sample, teacher_model, eval)

    @property
    def source_dictionary(self):
        raise NotImplementedError

    @property
    def target_dictionary(self):
        raise NotImplementedError
