from utils.pyodbc_utils import PyODBCSQL

sql = PyODBCSQL("BI_AFC")

data_uploads = sql.data_uploads_pending_python_side()
print(f"\nData Uplods Pending clients : {data_uploads}\n")

pdf_in_progress_count = sql.pdf_in_progress_count()
print(f"PDF In Progress count : {pdf_in_progress_count}\n")

pdf_yet_to_start_count = sql.pdf_yet_to_start_count()
print(f"PDF Yet to start count : {pdf_yet_to_start_count}\n")

pending_sms_and_email_count = sql.pending_sms_and_email_count()
print(f"Pending SMS & Email count: {pending_sms_and_email_count}\n")

sms_count_today = sql.sms_count_today()
print(f"SMS count today : {sms_count_today}\n")

call_sync_count_today = sql.call_sync_count_today()
print(f"Call sync count today : {call_sync_count_today}\n")

total_call_transcript_count = sql.total_call_transcript_count()
print(f"Total call transcripts count : {total_call_transcript_count}\n")