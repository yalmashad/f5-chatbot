# Chat Document Guardrail Design

## Goal

Extend the Streamlit chat app so users can upload a PDF or DOCX document with a normal chat prompt, while the app transparently extracts document text and sends it to F5 Guardrail for inspection before model execution.

## User Experience

The app remains chat-first. Users attach a supported document near the chat input and type a prompt such as "summarize this document." The visible chat should show the user's prompt and attached filename, but it must not paste or expose the extracted document text.

If the document cannot be inspected safely, the assistant returns a normal chat error or blocked response. The user should not need to understand the extraction and guardrail pipeline.

## Supported Files

The first version supports:

- PDF files with selectable/extractable text.
- DOCX files.

Legacy DOC files, OCR for scanned PDFs, images, spreadsheets, and other formats are out of scope.

## Limits

The app fails closed when limits are exceeded:

- Maximum uploaded file size: 10 MB.
- Maximum extracted text size: 100,000 characters.

The app also fails closed when extraction returns empty text, because that usually means the PDF is scanned/image-only or the document has no inspectable content.

## Extraction

PDF text extraction uses `pypdf`. DOCX text extraction uses `python-docx`.

Extraction should be implemented behind focused helper functions so document validation and parsing can be tested without driving the Streamlit UI.

## Guardrail Flow

When a document is attached, the app builds an internal inspection payload containing:

- The document filename.
- The user's visible prompt.
- The extracted document text.

The extracted text is never appended to the visible user prompt.

Guardrail behavior by mode:

- Guardrail disabled: send the user prompt plus document context directly to the selected model.
- Out-of-band: scan the combined prompt and extracted document text before the model call. If cleared, call the model with the prompt plus document context, then scan the model response as the app does today.
- Inline: send the combined prompt and extracted document text to the F5 Guardrail Prompt API, because Inline mode uses Guardrail to produce the response directly.

If the guardrail blocks or the scan fails, the app must not call the model with the document content.

## Model Context

When the app calls a model after a document clears inspection, it should include the document as hidden context in the model messages. The model should be told that the document text is untrusted content and that the user's prompt is the task.

## Debugging

When `Show debug details` is enabled, the app may show extraction metadata such as filename, file type, file size, extracted character count, and guardrail JSON. Debug mode should not show the full extracted document text by default.

## Documentation

Update `README.md` with:

- New dependencies: `pypdf` and `python-docx`.
- Supported document types.
- Size and extracted text limits.
- Explanation that documents are parsed locally and extracted text is sent to Guardrail for inspection.

## Verification

Verification should include:

- Python syntax/import check.
- Focused helper tests or smoke checks for validation paths where practical.
- Manual Streamlit run if dependencies are available in the environment.
