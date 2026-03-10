import os
from pathlib import Path
from docx import Document


def ingest_docs(folder_path: str):
    """
    Ingest documents from the specified folder path and store
    their metadata in the database. This function reads all .docx
    files in the given folder, extracts their metadata, and saves
    it to the database.

    Args:
        folder_path (str): The path to the folder containing
        the documents to be ingested.
    """

    print(f"Ingesting documents from folder: {folder_path}")

    for file in Path(folder_path).glob("*.docx"):
        if file.is_file():
            doc = Document(file)
            props = doc.core_properties
            metadata = {
                "filename": file.name,
                "author": props.author,
                "created": props.created,
                "modified": props.modified,
                "file_type": file.suffix,
                "file_size": file.stat().st_size,
                "paragraph_count": len(doc.paragraphs),
                "table_count": len(doc.tables),
                "section_count": len(doc.sections),
                "word_count": sum(len(p.text.split()) for p in doc.paragraphs),
                "table_data": [],
            }

            # Extract table data
            for table in doc.tables:
                table_content = []
                for row in table.rows:
                    table_content.append([cell.text for cell in row.cells])
                metadata["table_data"].append(table_content)

            for k, v in metadata.items():
                print(f"{k}: {v}")

            # Contents
            print("Document content:")
            for paragraph in doc.paragraphs:
                print(paragraph.text)


if __name__ == "__main__":
    # For testing
    for folder in [
        "Company_A/Project 1",
        "Company_B/Project 2",
        "Company_B/Project 3",
        "Company_C/Project 4",
        "Company_C/Project 5",
    ]:
        print("\n" + "=" * 50 + "\n")
        test_folder = f"{os.getcwd()}/../data/{folder}"
        ingest_docs(test_folder)
