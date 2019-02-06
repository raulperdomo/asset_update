import gspread, json, time, datetime
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
ws = book.get_worksheet(0)
epoch = datetime.date(1899,12,30)
today = datetime.date.today()
timedelt = today - epoch

#Hoping this sleep with allow the sheet to update values.
time.sleep(10)

#Grab column C to check if it has a number of shares owned, if so add it to list of rows to gather data from.
colC = ws.col_values(3)[1:]
colA = ws.col_values(1)
totalRow = colA.index('Total')+1
index = 2
rows_with_symbols = []

for row in colC:
    if row:
        rows_with_symbols.append(index)
    index += 1


#Craft Text Message
body = 'Symbol, Change %, Gain/Loss\n'
for row in rows_with_symbols:
    current_row = ws.row_values(row)
    body = body + current_row[0].ljust(6) + ' ' +current_row[6].rjust(4) +' '+ current_row[8]+'\n'
body += '\n' + ws.acell(f'F{totalRow}').value + ' ' + ws.acell(f'I{totalRow}').value +' '+ ws.acell(f'G{totalRow}').value

dayTotal = ws.acell(f'F{totalRow}').value
sheet2totalRow = book.get_worksheet(1).col_values(1).index('Total')+1
sheet2total = book.get_worksheet(1).acell(f'F{sheet2totalRow}').value
print(body)

#These lines create a running total on a different sheet that are grabbed to make a line chart
ws = book.get_worksheet(2)
rows = len(ws.col_values(1))
print(dayTotal)
print(float(dayTotal.strip('$').replace(',','')))

ws.update_acell(f'A{rows+1}', timedelt)
ws.update_acell(f'b{rows+1}', f'{dayTotal}')
ws.update_acell(f'c{rows+1}', f'{sheet2total}')
ws.update_acell(f'd{rows+1}', f"={float(dayTotal.strip('$').replace(',',''))}+{float(sheet2total.strip('$').replace(',',''))}")


''' Only uncomment this is you want to send texts. 
message = client.messages.create(
    to = '+17343581630',
    from_= '+17343596302',
    body=body)
print(message.sid)
'''
