import pytest

from services.classifier import get_classifier


def test_zero_shot_classifier():
    """
    Validates the classification of the zero-shot classifier.

    Args:
        None
    Returns:
        None
    Raises:
        AssertionError: If any of the .txt files is labeled wrongly.
    """

    classifier = get_classifier("zero-shot")

    sample_text = "Dit bestand is een contract in het Nederlands."
    label = classifier.classify(sample_text)

    assert label == "contract"

    sample_text = "This file is a report in English."
    label = classifier.classify(sample_text)

    assert label == "report"


@pytest.mark.skip(reason=("The model download slows down testing significantly."))
def test_phi4_classifier():
    """
    Validates the classification of the Phi-4 classifier.

    Args:
        None
    Returns:
        None
    Raises:
        AssertionError: If the labels do not contain the expected keywords.
    """

    classifier = get_classifier("phi4")

    sample_text = "Dit bestand is een contract in het Nederlands."
    label = classifier.classify(sample_text)

    assert "contract" in label.lower()

    sample_text = "This file is a report in English."
    label = classifier.classify(sample_text)

    assert "report" in label.lower()


def test_gemini_classifier():
    """
    Validates the classification of the Gemini classifier.

    Args:
        None
    Returns:
        None
    Raises:
        AssertionError: If the labels do not contain the expected keywords.
    """

    classifier = get_classifier("gemini")

    sample_text = "Dit bestand is een contract in het Nederlands."
    label = classifier.classify(sample_text)

    assert "contract" in label.lower()

    sample_text = "This file is a report in English."
    label = classifier.classify(sample_text)

    assert "report" in label.lower()


def test_invalid_classifier():
    """
    Validates that an invalid classifier type raises a ValueError.

    Args:
        None
    Returns:
        None
    Raises:
        ValueError: If an invalid classifier type is provided.
    """

    with pytest.raises(ValueError):
        get_classifier("some-other-model")
