================================
ZenPacks.community.OracleMon
================================

About
=====

This project is `Zenoss <http://www.zenoss.com/>`_ extension (ZenPack) that
makes it possible to model and monitor Oracle databases.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2, Zenoss 3.2 and Zenoss 4.2. You can download the free Core version of
Zenoss from http://community.zenoss.org/community/download

ZenPacks
--------

You must first install

- `SQLDataSource ZenPack <http://community.zenoss.org/docs/DOC-5913>`_
- `RDBMS Monitoring ZenPack <http://community.zenoss.org/docs/DOC-3447>`_

External dependencies
---------------------

You can use **pyisqldb** module provided by SQLDataSource ZenPack in combination
with Oracle ODBC driver, or install Python DB-API 2.0 compatible cx_Oracle
module. cx_Oracle can be installed with **easy_install-2.6** command as
**zenoss** user.

- **pyisqldb** - DB-API 2.0 compatible wrapper for **isql** command from
  `unixODBC <http://www.unixodbc.org/>`_. Oracle ODBC driver must be
  installed and registered with name "OracleDB".

  zOracleConnectionString example:

      ::

          'pyisqldb','DRIVER={OracleDB};SERVER=${here/dsn};UID=${here/zOracleUser};PWD=${here/zOraclePassword}',ansi=True,cp_good_sql='SELECT 1 FROM DUAL'

- `pyodbc <http://code.google.com/p/pyodbc/>`_ - DB-API 2.0 compatible interface
  to unixODBC. Oracle ODBC driver must be installed and registered with name
  "OracleDB".

  zOracleConnectionString example:

      ::

          'pyodbc',DRIVER='{OracleDB}',SERVER='${here/dsn}',UID='${here/zOracleUser}',PWD='${here/zOraclePassword}',ansi=True,cp_good_sql='SELECT 1 FROM DUAL'

- `cx_Oracle <http://cx-oracle.sourceforge.net/>`_ - DB-API 2.0 compatible Pure-Python
  interface to the Oracle database.

  zOracleConnectionString example 1:

      ::

          'cx_Oracle','${here/zOracleUser}','${here/zOraclePassword}','${here/dsn}',cp_good_sql='SELECT 1 FROM DUAL'

  zOracleConnectionString example 2 (connect as DBA):

      ::

          'cx_Oracle','${here/zOracleUser}','${here/zOraclePassword}','${here/dsn}',mode=2,cp_good_sql='SELECT 1 FROM DUAL'

Installation
============

If you have an old version of this ZenPack installed, please uninstall it first.

Normal Installation (packaged egg)
----------------------------------

Download the `OracleMon ZenPack <http://community.zenoss.org/docs/DOC-10244>`_.
Copy this file to your Zenoss server and run the following commands as the zenoss
user.

    ::

        zenpack --install ZenPacks.community.OracleMon-1.3.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the OracleMon
ZenPack you should clone the git `repository <https://github.com/epuzanov/ZenPacks.community.OracleMon>`_,
then install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.OracleMon.git
        zenpack --link --install ZenPacks.community.OracleMon
        zenoss restart


Usage
=====

Installing the ZenPack will add the following items to your Zenoss system.

Configuration Properties
------------------------

- zOracleConnectionString - connection string template.
- zOracleDSN - list of TSNs for Oracle Database Instances.
- zOracleUser - Username for the Oracle account.
- zOraclePassword - Password for the Oracle account
- zOracleTablespaceIgnoreNames - tablespace names to ignore
- zOracleTablespaceIgnoreTypes - tablespace types to ignore [PERMANENT, TEMPORARY, UNDO]

Modeler Plugins
---------------

- community.sql.OracleDatabaseMap

Monitoring Templates
--------------------

- OracleSrvInst
- OracleTablespace

Performance graphs
------------------

**OracleSrvInst**

- Transactions
- IO
- Database Time Ratio
- Load
- Redo Log
- Shared Pool
- Interconnect Times
- Logon rate
- Errors
- Sessions
- DBA Objects

**OracleTablespace**

- Usage
