
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ OracleMon loader
    """

    packZProperties = [
            ('zOracleConnectionString', "'cx_Oracle','${here/zOracleUser}','${here/zOraclePassword}','${here/dsn}',cp_good_sql='SELECT 1 FROM DUAL'", 'string'),
            ('zOracleDSN', ['(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=${here/manageIp})(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=ORCL)))'], 'lines'),
            ('zOracleUser', 'zenoss', 'string'),
            ('zOraclePassword', '', 'password'),
            ('zOracleTablespaceIgnoreNames', '', 'string'),
            ('zOracleTablespaceIgnoreTypes', '', 'string'),
            ]

