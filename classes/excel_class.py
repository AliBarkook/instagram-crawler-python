
# ? import excel module
import xlsxwriter 

class Excel_Class():

    """

    |---------------------------------------------------------------------
    |                                                                    |
    |     excel Class                                                    |
    |                                                                    |
    |---------------------------------------------------------------------
    |                                                                    |
    |   1 - initial Class with excel name and sheet name                 |
    |                                                                    |
    |   2 - create excel file and worksheet                              |
    |                                                                    |
    |   3 - close excel                                                  |
    |                                                                    |
    |   4 - store comment data in excel row                              |
    |                                                                    |
    ----------------------------------------------------------------------

    """
    # ? -> 1
    def __init__(self, excelName, sheetName):

        self.excelName = excelName
        self.sheetName = sheetName
        self.coursePropTitleList = ['نام اکانت', 'متن کامنت', 'نویسنده کامنت', 'تعداد لایک ها']

        self.excelFile = xlsxwriter.Workbook(excelName)
        self.worksheet = self.excelFile.add_worksheet(sheetName)
    # ? -> 2
    def initExcel(self):
        col = 0
        for title in self.coursePropTitleList:

            self.worksheet.write(0, col, title)
            col += 1
    # ? -> 3
    def closeExcel(self):
        while True:
            try:
                self.excelFile.close()
                print('excel file closed')
                break
            except xlsxwriter.exceptions.FileCreateError as e:
                decision = input("Exception caught in workbook.close(): %s\n"
                                "Please close the file if it is open in Excel.\n"
                                "Try to write file again? [Y/n]: " % e)
                if decision != 'n':
                    continue
    # ? -> 4
    def storeDataInExcel(self, row, col, course):
        try:
            worksheet = self.excelFile.get_worksheet_by_name(self.sheetName)
            for prop in course.return_prop_as_list():
                worksheet.write(row, col, prop)
                col += 1
        except:
            print('can not write to excel file comment number' + str(row))