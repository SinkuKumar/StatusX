import os
import pyodbc
from dotenv import load_dotenv
from datetime import datetime, timedelta

current_date = datetime.now().date()
next_date = current_date + timedelta(days=1)

# Format dates as 'YYYY-MM-DD'
current_date_str = current_date.strftime('%Y-%m-%d')
next_date_str = next_date.strftime('%Y-%m-%d')

class PyODBCSQL:
    def __init__(self, database):
        load_dotenv()
        self.server = os.getenv("SQL_SERVER")
        self.database = database
        self.username = os.getenv("SQL_USERNAME")
        self.password = os.getenv("SQL_PASSWORD")
        self.conn = None

    def execute_query(self, query: str) -> list[tuple[str, str]]:
        self.conn = pyodbc.connect(
            f"""DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};
                                UID={self.username};PWD={self.password}""",
            TrustServerCertificate="yes",
        )
        cursor = self.conn.cursor()
        cursor.execute(query)

        if cursor.description is not None:
            data = cursor.fetchall()
        else:
            data = None

        self.conn.commit()
        cursor.close()
        self.conn.close()
        return data

    def get_all_active_clients(self):
        query = r"select distinct client_id from bi_afc..afc_password_tbl where active = 1;"
        result = self.execute_query(query)
        client_list = [x[0] for x in result]
        return client_list
    
    def data_uploads_pending_python_side(self):
        query = rf"""
            select client_id from bi_afc..afc_password_tbl
            where active = 1 and client_id not in (
                select distinct client_id from bi_afc_experity..data_uploads_summary 
                where date_updated > '{current_date_str}' and date_updated <= '{next_date_str}'
            );
        """
        result = self.execute_query(query)
        client_list = [x[0] for x in result]
        return client_list
    
    def pdf_in_progress_count(self):
        query = r"SELECT COUNT(*) FROM BI_AFC..MB_trans_master_progress WHERE file_location = 'TEMP';"
        count = self.execute_query(query)
        return count[0][0]
    
    def pdf_yet_to_start_count(self):
        query = r"SELECT COUNT(*) FROM BI_AFC..MB_trans_master_progress WHERE file_location IS NULL;"
        count = self.execute_query(query)
        return count[0][0]
    
    def pending_sms_and_email_count(self):
        query = r"select  count(*) from bi_afc..email_schedule where exp_posted != 1;"
        count = self.execute_query(query)
        return count[0][0]
    
    def sms_count_today(self):
        query = rf"""
            SELECT count(*) FROM BI_AFC..RingCentralMessages WHERE 
            creationTime > '{current_date_str}' 
            and creationTime <= '{next_date_str}';
        """
        count = self.execute_query(query)
        return count[0][0]
    
    def call_sync_count_today(self):
        query = rf"""
            SELECT count(*) FROM BI_AFC..RC_Call_Logs WHERE 
            startTime > '{current_date_str}' 
            and startTime <= '{next_date_str}';
        """
        count = self.execute_query(query)
        return count[0][0]

    def total_call_transcript_count(self):
        query = r"SELECT count(*) FROM MB_Call_Table where transcript is null;"
        count = self.execute_query(query)
        return count[0][0]
