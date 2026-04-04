import logging

from app.config import settings
from app.logging_config import configure_logging


def test_request_logs_are_emitted(client, caplog):
    with caplog.at_level(logging.INFO, logger="app.requests"):
        response = client.get("/health")

    assert response.status_code == 200
    assert any(
        'method=GET path="/health" status=200' in record.getMessage()
        for record in caplog.records
    )


def test_logs_are_written_to_file(tmp_path):
    original_log_dir = settings.LOG_DIR
    original_log_file = settings.LOG_FILE

    try:
        settings.LOG_DIR = str(tmp_path)
        settings.LOG_FILE = "test.log"

        log_file = configure_logging()
        logging.getLogger("app.tests").info("file logging smoke test")

        for handler in logging.getLogger().handlers:
            handler.flush()

        assert log_file.exists()
        assert "file logging smoke test" in log_file.read_text()
    finally:
        settings.LOG_DIR = original_log_dir
        settings.LOG_FILE = original_log_file
        configure_logging()
