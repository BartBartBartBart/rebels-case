from transformers import pipeline
from abc import ABC, abstractmethod


class BaseClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> str:
        pass

    @abstractmethod
    def classify_batch(self, texts: list[str]) -> list[str]:
        pass


class ZeroShotClassifier(BaseClassifier):
    """
    A simple multi-lingual zero-shot text classifier from HuggingFace.

    Advantages:
    - Fast to load
    - Fast inference

    Disadvantages:
    - Pre-determined set of labels
    - Lower quality labels
    """

    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli",
            device=-1,  # cpu
        )

        self.candidate_labels = [
            "selected",
            "not selected",
            "invoice",
            "acceptance letter",
            "rejection letter",
            "contract",
            "report",
            "email",
            "resume",
            "legal",
            "technical",
            "financial",
            "miscellaneous",
        ]

    def classify(self, text: str) -> str:
        """
        Classify the given text into one of the candidate labels using
        a zero-shot classification model from HuggingFace.

        Args:
            text (str): The text to be labeled.
        Returns:
            str: The label for the text.
        """

        results = self.classifier(
            text, self.candidate_labels, hypothesis_template="Dit document is een {}."
        )

        return results["labels"][0]

    def classify_batch(self, texts: list[str]) -> list[str]:
        """
        Classify a batch of texts in one pass.

        Args:
            texts (list(str)): A list of texts to be labeled.
        Returns:
            list(str): A list containing the labels for the texts.
        """

        results = self.classifier(
            texts, self.candidate_labels, hypothesis_template="Dit document is een {}."
        )

        return [r["labels"][0] for r in results]


class Phi4MiniClassifier(BaseClassifier):
    """
    Uses the Phi-4-mini-instruct LLM from Huggingface to classify documents.

    Advantages:
    - No pre-determined set of labels (flexibility)
    - Generally accurate labels

    Disadvantages:
    - Requires downloading model checkpoints locally (6GB)
    - Slower inference
    """

    def __init__(self):
        self.model = pipeline(
            "text-generation",
            model="microsoft/Phi-4-mini-instruct",
            device=-1,  # cpu
            trust_remote_code=True,
        )

    def classify(self, text: str) -> str:
        """
        Given a text, do a forward pass and obtain labels.

        Args:
            texts (str): The text to be classified.
        Returns:
            str: The generated label.
        """

        # Create prompt
        message = [
            {
                "role": "system",
                "content": "You are a helpful assistant for classifying documents.",
            },
            {
                "role": "user",
                "content": (
                    f"Answer with only the label in english.\n\n" f"Document:\n{text}"
                ),
            },
        ]

        # Settings
        generation_args = {
            "max_new_tokens": 20,
            "return_full_text": False,
            "temperature": 0,
            "do_sample": False,
            "batch_size": 1,
        }

        # Get response
        response = self.model(message, **generation_args)
        return response[0]["generated_text"].strip()

    def classify_batch(self, texts: list[str]) -> list[str]:
        """
        Given a list of texts, do a forward pass and obtain
        labels.

        Args:
            texts (list(str)): A list containing the texts to be labelled.
        Returns:
            list(str): A list containing labels for the texts.
        """

        # Create prompt
        messages = [
            [
                {
                    "role": "system",
                    "content": "You are a helpful assistant for classifying documents.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Answer with only the label in english.\n\n"
                        f"Document:\n{text}"
                    ),
                },
            ]
            for text in texts
        ]

        # Settings
        generation_args = {
            "max_new_tokens": 50,
            "return_full_text": False,
            "temperature": 0,
            "do_sample": False,
            "batch_size": 8,
        }

        # Get response
        response = self.model(messages, **generation_args)

        return [r[0]["generated_text"].strip() for r in response]


def get_classifier(type: str) -> BaseClassifier:
    """
    Helper function to load the correct classifier.

    Args:
        type (str): The classifier type to load. Can be
        "zero-shot" or "phi4".
    Returns:
        BaseClassifier: The selected classifier.
    """

    if type == "zero-shot":
        return ZeroShotClassifier()
    elif type == "phi4":
        return Phi4MiniClassifier()
    else:
        raise ValueError(
            f"{type} is not a valid classifier."
            f"Possible classifiers: zero-shot, phi4 (Received {type})."
        )
