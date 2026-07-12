from pathlib import Path

from config.settings import Settings


def test_ensure_directories_honors_configured_paths(tmp_path):
    original_database = Settings.DATABASE_PATH
    original_chroma = Settings.CHROMA_DB_PATH
    original_exports = Settings.EXPORTS_DIR

    try:
        Settings.DATABASE_PATH = str(tmp_path / "db" / "library.sqlite3")
        Settings.CHROMA_DB_PATH = str(tmp_path / "indexes" / "chroma")
        Settings.EXPORTS_DIR = tmp_path / "generated" / "reports"

        Settings.ensure_directories()

        assert Path(Settings.DATABASE_PATH).parent.is_dir()
        assert Path(Settings.CHROMA_DB_PATH).is_dir()
        assert Path(Settings.EXPORTS_DIR).is_dir()
    finally:
        Settings.DATABASE_PATH = original_database
        Settings.CHROMA_DB_PATH = original_chroma
        Settings.EXPORTS_DIR = original_exports


def test_negative_session_timeout_is_rejected():
    original_timeout = Settings.SESSION_TIMEOUT_MINUTES
    try:
        Settings.SESSION_TIMEOUT_MINUTES = -1
        valid, error = Settings.validate_configuration()
        assert valid is False
        assert error == "SESSION_TIMEOUT_MINUTES cannot be negative"
    finally:
        Settings.SESSION_TIMEOUT_MINUTES = original_timeout
