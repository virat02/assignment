from socket import socket
import pytest

@pytest.mark.parametrize(
    "key, val", [
        ("*2\r\n$3\r\nget\r\n$3\r\nfoo\r\n", "bar"),
        ("*2\r\n$3\r\nget\r\n$4\r\nfoo1\r\n", "bar1"),
        ("*2\r\n$3\r\nget\r\n$4\r\nfoo2\r\n", "bar2"),
        ("*2\r\n$3\r\nget\r\n$4\r\nfoo3\r\n", "bar3"),
        ("*2\r\n$3\r\nget\r\n$4\r\nfoo4\r\n", "bar4"),
        ("*2\r\n$3\r\nget\r\n$4\r\nfoo5\r\n", "bar5"),
        ("*2\r\n$3\r\nget\r\n$4\r\nfoo6\r\n", "foo6 not found!"),
        ("*2\r\n$3\r\nget\r\n$4\r\foo6\r\n", "Invalid key requested"),
        ("*3\r\n$3\r\nset\r\n$4\r\nfoo7\r\n$4\r\nbar7\r\n", "Not a GET request"),
    ]
)
def test_get_key(create_socket: socket, key: str, val: str):
    create_socket.sendall(f'{key}'.encode("utf-8"))

    resp_data = (create_socket.recv(32)).decode("utf-8")
    assert resp_data == val