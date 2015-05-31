import platform

import pytest
import easysnmp

from .fixtures import (
    sess_v1_args, sess_v2_args, sess_v3_args,
    sess_v1, sess_v2, sess_v3
)
from .helpers import snmp_set_via_cli


@pytest.yield_fixture(autouse=True)
def reset_values():
    snmp_set_via_cli('sysLocation.0', 'my original location', 's')
    snmp_set_via_cli('nsCacheTimeout.1.3.6.1.2.1.2.2', '0', 'i')
    yield


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get(sess_args):
    res = easysnmp.snmp_get('sysDescr.0', **sess_args)

    assert platform.version() in res.value
    assert res.oid == 'sysDescr'
    assert res.oid_index == '0'
    assert res.snmp_type == 'OCTETSTR'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_tuple(sess_args):
    res = easysnmp.snmp_get(('sysDescr', '0'), **sess_args)

    assert platform.version() in res.value
    assert res.oid == 'sysDescr'
    assert res.oid_index == '0'
    assert res.snmp_type == 'OCTETSTR'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_fully_qualified(sess_args):
    res = easysnmp.snmp_get(
        '.iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0', **sess_args
    )

    assert platform.version() in res.value
    assert res.oid == 'sysDescr'
    assert res.oid_index == '0'
    assert res.snmp_type == 'OCTETSTR'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_fully_qualified_tuple(sess_args):
    res = easysnmp.snmp_get(
        ('.iso.org.dod.internet.mgmt.mib-2.system.sysDescr', '0'), **sess_args
    )

    assert platform.version() in res.value
    assert res.oid == 'sysDescr'
    assert res.oid_index == '0'
    assert res.snmp_type == 'OCTETSTR'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_numeric(sess_args):
    res = easysnmp.snmp_get(('.1.3.6.1.2.1.1.1', '0'), **sess_args)

    assert platform.version() in res.value
    assert res.oid == 'sysDescr'
    assert res.oid_index == '0'
    assert res.snmp_type == 'OCTETSTR'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_unknown(sess_args):
    with pytest.raises(easysnmp.EasySNMPUnknownObjectIDError):
        easysnmp.snmp_get('sysDescripto.0', **sess_args)


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_invalid_instance(sess_args):
    with pytest.raises(easysnmp.EasySNMPNoSuchInstanceError):
        easysnmp.snmp_get('sysContact.1', **sess_args)


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_invalid_object(sess_args):
    with pytest.raises(easysnmp.EasySNMPNoSuchObjectError):
        easysnmp.snmp_get('iso', **sess_args)


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_next(sess_args):
    res = easysnmp.snmp_get_next('nsCacheEntry', **sess_args)

    assert res.oid == 'nsCacheTimeout'
    assert res.oid_index == '1.3.6.1.2.1.2.2'
    assert res.value >= 0
    assert res.snmp_type == 'INTEGER'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_next_numeric(sess_args):
    res = easysnmp.snmp_get_next(('.1.3.6.1.2.1.1.1', '0'), **sess_args)

    assert res.oid == 'sysObjectID'
    assert res.oid_index == '0'
    assert res.value == '.1.3.6.1.4.1.8072.3.2.10'
    assert res.snmp_type == 'OBJECTID'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_next_unknown(sess_args):
    with pytest.raises(easysnmp.EasySNMPUnknownObjectIDError):
        easysnmp.snmp_get_next('sysDescripto.0', **sess_args)


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_set_string(sess_args):
    res = easysnmp.snmp_get(('sysLocation', '0'), **sess_args)
    assert res.oid == 'sysLocation'
    assert res.oid_index == '0'
    assert res.value != 'my newer location'
    assert res.snmp_type == 'OCTETSTR'

    success = easysnmp.snmp_set(
        ('sysLocation', '0'), 'my newer location', **sess_args
    )
    assert success

    res = easysnmp.snmp_get(('sysLocation', '0'), **sess_args)
    assert res.oid == 'sysLocation'
    assert res.oid_index == '0'
    assert res.value == 'my newer location'
    assert res.snmp_type == 'OCTETSTR'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_set_integer(sess_args):
    success = easysnmp.snmp_set(
        ('nsCacheTimeout', '.1.3.6.1.2.1.2.2'), 65, **sess_args
    )
    assert success

    res = easysnmp.snmp_get(
        ('nsCacheTimeout', '.1.3.6.1.2.1.2.2'), **sess_args
    )
    assert res.oid == 'nsCacheTimeout'
    assert res.oid_index == '1.3.6.1.2.1.2.2'
    assert res.value == '65'
    assert res.snmp_type == 'INTEGER'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_set_unknown(sess_args):
    with pytest.raises(easysnmp.EasySNMPUnknownObjectIDError):
        easysnmp.snmp_set('nsCacheTimeoooout', 1234, **sess_args)


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_set_multiple(sess_args):
    res = easysnmp.snmp_get(
        ['sysLocation.0', 'nsCacheTimeout.1.3.6.1.2.1.2.2'], **sess_args
    )
    assert res[0].value != 'my newer location'
    assert res[1].value != '162'

    success = easysnmp.snmp_set_multiple([
        ('sysLocation.0', 'my newer location'),
        (('nsCacheTimeout', '.1.3.6.1.2.1.2.2'), 162)
    ], **sess_args)
    assert success

    res = easysnmp.snmp_get(
        ['sysLocation.0', 'nsCacheTimeout.1.3.6.1.2.1.2.2'], **sess_args
    )
    assert res[0].value == 'my newer location'
    assert res[1].value == '162'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_get_bulk(sess_args):
    if sess_args['version'] == 1:
        with pytest.raises(easysnmp.EasySNMPError):
            easysnmp.snmp_get_bulk([
                'sysUpTime', 'sysORLastChange', 'sysORID', 'sysORDescr',
                'sysORUpTime'], 2, 8, **sess_args
            )
    else:
        res = easysnmp.snmp_get_bulk([
            'sysUpTime', 'sysORLastChange', 'sysORID', 'sysORDescr',
            'sysORUpTime'], 2, 8, **sess_args
        )

        assert len(res) == 26

        assert res[0].oid == 'sysUpTimeInstance'
        assert res[0].oid_index is ''
        assert res[0].value > 0
        assert res[0].snmp_type == 'TICKS'

        assert res[4].oid == 'sysORUpTime'
        assert res[4].oid_index == '1'
        assert res[4].value >= 0
        assert res[4].snmp_type == 'TICKS'


@pytest.mark.parametrize('sess', [sess_v1(), sess_v2(), sess_v3()])
def test_snmp_session_set_multiple_next(sess):
    success = sess.set_multiple([
        ('.1.3.6.1.6.3.12.1.2.1.2.116.101.115.116', '.1.3.6.1.6.1.1'),
        ('.1.3.6.1.6.3.12.1.2.1.3.116.101.115.116', '1234'),
        ('.1.3.6.1.6.3.12.1.2.1.9.116.101.115.116', 4),
    ])
    assert success

    res = sess.get_next([
        'snmpTargetAddrTDomain', 'snmpTargetAddrTAddress',
        'snmpTargetAddrRowStatus'
    ])

    assert len(res) == 3

    assert res[0].oid == 'snmpTargetAddrTDomain'
    assert res[0].oid_index == '116.101.115.116'
    assert res[0].value == '.1.3.6.1.6.1.1'
    assert res[0].snmp_type == 'OBJECTID'

    assert res[1].oid == 'snmpTargetAddrTAddress'
    assert res[1].oid_index == '116.101.115.116'
    assert res[1].value == '1234'
    assert res[1].snmp_type == 'OCTETSTR'

    assert res[2].oid == 'snmpTargetAddrRowStatus'
    assert res[2].oid_index == '116.101.115.116'
    assert res[2].value == '3'
    assert res[2].snmp_type == 'INTEGER'


@pytest.mark.parametrize('sess', [sess_v1(), sess_v2(), sess_v3()])
def test_snmp_session_set_clear(sess):
    res = sess.set('.1.3.6.1.6.3.12.1.2.1.9.116.101.115.116', 6)
    assert res == 1

    res = sess.get_next([
        'snmpTargetAddrTDomain', 'snmpTargetAddrTAddress',
        'snmpTargetAddrRowStatus'
    ])

    assert len(res) == 3

    assert res[0].oid == 'snmpUnavailableContexts'
    assert res[0].oid_index == '0'
    assert res[0].value == '0'
    assert res[0].snmp_type == 'COUNTER'

    assert res[1].oid == 'snmpUnavailableContexts'
    assert res[1].oid_index == '0'
    assert res[1].value == '0'
    assert res[1].snmp_type == 'COUNTER'

    assert res[2].oid == 'snmpUnavailableContexts'
    assert res[2].oid_index == '0'
    assert res[2].value == '0'
    assert res[2].snmp_type == 'COUNTER'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_walk(sess_args):
    res = easysnmp.snmp_walk('system', **sess_args)
    assert len(res) >= 7

    assert platform.version() in res[0].value
    assert res[3].value == 'G. S. Marzot <gmarzot@marzot.net>'
    assert res[4].value == platform.node()
    assert res[5].value == 'my original location'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_walk_res(sess_args):
    res = easysnmp.snmp_walk('system', **sess_args)

    assert len(res) >= 7

    assert res[0].oid == 'sysDescr'
    assert res[0].oid_index == '0'
    assert platform.version() in res[0].value
    assert res[0].snmp_type == 'OCTETSTR'

    assert res[3].oid == 'sysContact'
    assert res[3].oid_index == '0'
    assert res[3].value == 'G. S. Marzot <gmarzot@marzot.net>'
    assert res[3].snmp_type == 'OCTETSTR'

    assert res[4].oid == 'sysName'
    assert res[4].oid_index == '0'
    assert res[4].value == platform.node()
    assert res[4].snmp_type == 'OCTETSTR'

    assert res[5].oid == 'sysLocation'
    assert res[5].oid_index == '0'
    assert res[5].value == 'my original location'
    assert res[5].snmp_type == 'OCTETSTR'


@pytest.mark.parametrize(
    'sess_args', [sess_v1_args(), sess_v2_args(), sess_v3_args()]
)
def test_snmp_walk_unknown(sess_args):
    with pytest.raises(easysnmp.EasySNMPUnknownObjectIDError):
        easysnmp.snmp_walk('systemo', **sess_args)


@pytest.mark.parametrize('sess', [sess_v1(), sess_v2(), sess_v3()])
def test_snmp_session_get(sess):
    res = sess.get([
        ('sysUpTime', '0'),
        ('sysContact', '0'),
        ('sysLocation', '0')
    ])

    assert len(res) == 3

    assert res[0].oid == 'sysUpTimeInstance'
    assert res[0].oid_index is ''
    assert res[0].value > 0
    assert res[0].snmp_type == 'TICKS'

    assert res[1].oid == 'sysContact'
    assert res[1].oid_index == '0'
    assert res[1].value == 'G. S. Marzot <gmarzot@marzot.net>'
    assert res[1].snmp_type == 'OCTETSTR'

    assert res[2].oid == 'sysLocation'
    assert res[2].oid_index == '0'
    assert res[2].value == 'my original location'
    assert res[2].snmp_type == 'OCTETSTR'


@pytest.mark.parametrize('sess', [sess_v1(), sess_v2(), sess_v3()])
def test_snmp_session_get_next(sess):
    res = sess.get_next([
        ('sysUpTime', '0'),
        ('sysContact', '0'),
        ('sysLocation', '0')
    ])

    assert len(res) == 3

    assert res[0].oid == 'sysContact'
    assert res[0].oid_index == '0'
    assert res[0].value == 'G. S. Marzot <gmarzot@marzot.net>'
    assert res[0].snmp_type == 'OCTETSTR'

    assert res[1].oid == 'sysName'
    assert res[1].oid_index == '0'
    assert res[1].value == platform.node()
    assert res[1].snmp_type == 'OCTETSTR'

    assert res[2].oid == 'sysORLastChange'
    assert res[2].oid_index == '0'
    assert res[2].value >= 0
    assert res[2].snmp_type == 'TICKS'


@pytest.mark.parametrize('sess', [sess_v1(), sess_v2(), sess_v3()])
def test_snmp_session_set(sess):
    res = sess.get(('sysLocation', '0'))
    assert res.value != 'my newer location'

    success = sess.set(('sysLocation', '0'), 'my newer location')
    assert success

    res = sess.get(('sysLocation', '0'))
    assert res.value == 'my newer location'


@pytest.mark.parametrize('sess', [sess_v1(), sess_v2(), sess_v3()])
def test_snmp_session_set_multiple(sess):
    res = sess.get(['sysLocation.0', 'nsCacheTimeout.1.3.6.1.2.1.2.2'])
    assert res[0].value != 'my newer location'
    assert res[1].value != '160'

    success = sess.set_multiple([
        ('sysLocation.0', 'my newer location'),
        (('nsCacheTimeout', '.1.3.6.1.2.1.2.2'), 160),
    ])
    assert success

    res = sess.get(['sysLocation.0', 'nsCacheTimeout.1.3.6.1.2.1.2.2'])
    assert res[0].value == 'my newer location'
    assert res[1].value == '160'


@pytest.mark.parametrize('sess', [sess_v1(), sess_v2(), sess_v3()])
def test_snmp_session_get_bulk(sess):  # noqa
    if sess.version == 1:
        with pytest.raises(easysnmp.EasySNMPError):
            sess.get_bulk(
                ['sysUpTime', 'sysORLastChange', 'sysORID', 'sysORDescr',
                 'sysORUpTime'],
                2, 8
            )
    else:
        res = sess.get_bulk(
            ['sysUpTime', 'sysORLastChange', 'sysORID', 'sysORDescr',
             'sysORUpTime'], 2, 8
        )

        assert len(res) == 26

        assert res[0].oid == 'sysUpTimeInstance'
        assert res[0].oid_index is ''
        assert res[0].value > 0
        assert res[0].snmp_type == 'TICKS'

        assert res[4].oid == 'sysORUpTime'
        assert res[4].oid_index == '1'
        assert res[4].value >= 0
        assert res[4].snmp_type == 'TICKS'


@pytest.mark.parametrize('sess', [sess_v1(), sess_v2(), sess_v3()])
def test_snmp_session_walk(sess):
    res = sess.walk('system')

    assert len(res) >= 7

    assert res[0].oid == 'sysDescr'
    assert res[0].oid_index == '0'
    assert platform.version() in res[0].value
    assert res[0].snmp_type == 'OCTETSTR'

    assert res[3].oid == 'sysContact'
    assert res[3].oid_index == '0'
    assert res[3].value == 'G. S. Marzot <gmarzot@marzot.net>'
    assert res[3].snmp_type == 'OCTETSTR'

    assert res[4].oid == 'sysName'
    assert res[4].oid_index == '0'
    assert res[4].value == platform.node()
    assert res[4].snmp_type == 'OCTETSTR'

    assert res[5].oid == 'sysLocation'
    assert res[5].oid_index == '0'
    assert res[5].value == 'my original location'
    assert res[5].snmp_type == 'OCTETSTR'
