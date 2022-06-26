import imaplib
import email
from uuid import uuid4
import os
import html2text
import dateutil.parser


class Mail:
    def __init__(self, email_obj, download_path=None):
        self.email_obj = email_obj
        self.download_path = download_path
        self._subject = self.get_subject()
        self._from_add = self.get_from_add()
        self._email_date = self.get_email_date()
        self._body, self._attachment = self.get_body_and_attachments()

    def get_body_and_attachments(self):
        body_text = ''
        attachments = []

        for part in self.email_obj.walk():
            if part.get_content_type() == 'text/html':
                body = part.get_payload(decode=True)
                body_text = html2text.html2text(body.decode('utf-8'))

            if part.get_content_type() == 'text/plain':
                body = part.get_payload()

            if part.get('Content-Disposition'):
                file_name = part.get_filename()
                file_content = part.get_payload(decode=True)

                if not file_name and not file_content:
                    continue
                if not file_name:
                    file_name = 'downloaded_file_' + str(uuid4())
                result_path = Mail.write_file(file_name, file_content)
                # print(result_path)
                attachments.append(result_path)

        return body_text, attachments

    @staticmethod
    def write_file(file_name, file_content, download_path=None):
        if not download_path:
            download_path = os.path.join(os.getcwd(), 'download')
            os.makedirs(download_path, exist_ok=True)

        file_path = os.path.join(download_path, file_name)
        if not os.path.isfile(file_path):
            fp = open(file_path, 'wb')
            fp.write(file_content)
            fp.close()

        return file_path

    def get_subject(self):
        decode_subject = email.header.decode_header(self.email_obj['Subject'])[0][0]
        return decode_subject

    def get_from_add(self):
        decode_from_add = email.header.decode_header(self.email_obj['From'])[0][0]
        return decode_from_add

    def get_email_date(self):
        email_date = email.header.decode_header(self.email_obj['Received'])[0][0]
        return dateutil.parser.parse(email_date[-26:])

    @property
    def subject(self):
        return self._subject

    @property
    def body(self):
        return self._body

    @property
    def attachment(self):
        return self._attachment

    @property
    def from_add(self):
        return self._from_add

    @property
    def email_date(self):
        return self._email_date


class MailBox():
    def __init__(self, email_id, password):
        imap_server = "imap.outlook.com"
        self.username = email_id
        self.password = password
        self.imap = imaplib.IMAP4_SSL(imap_server)
        # email_id = "udaay7446@outlook.com"
        # password = "Aruna@270895"
        self.imap.login(email_id, password)
        self.imap.select("INBOX")

    def get_latest_mail(self, subject='', from_add='', keep_unread=False, download_path=None):
        # subject = 'This is test mail'
        # from_add = ''
        data = self.imap.uid('search', None, 'UNSEEN', f'(FROM "{from_add}")', f'(SUBJECT "{subject}")')[1][0].split()
        if len(data) > 0:
            latest = data[-1]
        else:
            return False
        mail_data = self.imap.uid('FETCH', latest, '(RFC822)')[1]

        if keep_unread:
            self.imap.uid('STORE', latest, '-FLAGS', '\SEEN')

        email_obj = email.message_from_string(mail_data[0][1].decode('utf-8'))

        return Mail(email_obj, download_path)







