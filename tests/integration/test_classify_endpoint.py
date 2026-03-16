from pathlib import Path

from fastapi.testclient import TestClient


class TestClassifyEndpoint:
    """
    Test class for the folder/classify API.
    """

    def test_returns_200(self, client: TestClient, tmp_path: Path) -> None:
        """
        Checks whether endpoint returns OK status.

        Args:
            client (TestClient): Test client for making HTTP requests to the app.
            tmp_path (Path): Temporary path fixture from pytest.
        Returns:
            None
        Raises:
            AssertionError: If response code is not 200.
        """
        (tmp_path / "invoice.txt").write_text(
            "Please pay the total amount of 500 euros by the end of the month"
        )

        response = client.post(f"/folder/classify?folder_path={tmp_path}")
        assert response.status_code == 200

    def test_folder_path_with_spaces(self, client: TestClient, tmp_path: Path) -> None:
        """
        Checks that folder paths containing spaces are handled correctly.

        Args:
            client (TestClient): Test client for making HTTP requests to the app.
            tmp_path (Path): Temporary path fixture from pytest.
        Returns:
            None
        Raises:
            AssertionError: If the endpoint fails to resolve a folder containing spaces.
        """

        folder_with_space = tmp_path / "Project 6"
        folder_with_space.mkdir()
        (folder_with_space / "doc.txt").write_text("financial report")

        response = client.post(
            "/folder/classify",
            params={"folder_path": str(folder_with_space)},
        )
        assert response.status_code == 200
        assert response.json()["classifications"]["doc.txt"] is not None

    def test_all_documents_get_labeled(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        """
        Checks whether all documents in the folder receive a classification label.

        Args:
            client (TestClient): Test client for making HTTP requests to the app.
            tmp_path (Path): Temporary path fixture from pytest.
        Returns:
            None
        Raises:
            AssertionError: If any document does not have a label.
        """

        (tmp_path / "doc1.txt").write_text("quarterly financial report")
        (tmp_path / "doc2.txt").write_text("employment contract terms")

        response = client.post(f"/folder/classify?folder_path={tmp_path}")

        data = response.json()
        print(label for doc, label in data["classifications"].items())
        assert all(label is not None for doc, label in data["classifications"].items())

    def test_already_classified_docs(self, client: TestClient, tmp_path: Path) -> None:
        """
        Checks whether already classified documents return the same label
        on subsequent calls.

        Args:
            client (TestClient): Test client for making HTTP requests to the app.
            tmp_path (Path): Temporary path fixture from pytest.
        Returns:
            None
        Raises:
            AssertionError: If the labels differ between calls.
        """

        (tmp_path / "doc.txt").write_text("financial report")

        first = client.post(f"/folder/classify?folder_path={tmp_path}")
        second = client.post(f"/folder/classify?folder_path={tmp_path}")

        assert (
            first.json()["classifications"]["doc.txt"]
            == second.json()["classifications"]["doc.txt"]
        )

    def test_empty_folder(self, client: TestClient, tmp_path: Path) -> None:
        """
        Checks whether an empty folder returns an empty classifications dictionary.

        Args:
            client (TestClient): Test client for making HTTP requests to the app.
            tmp_path (Path): Temporary path fixture from pytest.
        Returns:
            None
        Raises:
            AssertionError: If classifications is not empty.
        """

        response = client.post(f"/folder/classify?folder_path={tmp_path}")
        assert response.json()["classifications"] == {}

    def test_nonexistent_folder_path(self, client: TestClient) -> None:
        """
        Checks whether providing a nonexistent folder path returns a 400 status code.

        Args:
            client (TestClient): Test client for making HTTP requests to the app.
        Returns:
            None
        Raises:
            AssertionError: If the response status code is not 400.
        """

        response = client.post("/folder/classify?folder_path=./nonexistentfolder")
        assert response.status_code == 400

    def test_file_as_folder_path(self, client: TestClient, tmp_path: Path) -> None:
        """
        Checks whether providing a file path instead of a folder path returns
        a 400 status code.

        Args:
            client (TestClient): Test client for making HTTP requests to the app.
            tmp_path (Path): Temporary path fixture from pytest.
        Returns:
            None
        Raises:
            AssertionError: If the response status code is not 400.
        """

        (tmp_path / "doc1.txt").write_text("quarterly financial report")
        response = client.post(f"/folder/classify?folder_path=./{tmp_path}/doc1.txt")
        assert response.status_code == 400
