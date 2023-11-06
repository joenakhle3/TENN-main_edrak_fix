import os
import sys
import json
import uuid

from tenn_ai.fabric_ai.utils.tenn_properties import TENN_Properties

import sqlalchemy as db
from sqlalchemy import URL, Engine, CursorResult, Sequence
from sqlalchemy.sql import text
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Row
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

import pandas as pd
from pandas import DataFrame

class TENN_SqlDB:

    # #########################################################################################################

    # Initiatlize the class with the database type
    def __init__(self, passed_db_path: str = "", passed_db_engine: str = "", passed_verbose: bool = False):
        self.properties = TENN_Properties()

        self.db_url = None
        self.db_engine_type = None
        self.engine: Engine = None # Will be set in the connect() function
        self.verbose = passed_verbose

        # If the passed db url is none or empty, use the standard sql db path from the properties
        if passed_db_path is None or passed_db_path == "":
            self.db_url = self.properties.standard_edrak_db_path
        elif not os.path.isdir(passed_db_path):
            print("TENN_SqlDB - Passed database path (" + str(passed_db_path) + ") is not a valid path. Switching to standard DB location.")
            self.db_url = self.properties.standard_edrak_db_path
        else:
            self.db_url = os.path.abspath(passed_db_path)
        if self.verbose: print("TENN_SqlDB - Using database path " + self.db_url)

        # If the passed db engine is none or empty, use the standard sql db engine from the properties
        if passed_db_engine is None or passed_db_engine == "":
            self.db_engine_type = self.properties.standard_edrak_db_engine
        elif passed_db_engine not in self.properties.allowed_engines:
            print("TENN_SqlDB - Unsupported database engine type (" + passed_db_engine + "). Switching to standard SQL database.")
            self.db_engine_type = self.properties.standard_edrak_db_engine
        else:
            self.db_engine_type = passed_db_engine
        if self.verbose: print("TENN_SqlDB - Using database engine " + self.db_engine_type)
        
        # Create the connection string
        self.connection_string = self.db_engine_type + ":///" + self.db_url
        if self.verbose: print("TENN_SqlDB - Using connection string " + self.connection_string)

    # #########################################################################################################

    # Set the database engine
    def connect(self) -> Engine:
        # Create the engine based on db_type.
        try:
            self.engine = db.create_engine(self.connection_string, echo=self.verbose)
        except Exception as e:
            if self.verbose: print("TENN_SqlDB - Connect error: " + str(e))
            return None
        
        if self.verbose: print("TENN_SqlDB - Connected to the database.")
        return self.engine
                               
        # TODO - Add support for other database types based on the engine type

    # #########################################################################################################

    # Function to execute a SQL statement (needs an open connection)
    def query(self, passed_query: str = "") -> DataFrame:
        # Return nothing if query is empty
        if passed_query == "" or passed_query is None: return ""

        # If we're not connected to a DB, raise an exception
        if self.engine is None:
            raise Exception("TENN_SqlDB - Cannot query without connecting to a database first.")

        response: CursorResult = None
        result: DataFrame = None

        if self.verbose: print("\nTENN_SqlDB - Executing query " + passed_query)
        try:
            with self.engine.connect() as connection:
                response = connection.execute(text(passed_query)) # We would use this if we want to use sqlalchemy to query directly
                connection.commit()
                result = pd.DataFrame(response)
                # result = pd.read_sql(passed_query, connection)

                if self.verbose: print("TENN_SqlDB - Query executed successfully.")
                # if response.returns_rows:
                if result is not None:
                    # result = response.fetchall()
                    if self.verbose: 
                        print("TENN_SqlDB - Query returned " + str(len(result)) + " rows.")
                        print("-----------------------------------------------------------------------")
                        print(result)
                        print("-----------------------------------------------------------------------")
                else:
                    # result = None
                    if self.verbose: print("TENN_SqlDB - Query type does not return rows.")

        except Exception as e:
            if self.verbose: print("TENN_SqlDB - " + str(e))
            result = None
        
        finally:
            connection.commit()
            connection.close()
            if self.verbose: print("TENN_SqlDB - Query completed.\n")

        return result
    