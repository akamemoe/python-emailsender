### EmailSender

simply sending email via command line.

##### Usage

configure your own smtp server infomation first, see `email.ini.example` for example.
```
./emailsender.py -r recipient@gmail.com -s "this is subject" -c "this email content" -f transactions.xls
```