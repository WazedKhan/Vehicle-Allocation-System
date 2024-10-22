from typing import List


def convert_objectids_to_strings(documents: List):
    """Convert ObjectId fields in a list of documents to strings."""
    for document in documents:
        if "_id" in document:
            document["_id"] = str(document["_id"])
    return documents
