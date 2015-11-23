import sys
import xlrd, csv

"""
	A simple XLS to CSV converter with Unicode support
	by Paul Shiryaev, DBRS 2013-2015
"""
def csv_from_excel(filename, sheetname, skiprownum):

	if skiprownum > 0:
		print "Rows to skip: ", skiprownum

	wb = xlrd.open_workbook(filename)
	worksheet = wb.sheet_by_name(sheetname)
	csv_filename = open(''.join([sheetname,'.csv']), 'wb')
	wr = csv.writer(csv_filename, quoting=csv.QUOTE_ALL)
	rc = 0

	for rownum in xrange(worksheet.nrows):
		if rownum >= skiprownum:
			wr.writerow([unicode(entry).encode("utf-8") for entry in worksheet.row_values(rownum)])
			rc = rc + 1

	print "Saved " + str(rc) + " rows from " + filename + "$" + sheetname + " to " + csv_filename.name
	csv_filename.close()

if len(sys.argv) > 2:
	filename = str(sys.argv[1])
	sheetname = str(sys.argv[2])
	skiprowcount = 0
	if len(sys.argv) > 3:
		skiprowcount = int(str(sys.argv[3]))
	csv_from_excel(filename, sheetname, skiprowcount)
	sys.exit(0)
else:
	print "Usage: xls2csv.py {file name.xls} {sheet name} [{count of rows to skip from the top - default is 0}]"
	sys.exit(1)


