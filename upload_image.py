from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

class Upload_image:
    def __init__(self):
        self.folder = None

    def make_file(self, nickName, DRIVE):
        folder_metadata = {
            'name': nickName,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = DRIVE.files().create(body=folder_metadata,
                                      fields='id').execute()
        print('Folder ID: %s' % folder.get('id'))
        return folder

    def saveImage(self, img_url, nickName):
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        SCOPES = 'https://www.googleapis.com/auth/drive.file'
        store = file.Storage('storage.json')
        creds = store.get()

        if not creds or creds.invalid:
            print("make new storage data file ")
            flow = client.flow_from_clientsecrets('client_secret2.json', SCOPES)  # 서비스 계정 키 json 형식으로 저장
            creds = tools.run_flow(flow, store, flags) \
                if flags else tools.run(flow, store)

        DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

        if self.folder is None:
            self.folder = self.make_file(nickName, DRIVE)

        print('folder id : ' + self.folder.get('id'))
        '''
        if(self.__file_id == None):
            # 폴더 생성
            # 이름을 바꾸려면 kakao를 변경하면 됨
            # 폴더가 새로 생성됨
            folder_metadata = {
                'name': file_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = DRIVE.files().create(body=folder_metadata,
                                      fields='id').execute()
            print('Folder ID: %s' % folder.get('id'))
            self.file_id = folder.get('id')
        '''

        # 기존 폴더를 사용할 경우 위에 만들어진 폴더 아이디를 folder.get('id') 부분에 넣으면 됨
        file_metadata = \
            {
                'name': img_url,
                'parents': [self.folder.get('id')]
            }

        media = MediaFileUpload('./img/'+nickName+'/'+img_url,
                                mimetype='image/jpeg')
        img_id = DRIVE.files().create(body=file_metadata,
                                      media_body=media).execute()
        print('File ID: %s' % img_id.get('id'))

        return img_id.get('id')

