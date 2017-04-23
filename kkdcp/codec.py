"""Encode/Decode ASN.1 requests"""

from pyasn1.codec.der import decoder, encoder
from pyasn1 import error
from kkdcp import model


class ParserError(Exception):
    """Custom parser error class"""
    pass


class KkdcpRequest:
    def __init__(self, message, domain):
        self.message = message
        self.domain = domain


def decode(data: bytes) -> KkdcpRequest:
    """Decode a KDC-PROXY-MESSAGE"""
    try:
        req, err = decoder.decode(data, asn1Spec=model.KdcProxyMessage())
    except error.PyAsn1Error:
        raise ParserError("Invalid request")

    if err:
        raise ParserError("Invalid request")

    message = req.getComponentByName('kerb-message').asOctets()
    domain = req.getComponentByName('target-domain').asOctets()

    # TODO: Check if the request is valid here

    return KkdcpRequest(message, domain)


def encode(data: bytes) -> bytes:
    """Encode a KDC-PROXY-MESSAGE"""
    msg = model.KdcProxyMessage()
    msg.setComponentByName('kerb-message', data)
    return encoder.encode(msg)
