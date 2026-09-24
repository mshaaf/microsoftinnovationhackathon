from fastapi import Request
from python_multipart.multipart import MultipartParser, parse_options_header

MAX_FILE_SIZE = 10 * 1024 * 1024
VALID_TYPES = {
    "image/jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
    "image/png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    "application/pdf": lambda data: data.startswith(b"%PDF-"),
}


class UploadError(ValueError):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message


async def read_upload(request: Request) -> tuple[bytes, str]:
    kind, options = parse_options_header(request.headers.get("content-type", ""))
    boundary = options.get(b"boundary")
    if kind != b"multipart/form-data" or not boundary:
        raise UploadError(400, "invalid_input", "Send a letter file and language.")

    fields: dict[str, bytes] = {}
    headers: dict[bytes, bytes] = {}
    header_name = bytearray()
    header_value = bytearray()
    part = bytearray()
    current_name = ""
    filename = ""
    content_type = ""

    def on_part_begin():
        nonlocal headers, part, current_name, filename, content_type
        headers, part = {}, bytearray()
        current_name = filename = content_type = ""

    def on_header_field(data, start, end):
        header_name.extend(data[start:end])

    def on_header_value(data, start, end):
        header_value.extend(data[start:end])

    def on_header_end():
        headers[bytes(header_name).lower()] = bytes(header_value)
        header_name.clear()
        header_value.clear()

    def on_headers_finished():
        nonlocal current_name, filename, content_type
        disposition, params = parse_options_header(
            headers.get(b"content-disposition", b"")
        )
        if disposition != b"form-data":
            raise UploadError(400, "invalid_input", "Invalid upload form.")
        current_name = params.get(b"name", b"").decode("utf-8", errors="replace")
        filename = params.get(b"filename", b"").decode("utf-8", errors="replace")
        content_type = headers.get(b"content-type", b"").decode(
            "ascii", errors="replace"
        )
        if current_name == "file" and content_type not in VALID_TYPES:
            raise UploadError(415, "unsupported_file", "Use a JPEG, PNG, or PDF file.")

    def on_part_data(data, start, end):
        part.extend(data[start:end])
        if current_name == "file" and len(part) > MAX_FILE_SIZE:
            raise UploadError(413, "file_too_large", "Choose a file under 10 MB.")

    def on_part_end():
        if current_name in fields:
            raise UploadError(400, "invalid_input", "Send one letter file.")
        if current_name in {"file", "lang"}:
            fields[current_name] = bytes(part)
            if current_name == "file":
                fields["filename"] = filename.encode()
                fields["content_type"] = content_type.encode()

    parser = MultipartParser(
        boundary,
        {
            "on_part_begin": on_part_begin,
            "on_header_field": on_header_field,
            "on_header_value": on_header_value,
            "on_header_end": on_header_end,
            "on_headers_finished": on_headers_finished,
            "on_part_data": on_part_data,
            "on_part_end": on_part_end,
        },
    )
    total = 0
    try:
        async for chunk in request.stream():
            total += len(chunk)
            if total > MAX_FILE_SIZE + 65536:
                raise UploadError(413, "file_too_large", "Choose a file under 10 MB.")
            parser.write(chunk)
        parser.finalize()
    except UploadError:
        raise
    except ValueError as error:
        raise UploadError(400, "invalid_input", "Invalid upload form.") from error

    data = fields.get("file")
    if data is None or fields.get("lang") not in {b"en", b"es"}:
        raise UploadError(400, "invalid_input", "Send a letter file and language.")
    file_type = fields["content_type"].decode()
    if not VALID_TYPES[file_type](data):
        raise UploadError(415, "unsupported_file", "Use a JPEG, PNG, or PDF file.")
    return data, fields["filename"].decode(errors="replace")
