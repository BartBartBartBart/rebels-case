from pathlib import Path

from docx import Document
from fastapi.testclient import TestClient


class TestFolderInsights:
    """
    Test class for the folder/insights API endpoint.
    """

    def test_returns_200(self, client: TestClient, tmp_path: Path) -> None:
        """
        Checks whether the endpoint returns OK when called with correct path.

        Args:
            client (TestClient): Test client for making HTTP requests to the
                application.
            tmp_path (Path): Temporary directory path fixture provided by
                pytest.
        Returns:
            None
        Raises:
            AssertionError: If the response status code is not 200.
        """

        response = client.post(f"/folder/insights?folder_path={tmp_path}")
        assert response.status_code == 200

    def test_empty_folder_returns_zero_documents(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        """
        Checks whether endpoint handles empty directories correctly.

        Args:
            client (TestClient): Test client for making HTTP requests to the
                application.
            tmp_path (Path): Temporary directory path fixture provided by pytest.
        Returns:
            None
        Raises:
            AssertionError: If num_files is not 0 or insights is not empty.
        """

        response = client.post(f"/folder/insights?folder_path={tmp_path}")
        data = response.json()
        assert data["num_files"] == 0
        assert data["insights"] == {}

    def test_counts_documents_correctly(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        """
        Checks whether the endpoint correctly counts the number of documents in a
        folder.

        Args:
            client (TestClient): Test client for making HTTP requests to the
                application.
            tmp_path (Path): Temporary directory path fixture provided by pytest.
        Returns:
            None
        Raises:
            AssertionError: If the number of files is not counted correctly.
        """

        (tmp_path / "file1.txt").write_text("hello world")
        (tmp_path / "file2.txt").write_text("another document")
        docx_file = tmp_path / "file3.docx"
        doc = Document()
        doc.add_paragraph("This is a test document")
        doc.save(docx_file)

        response = client.post(f"/folder/insights?folder_path={tmp_path}")
        data = response.json()
        assert data["num_files"] == 3

    def test_folder_path_with_spaces(self, client: TestClient, tmp_path: Path) -> None:
        """
        Checks that folder paths containing spaces are handled correctly.

        Args:
            client (TestClient): Test client for making HTTP requests to the
                application.
            tmp_path (Path): Temporary directory path fixture provided by
                pytest.
        Returns:
            None
        Raises:
            AssertionError: If the endpoint fails to resolve a folder containing
                spaces.
        """

        folder_with_space = tmp_path / "Project 6"
        folder_with_space.mkdir()
        (folder_with_space / "test.txt").write_text("hello world")

        response = client.post(
            "/folder/insights",
            params={"folder_path": str(folder_with_space)},
        )
        assert response.status_code == 200
        assert response.json()["num_files"] == 1

    def test_returns_correct_metadata_fields(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        """
        Checks whether the endpoint returns the correct metadata fields for a
        document.

        Args:
            client (TestClient): Test client for making HTTP requests to the
                application.
            tmp_path (Path): Temporary directory path fixture provided by
                pytest.
        Returns:
            None
        Raises:
            AssertionError: If any required metadata fields are missing.
        """

        (tmp_path / "test.txt").write_text("hello world")

        response = client.post(f"/folder/insights?folder_path={tmp_path}")
        doc = response.json()["insights"]["test.txt"]

        assert "filename" in doc
        assert "file_type" in doc
        assert "file_size" in doc
        assert "word_count" in doc
        assert "language" in doc

    def test_invalid_path_returns_400(self, client: TestClient) -> None:
        """
        Checks whether the endpoint returns a 400 status code for an invalid
        folder path.

        Args:
            client (TestClient): Test client for making HTTP requests to the
                application.
        Returns:
            None
        Raises:
            AssertionError: If the response status code is not 400.
        """

        response = client.post("/folder/insights?folder_path=./nonexistent_folder")
        assert response.status_code == 400

    def test_file_as_folder_path(self, client: TestClient, tmp_path: Path) -> None:
        """
        Checks whether the endpoint returns a 400 status code when a file path is
        provided instead of a folder path.

        Args:
            client (TestClient): Test client for making HTTP requests to the
                application.
            tmp_path (Path): Temporary directory path fixture provided by pytest.
        Returns:
            None
        Raises:
            AssertionError: If the response status code is not 400.
        """

        (tmp_path / "doc1.txt").write_text("quarterly financial report")
        response = client.post(f"/folder/insights?folder_path=./{tmp_path}/doc1.txt")
        assert response.status_code == 400

    def test_upsert_doesnt_duplicate(self, client: TestClient, tmp_path: Path) -> None:
        """
        Checks whether calling the endpoint multiple times does not duplicate
        document entries.

        Args:
            client (TestClient): Test client for making HTTP requests to the
                application.
            tmp_path (Path): Temporary directory path fixture provided by
                pytest.
        Returns:
            None
        Raises:
            AssertionError: If the number of files is duplicated after multiple
                calls.
        """

        (tmp_path / "test.txt").write_text("hello world")

        # call twice
        client.post(f"/folder/insights?folder_path={tmp_path}")
        client.post(f"/folder/insights?folder_path={tmp_path}")

        response = client.post(f"/folder/insights?folder_path={tmp_path}")
        assert response.json()["num_files"] == 1  # not 2
