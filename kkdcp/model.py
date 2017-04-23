"""ASN.1 message definitions"""

from pyasn1.type import char, namedtype, tag, univ


class KerbMessage(univ.OctetString):
    tagSet = univ.OctetString.tagSet.tagExplicitly(
        tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0)
    )


class TargetDomain(char.GeneralString):
    tagSet = char.GeneralString.tagSet.tagExplicitly(
        tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1)
    )


class DcLocatorHint(univ.Integer):
    tagSet = univ.Integer.tagSet.tagExplicitly(
        tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)
    )


class KdcProxyMessage(univ.Sequence):
    """KDC-PROXY-MESSAGE as defined in MS-KKDCP 2.2.2"""
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('kerb-message', KerbMessage()),
        namedtype.OptionalNamedType('target-domain', TargetDomain()),
        namedtype.OptionalNamedType('dclocator-hint', DcLocatorHint())
    )


class AsReq(univ.Sequence):
    tagSet = univ.Sequence.tagSet.tagExplicitly(
        tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 10)
    )


class TgsReq(univ.Sequence):
    tagSet = univ.Sequence.tagSet.tagExplicitly(
        tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 12)
    )
