import pytest
from unittest.mock import Mock
from app.process_apk import APKProcessor

@pytest.fixture
def mock_redis_client(mocker):
    mock = mocker.Mock()
    mock.get_from_queue.return_value = ("apk_queue", b"/path/to/mock.apk")
    return mock

@pytest.fixture
def mock_mobsf_client(mocker):
    mock = mocker.Mock()
    mock.upload_apk.return_value = {
        "analyzer": "static_analyzer",
        "status": "success",
        "hash": "mockhashvalue",
        "scan_type": "apk",
        "file_name": "mock.apk"
    }
    mock.scan_apk.return_value = {
        "scan_results": "mock_scan_results"
    }
    return mock

@pytest.fixture
def apk_processor(mock_redis_client, mock_mobsf_client):
    return APKProcessor(
        redis_client=mock_redis_client,
        mobsf_client=mock_mobsf_client,
        queue_name="apk_queue",
        results_key_base="apk_results"
    )

def test_process_apk(apk_processor, mock_redis_client, mock_mobsf_client):
    apk_processor.process_apk("/path/to/mock.apk")
    
    mock_mobsf_client.upload_apk.assert_called_once_with("/path/to/mock.apk")
    
    mock_mobsf_client.scan_apk.assert_called_once_with("mockhashvalue")
    
    expected_results_key = "apk_results:mock.apk"
    mock_redis_client.save_results.assert_called_once_with(expected_results_key, {"scan_results": "mock_scan_results"})

def test_run(apk_processor, mock_redis_client):
    apk_processor.run()
    
    mock_redis_client.get_from_queue.assert_called_once_with("apk_queue")
    
    mock_redis_client.get_from_queue.return_value = ("apk_queue", b"/path/to/mock.apk")
    assert mock_redis_client.get_from_queue.called
