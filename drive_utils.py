import os
import pickle
import shutil
import io
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload 

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
    			creds = pickle.load(token)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
    			creds.refresh(Request())
		else:
    			flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    			creds = flow.fetch_token(code=code)
	with open('token.pickle', 'wb') as token:
    		pickle.dump(creds, token)

	service = googleapiclient.discovery.build('drive', 'v3', credentials=creds)
	return service

def download_file_from_drive(file_id, local_file_name):
	service = authenticate_drive()
	try:
		request = service.files().get_media(fileId=file_id)
		fh = io.BytesIO()
		downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
		done = False
		while not done:
			status, done = downloader.next_chunk()
			print(f"Download progress: {int(status.progress() * 100)}%")
		fh.seek(0)
		with open(local_file_name, 'wb') as f:
			shutil.copyfileobj(fh, f)
	except Exception as e:
		print(f"Error downloading file: {e}")
def create_folder(service, folder_name, parent_id=None):
	file_metadata = {
        	'name': folder_name,
        	'mimeType': 'application/vnd.google-apps.folder'
    	}
	if parent_id:
		file_metadata['parents'] = [parent_id]

	folder = service.files().create(body=file_metadata, fields='id').execute()
	return folder.get('id')
def upload_file_to_drive(local_file_name, drive_folder_id=None):
	service = authenticate_drive()
	file_metadata = {'name': os.path.basename(local_file_name)}
	if drive_folder_id:
		file_metadata['parents'] = [drive_folder_id]
	media = googleapiclient.http.MediaFileUpload(local_file_name, resumable=True)
	file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	print(f'File uploaded, ID: {file["id"]}')

def upload_folder(local_folder, drive_folder_name):
	service = authenticate_drive()
	root_folder_id = create_folder(service, drive_folder_name)
	folder_mapping = {local_folder: root_folder_id}

	for root, dirs, files in os.walk(local_folder):
		for dir_name in dirs:
			local_subfolder_path = os.path.join(root, dir_name)
			parent_drive_folder_id = folder_mapping[root]  # Parent folder ID
			drive_subfolder_id = create_folder(service, dir_name, parent_id=parent_drive_folder_id)
			folder_mapping[local_subfolder_path] = drive_subfolder_id  # Map the local subfolder path
		for file_name in files:
			file_path = os.path.join(root, file_name)
			parent_drive_folder_id = folder_mapping[root]  # Parent folder ID
			print(f"Uploading {file_path} to folder ID {parent_drive_folder_id}...")
			upload_file_to_drive( file_path, parent_drive_folder_id)
			print(f"Folder '{drive_folder_name}' and its contents uploaded successfully!")

if __name__ == '__main__':
	upload_folder('.','workdir')
