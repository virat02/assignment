import pytest

@pytest.mark.parametrize(
    "key, status_code, val", [
        ("color", 200, "blue"),
        ("test", 200, "test"),
        ("test1", 200, "test1"),
        ("test2", 200, "test2"),
        ("test3", 200, "test3"),
        ("test4", 200, "test4"),
        ("test5", 200, "test5 not found!")
    ]
)
def test_get_key(client, setup_test_data, key, status_code, val):
    resp = client.get(f'/get/{key}')
    assert resp.status_code == status_code

    resp_data = resp.data.decode()
    assert resp_data == val