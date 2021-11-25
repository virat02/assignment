from socket import socket
import pytest

@pytest.mark.parametrize(
    "key, val", [
        ("$3\r\nfoo\r\n", "bar"),
        ("$4\r\nfoo1\r\n", "bar1"),
        ("$4\r\nfoo2\r\n", "bar2"),
        ("$4\r\nfoo3\r\n", "bar3"),
        ("$4\r\nfoo4\r\n", "bar4"),
        ("$4\r\nfoo5\r\n", "bar5"),
        ("$4\r\nfoo6\r\n", "foo6 not found!"),
        ("$4\r\foo6\r\n", "Invalid key requested")
    ]
)
def test_get_key(create_socket: socket, key: str, val: str):
    create_socket.sendall(f'{key}'.encode("utf-8"))

    resp_data = (create_socket.recv(32)).decode("utf-8")
    assert resp_data == val