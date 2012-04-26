################################################################################
#
# This program is part of the OracleMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OracleDatabaseMap.py

OracleDatabaseMap maps the Oracle Databases table to Database objects

$Id: OracleDatabaseMap.py,v 1.6 2012/04/26 23:08:02 egor Exp $"""

__version__ = "$Revision: 1.6 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.DataMaps import MultiArgs
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
import re

class OracleDatabaseMap(ZenPackPersistence, SQLPlugin):


    ZENPACKID = 'ZenPacks.community.OracleMon'

    maptype = "OracleDatabaseMap"
    compname = "os"
    relname = "softwaredbsrvinstances"
    modname = "ZenPacks.community.OracleMon.OracleSrvInst"
    deviceProperties = SQLPlugin.deviceProperties + ('zOracleUser',
                                                'zOraclePassword',
                                                'zOracleConnectionString',
                                                'zOracleDSN',
                                                'zOracleTablespaceIgnoreNames',
                                                'zOracleTablespaceIgnoreTypes',
                                                )


    def queries(self, device):
        tasks = {}
        connectionString = getattr(device, 'zOracleConnectionString', '') or \
            "'cx_Oracle','${here/zOracleUser}','${here/zOraclePassword}','${here/dsn}'"
        dsns = getattr(device, 'zOracleDSN', '') or \
            "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=${here/manageIp})(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=ORCL)))"
        if type(dsns) is str:
            dsns = [dsns]
        for inst, dsn in enumerate(dsns):
            if not dsn.strip(): continue
            setattr(device, 'dsn', self.prepareCS(device, dsn))
            cs = self.prepareCS(device, connectionString)
            tasks['si_%s'%inst] = (
                """SELECT NAME,
                          ( SELECT BANNER
                            FROM v$version
                            WHERE rownum = 1
                          ) VERSION,
                          '%s' DSN
                    FROM v$database"""%device.dsn,
                None,
                cs,
                {
                    'dbsiname':'name',
                    'setProductKey':'version',
                    'dsn':'dsn',
                })
            tasks['db_%s'%inst] = (
                """SELECT TABLESPACE_NAME,
                          a.CONTENTS,
                          a.BLOCK_SIZE,
                          b.BYTES/a.BLOCK_SIZE BLOCKS,
                          ( SELECT NAME
                            FROM v$database
                            WHERE rownum = 1
                          ) DATABASE
                   FROM ( SELECT TABLESPACE_NAME,
                                 CONTENTS,
                                 BLOCK_SIZE
                          FROM dba_tablespaces ) a
                   INNER JOIN
                        ( SELECT TABLESPACE_NAME,
                                 sum(BYTES) BYTES
                          FROM dba_data_files
                          GROUP BY TABLESPACE_NAME) b
                   USING (TABLESPACE_NAME)""",
                None,
                cs,
                {
                    'dbname':'tablespace_name',
                    'type':'contents',
                    'blockSize':'block_size',
                    'totalBlocks':'blocks',
                    'setDBSrvInst':'database',
                })
        return tasks

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        skiptsnames = getattr(device, 'zOracleTablespaceIgnoreNames', None)
        skiptstypes = getattr(device, 'zOracleTablespaceIgnoreTypes', None)
        maps = [self.relMap()]
        databases = []
        for tname, instances in results.iteritems():
            if tname.startswith('si_'):
                for inst in instances:
                    om = self.objectMap(inst)
                    om.id = self.prepId(om.dbsiname)
                    om.setProductKey = MultiArgs(om.setProductKey, 'Oracle')
                    maps[-1].append(om)
            else: databases.extend(instances)
        self.relname = "softwaredatabases"
        self.modname = "ZenPacks.community.OracleMon.OracleTablespace"
        maps.append(self.relMap())
        for tspace in databases:
            if (skiptsnames and re.search(skiptsnames,tspace['dbname'])):continue
            if (skiptstypes and re.search(skiptstypes,tspace['type'])):continue
            try:
                om = self.objectMap(tspace)
                om.id = self.prepId('%s_%s'%(om.setDBSrvInst, om.dbname))
            except AttributeError:
                continue
            maps[-1].append(om)
        return maps
