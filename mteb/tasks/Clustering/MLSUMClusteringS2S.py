import datasets
import numpy as np

from ...abstasks.AbsTaskClustering import AbsTaskClustering


class MLSUMClusteringS2S(AbsTaskClustering):
    @property
    def description(self):
        return {
            "name": "MLSUMClusteringS2S",
            "hf_hub_name": "mlsum",
            "description": (
                "Clustering of newspaper article titles from MLSUM dataset. Clustering of 10 sets on the newpaper article topics."
            ),
            "reference": "https://huggingface.co/datasets/mlsum",
            "type": "Clustering",
            "category": "s2s",
            "eval_splits": ["test"],
            "eval_langs": ["fr"],
            "main_score": "v_measure",
            "revision": "b5d54f8f3b61ae17845046286940f03c6bc79bc7",
        }

    def load_data(self, **kwargs):
        """
        Load dataset from HuggingFace hub and convert it to the standard format.
        """
        if self.data_loaded:
            return
        self.dataset = datasets.load_dataset(
            self.description["hf_hub_name"],
            "fr",
            split=self.description["eval_splits"][0],
            revision=self.description.get("revision", None),
        )
        self.dataset_transform()
        self.data_loaded = True

    def dataset_transform(self):
        """
        Convert to standard format
        """
        self.dataset = self.dataset.remove_columns("summary")
        self.dataset = self.dataset.remove_columns("text")
        self.dataset = self.dataset.remove_columns("url")
        self.dataset = self.dataset.remove_columns("date")
        titles = self.dataset["title"]
        topics = self.dataset["topic"]
        new_format = {
            "sentences": [split.tolist() for split in np.array_split(titles, 10)],
            "labels": [split.tolist() for split in np.array_split(topics, 10)],
        }
        self.dataset = {self.description["eval_splits"][0]: datasets.Dataset.from_dict(new_format)}
