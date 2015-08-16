import json
from oauth2client.client import SignedJwtAssertionCredentials

from thirdparty import gspread

json_key = json.load(open('CodeChallenge-0fc1883d1a1c.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)


# Login with your Google account
gc = gspread.authorize(credentials)

# open a sheet by its key
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1PmHHHjyvoSg-erK_CvMmKCtYsezHOGHvoUu6EiZWutM/edit#gid=0')

puzzles_worksheet = spreadsheet.worksheet("Puzzles")
problems_worksheet = spreadsheet.worksheet("Problems")
attempts_worksheet = spreadsheet.worksheet("Attempts")

puzzle_data = puzzles_worksheet.get_all_values()

#attempts_worksheet.append_row(["puzz1_easy", "Matt's Team", 61])


#cell_list = attempts_worksheet.range('A2:E5')

attempts_worksheet.resize(1, 5)

'''
rows = 1000
columns = 5

for row in xrange(0, rows):
	for column in xrange(0, columns):
		attempts_worksheet.update_cell(row, column, '')
'''