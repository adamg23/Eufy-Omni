"""Base64 / length-prefixed protobuf helpers for Eufy data points.

A "novel" data point value is base64 of: varint(len) + protobuf message. A few data
points omit the length prefix; decode() tolerates both by trying the prefixed form
first and falling back to the raw bytes.
"""

from __future__ import annotations

import base64
from typing import TypeVar

from google.protobuf.message import DecodeError, Message

T = TypeVar("T", bound=Message)


def read_varint(data: bytes, pos: int = 0) -> tuple[int, int]:
    value = shift = 0
    while pos < len(data):
        b = data[pos]
        pos += 1
        value |= (b & 0x7F) << shift
        if not b & 0x80:
            return value, pos
        shift += 7
    raise ValueError("truncated varint")


def write_varint(n: int) -> bytes:
    if n < 0:
        raise ValueError("negative varint")
    out = bytearray()
    while n >= 0x80:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    out.append(n)
    return bytes(out)


def strip_length_prefix(data: bytes) -> bytes:
    """Return the message bytes if `data` is varint(len)+msg, else `data` unchanged."""
    if not data:
        return data
    try:
        length, pos = read_varint(data)
    except ValueError:
        return data
    if length == len(data) - pos:
        return data[pos:]
    return data


def decode(msg_type: type[T], b64: str) -> T:
    raw = base64.b64decode(b64)
    body = strip_length_prefix(raw)
    msg = msg_type()
    try:
        msg.ParseFromString(body)
        return msg
    except DecodeError:
        if body is raw:
            raise
        msg = msg_type()
        msg.ParseFromString(raw)
        return msg


def encode(msg: Message, length_prefix: bool = True) -> str:
    body = msg.SerializeToString()
    if length_prefix:
        body = write_varint(len(body)) + body
    return base64.b64encode(body).decode("ascii")
