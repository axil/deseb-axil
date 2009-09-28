class DesebDatabaseOperations(object):
    def __init__(self, connection, style):
        self.connection = connection
        self.style = style
    
    def get_sql_indexes_for_field(self, tablespace, table, f):
        "Returns the CREATE INDEX SQL statement for a single field"
        from django.db import backend
        output = []
        try:
            autopk = self.connection.features.autoindexes_primary_keys
        except AttributeError:
            autopk = False
        if f.db_index and not ((f.primary_key or f.unique) and autopk):
            unique = f.unique and 'UNIQUE ' or ''
            try:
                tablespace = f.db_tablespace or tablespace
            except: # v0.96 compatibility
                tablespace = None
            if tablespace and backend.supports_tablespaces:
                tablespace_sql = ' ' + backend.get_tablespace_sql(tablespace)
            else:
                tablespace_sql = ''
            qn = self.connection.ops.quote_name
            output.append(
                self.style.SQL_KEYWORD('CREATE %sINDEX' % unique) + ' ' + \
                self.style.SQL_TABLE(qn('%s_%s' % (table, f.column))) + ' ' + \
                self.style.SQL_KEYWORD('ON') + ' ' + \
                self.style.SQL_TABLE(qn(table)) + ' ' + \
                "(%s)" % self.style.SQL_FIELD(qn(f.column)) + \
                "%s;" % tablespace_sql
            )
        return output
        
    def drop_sql_index_for_field(self, index_name):
        "Returns the CREATE INDEX SQL statement for a single field"
        from django.db import backend
        qn = self.connection.ops.quote_name
        output = [
            self.style.SQL_KEYWORD('DROP INDEX') + ' ' + \
            self.style.SQL_TABLE(qn(index_name))+";"
        ]
        return output
        
