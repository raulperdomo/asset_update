import gspread, json
from twilio.rest import Client
from oauth2client.service_account import ServiceAccountCredentials

#Twilio Auth
with open('twilio_creds.json', 'r') as f:
    dict = json.load(f)
    twilio_sid = dict['twilio_sid']
    auth_token = dict['auth_token']
client = Client(twilio_sid, auth_token)

#Google Auth
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('assetupdater-37da94a236d9.json', scope)
gc = gspread.authorize(credentials)

#Open Google Sheet
book = gc.open('Investments')
rows_with_symbols = [2,3,4,5,7,8,9,10]
ws = book.get_worksheet(0)

#Craft Text Message
body = 'Symbol, Gain/Loss, Change %\n'
for row in rows_with_symbols:
    current_row = ws.row_values(row)
    body = body + current_row[0].ljust(6) + ' ' +current_row[6].rjust(4) +' '+ current_row[8]+'\n'
body += '\n' + ws.acell('F15').value + ' ' + ws.acell('I15').value +' '+ ws.acell('G15').value
print(body)


message = client.messages.create(
    to = '+17343581630',
    from_= '+17343596302',
    body=body)
print(message.sid)
