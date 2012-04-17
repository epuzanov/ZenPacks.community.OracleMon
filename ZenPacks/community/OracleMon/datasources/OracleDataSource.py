################################################################################
#
# This program is part of the OracleMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OracleDataSource

Defines attributes for how a datasource will be graphed
and builds the nessesary DEF and CDEF statements for it.

$Id: OracleDataSource.py,v 1.2 2012/04/17 23:56:42 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from ZenPacks.community.SQLDataSource.datasources import SQLDataSource

class OracleDataSource(SQLDataSource.SQLDataSource):

    ZENPACKID = 'ZenPacks.community.OracleMon'

    sourcetypes = ('Oracle',)
    sourcetype = 'Oracle'

    timeout = 15

    cs = '${here/zOracleConnectionString}'
    dsn = '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=${dev/manageIp})(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=ORCL)))'
    username = '${here/zOracleUser}'
    password = '${here/zOraclePassword}'


    _properties = SQLDataSource.SQLDataSource._properties + (
        {'id':'dsn', 'type':'string', 'mode':'w'},
        {'id':'username', 'type':'string', 'mode':'w'},
        {'id':'password', 'type':'string', 'mode':'w'},
        {'id':'timeout', 'type':'int', 'mode':'w'},
        )

    _relations = SQLDataSource.SQLDataSource._relations + (
        )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
    {
        'immediate_view' : 'editOracleDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit'
            , 'name'          : 'Data Source'
            , 'action'        : 'editOracleDataSource'
            , 'permissions'   : ( 'View', )
            },
        )
    },
    )


    def zmanage_editProperties(self, REQUEST=None):
        'add some validation'
        if REQUEST:
            self.dsn = REQUEST.get('dsn', '')
            self.username = REQUEST.get('username', '')
            self.password = REQUEST.get('password', '')
            self.sql = REQUEST.get('sql', '')
            self.sqlparsed, self.sqlkb = self.parseSqlQuery(self.sql)
        return SQLDataSource.SQLDataSource.zmanage_editProperties(self, REQUEST)
