import smtplib
from email.mime.text import MIMEText
from collections import defaultdict


def send_email(subject, message, from_addr, *to_addrs,
               host="localhost", port=1025, headers=None):
    headers = {} if headers is None else headers
    email = MIMEText(message)
    email['Subject'] = subject
    email['From'] = from_addr
    
    for header, value in headers.items():
        email[header] = value
        
    sender = smtplib.SMTP(host, port)
    for addr in to_addrs:
        del email['To']
        email['To'] = addr
        sender.sendmail(from_addr, addr, email.as_string())
    sender.quit()
    

class MailingList:
    """Manage groups of e-mail addresses for sending e-mails."""
    def __init__(self):
        self.email_map = defaultdict(set)
        self.data_file = "database.txt"
        
    def add_to_group(self, email, group):
        self.email_map[email].add(group)

    def emails_in_groups(self, *groups):
        groups = set(groups)
        emails = set()
        for email, email_groups in self.email_map.items():
            # If there is at least a position that is intersection from 
            # the two sets
            # 'email_groups & groups' is a shortcut for sets intersection:
            if email_groups.intersection(groups):
                emails.add(email)
        return emails

    def send_mailing(self, subject, message, from_addr,
                     *groups, headers=None):
        emails = self.emails_in_groups(*groups)
        send_email(subject, message, from_addr, *emails, headers=headers)
        
    def save(self):
        with open(self.data_file, 'w') as file:
            for email, groups in self.email_map.items():
                file.write('{} {}\n'.format(email, ','.join(groups)))
        
    def load(self):
        self.email_map = defaultdict(set)
        try:
            with open(self.data_file) as file:
                for line in file:
                    # strip tira caracteres de espaco no inicio e fim
                    # a = ' lol teste som'
                    # a.strip(' lolm')
                    # saida:'teste s'                    
                    email, groups = line.strip().split(' ')
                    groups = set(groups.split(','))
                    self.email_map[email] = groups
        except IOError:
            pass    
    
    def __enter__(self):
        self.load()
        return self
    
    def __exit__(self, type, value, traceback):
        self.save()
