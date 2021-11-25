from flask.testing import FlaskClient
import pytest

@pytest.mark.parametrize(
    "key, status_code, val", [
        ("color", 200, "blue"),
        ("test", 200, "test"),
        ("test1", 200, "test1"),
        ("test2", 200, "test2"),
        ("test3", 200, "test3"),
        ("test4", 200, "test4"),
        ("test5", 200, "1"),
        ("test6", 200, "test6 not found!"),
    ]
)
def test_get_key(client: FlaskClient, key: str, status_code: int, val: str) -> str:
    resp = client.get(f'/get/{key}')
    assert resp.status_code == status_code

    resp_data = resp.data.decode()
    assert resp_data == val