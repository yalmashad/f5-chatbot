import pytest

from f5_chatbot import (
    MAX_DOCUMENT_FILE_BYTES,
    MAX_EXTRACTED_TEXT_CHARS,
    DocumentInspectionError,
    build_document_inspection_payload,
    build_document_model_messages,
    validate_document_upload,
)


class FakeUpload:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


def test_validate_document_upload_accepts_pdf_under_limit():
    uploaded = FakeUpload("report.pdf", MAX_DOCUMENT_FILE_BYTES)

    assert validate_document_upload(uploaded) == ".pdf"


def test_validate_document_upload_rejects_unsupported_extension():
    uploaded = FakeUpload("report.txt", 100)

    with pytest.raises(DocumentInspectionError, match="Only PDF and DOCX"):
        validate_document_upload(uploaded)


def test_validate_document_upload_rejects_oversized_file():
    uploaded = FakeUpload("report.pdf", MAX_DOCUMENT_FILE_BYTES + 1)

    with pytest.raises(DocumentInspectionError, match="10 MB"):
        validate_document_upload(uploaded)


def test_build_document_inspection_payload_rejects_empty_text():
    with pytest.raises(DocumentInspectionError, match="No inspectable text"):
        build_document_inspection_payload("Summarize this", "empty.pdf", "   ")


def test_build_document_inspection_payload_rejects_oversized_text():
    oversized_text = "a" * (MAX_EXTRACTED_TEXT_CHARS + 1)

    with pytest.raises(DocumentInspectionError, match="too large"):
        build_document_inspection_payload("Summarize this", "large.pdf", oversized_text)


def test_build_document_inspection_payload_combines_prompt_and_document_text():
    payload = build_document_inspection_payload(
        "Summarize this",
        "report.pdf",
        "Document body",
    )

    assert "User prompt:" in payload
    assert "Summarize this" in payload
    assert "Attached document: report.pdf" in payload
    assert "Document body" in payload


def test_build_document_model_messages_marks_document_as_untrusted_context():
    messages = build_document_model_messages(
        "Summarize this",
        "report.docx",
        "Document body",
    )

    assert messages[0]["role"] == "system"
    assert "untrusted document content" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    assert "report.docx" in messages[1]["content"]
    assert "Document body" in messages[1]["content"]
    assert "Summarize this" in messages[1]["content"]
