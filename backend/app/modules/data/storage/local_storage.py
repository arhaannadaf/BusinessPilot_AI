
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class LocalStorage:
    def __init__(self,
        storage_dir: str = "storage/uploads",
        max_bytes: int = 10 * 1024 * 1024
        ):
        self.storage_dir = Path(storage_dir).resolve()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes

    async def save(self, file: UploadFile) -> tuple[str, int]:
        if not file.filename:
            raise ValueError("Uploaded file must have a filename.")

        # Store using a generated name, not the user-supplied path.
        suffix = Path(file.filename).suffix.lower()
        stored_name = f"{uuid4().hex}{suffix}"
        destination = self.storage_dir / stored_name

        size = 0

        try:
            with destination.open("wb") as output:
                while chunk := await file.read(1024 * 1024):
                    total_bytes += len(chunk)

                    if total_bytes > self.max_bytes:
                        raise ValueError(
                            "Uploaded file exceeds the 10 MB size limit."
                        )

                    destination.write(chunk)
        except Exception:
            destination.unlink(missing_ok=True)
            raise
        finally:
            await file.close()

        return str(destination), size


    async def save_upload(
        self,
        file: UploadFile,
    ) -> tuple[str, int]:
        original_name = Path(file.filename or "").name

        if not original_name:
            raise ValueError("Uploaded file must have a filename.")

        if Path(original_name).suffix.lower() != ".csv":
            raise ValueError("Only CSV files are supported.")

        stored_name = f"{uuid4().hex}.csv"
        file_path = self.storage_dir / stored_name
        total_bytes = 0

        try:
            with file_path.open("xb") as destination:
                while chunk := await file.read(1024 * 1024):
                    total_bytes += len(chunk)

                    if total_bytes > self.max_bytes:
                        raise ValueError(
                            "Uploaded file exceeds the 10 MB size limit."
                        )

                    destination.write(chunk)

        except Exception:
            file_path.unlink(missing_ok=True)
            raise

        finally:
            await file.close()

        return str(file_path), total_bytes
