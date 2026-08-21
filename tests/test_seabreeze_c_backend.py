"""smoke tests for the compiled seabreeze_c_backend extension module"""

import pytest

import seabreeze_c_backend


def test_backend_name():
    assert seabreeze_c_backend.__seabreeze_backend__ == "cseabreeze"


def test_all_exports_available():
    for name in seabreeze_c_backend.__all__:
        assert hasattr(seabreeze_c_backend, name), name


def test_api_list_devices():
    api = seabreeze_c_backend.SeaBreezeAPI()
    try:
        assert isinstance(api.list_devices(), list)
    finally:
        api.shutdown()


def test_error_is_exception():
    assert issubclass(seabreeze_c_backend.SeaBreezeError, Exception)
    with pytest.raises(seabreeze_c_backend.SeaBreezeError):
        raise seabreeze_c_backend.SeaBreezeError("test")
