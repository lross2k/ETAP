import openpyxl   # For Excel files (.xlsx)
import xlwt, xlrd # For old Excel files (.xls)
from datetime import datetime
import time

# Class with methods and fields related to generating and manipulating ETAP Lumped files
class ETAP_Lump():
    # Empty initialization
    def __init__(self):
        self._last_modified = time.localtime()
        self._last_cache_xlwt = time.localtime()
        self._last_cache_openpyxl = time.localtime()
        self._wb = None
        self._xlwt_wb = None
        self._xlrd_wb = None
        self.date_str = "%Y-%d-%m %H:%M:%S"
        self._timestep = None # Y-d-m HH:MM:SS
        self._rows = [] # row column syntax
        self._gen_header_row()
    
    # Calculate time step used in the current object
    def _calc_step(self):
        self._timestep = [self._rows[2][9] - self._rows[1][9],
                     self._rows[2][10] - self._rows[1][10],
                     self._rows[2][11] - self._rows[1][11]]
    
    # Generate the HEADER of Lump file
    def _gen_header_row(self):
        self._rows = [['P(MW)','Q(Mvar)','PF%','V(p.u.)','Angle', 'Humidity','Temp C',
                       'Wind(m/s)','Irradiance(W/m^2)','Hour','Min','Seconds','Date']]

    # Allow string conversion of the Lump structure for functions like str(), print()
    def __str__(self):
        longest = 0
        for row in self._rows:
            for col in row:
                longest = len(str(col)) if len(str(col)) > longest else longest
        string = ''
        for row in self._rows:
            for col in row:
                if col != '':
                    string = string + str(col) + ' '*(longest - len(str(col)))
                else:
                    string = string + ' '*longest
            string = string + '\n'
        return(string)
    
    # Set the current values for all items in the rows
    def set_values(self, P, Q, PF, Hour, Min, Sec, Date, V=None, Angle=None, 
                   Humidity=None, Temp=None, Wind=None, Irradiance=None, date_str=None):
        data = [P, Q, PF, V, Angle, Humidity, Temp, Wind, 
                Irradiance, Hour, Min, Sec, Date]
        tmp_row = []
        if date_str:
            self.date_str = date_str
        for i in range(0, len(P)):
            for j in range(0, 13):
                if data[j] != None:
                    if j == 12:
                        if type(data[j][i]) == str:
                            tmp_row.append(datetime.strptime(data[j][i], self.date_str) if data[j][i] != None else '')
                        else:
                            tmp_row.append(data[j][i] if data[j][i] != None else '')
                    else:
                        tmp_row.append(data[j][i] if data[j][i] != None else '')
                else:
                    tmp_row.append('')
            self._rows.append(tmp_row[::])
            tmp_row = []
        self._calc_step()
    
    # Save the current data in an Excel file, either xlsx or xls
    def save(self, filename, writer='openpyxl'):
        if writer == 'openpyxl':
            if self._wb != None and  self._last_cache_openpyxl > self._last_modified:
                self._wb.save(filename)
            else:
                self._write_openpyxl_wb()
                try:
                    self.save(filename)
                except PermissionError:
                    print("Couldn't write to file, close it before running the program")
        elif writer == 'xlwt':
            if self._xlwt_wb != None and self._last_cache_xlwt > self._last_modified:
                self._xlwt_wb.save(filename)
            else:
                self._write_xlwt_wb()
                try:
                    self.save(filename, writer='xlwt')
                except PermissionError:
                    print("Couldn't write to file, close it before running the program")

    # Generate data for an xls file using xlwt
    def _write_xlwt_wb(self):
        self._xlwt_wb = xlwt.Workbook()
        ws = self._xlwt_wb.add_sheet('Sheet1')
        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'yyyy-mm-dd hh:mm:ss'
        for i in range(0, len(self._rows)):
            for j in range(0, 13):
                if j == 12:
                    ws.write(i,j,self._rows[i][j],date_format)
                else:
                    ws.write(i,j,self._rows[i][j])
        self._last_cache_xlwt = time.localtime()
                
    # Generate data for an xlsx file using openpyxl
    def _write_openpyxl_wb(self):
        self._wb = openpyxl.Workbook()
        ws = self._wb.active
        for i in range(1, len(self._rows)+1):
            for j in range(1, 14):
                try:
                    ws.cell(row=i,column=j).value = self._rows[i-1][j-1]
                except TypeError:
                    print(self._rows)
        self._last_cache_openpyxl = time.localtime()
    
    def change_time_step(self, time_step):
        if not self._timestep:
            print("No data has been added yet")
            return
        _rows_copy = self._rows[::]
        self._gen_header_row() 
        factor = (self._timestep[0]*60 + self._timestep[1]) / (time_step[0]*60 + time_step[1])
        tmp_row = []
        if type(factor) == float:
            step = int(1/factor)
            for i in range(1, len(_rows_copy), step):
                for j in range(0, 13):
                    tmp_row.append(_rows_copy[i][j])
                self._rows.append(tmp_row[::])
                tmp_row = []
        else:
            for i in range(1, len(_rows_copy)):
                for k in range(0,factor):
                    for j in range(0, 13):
                        if j == 10:
                            tmp_row.append(time_step[1]*k)
                        else:
                            tmp_row.append(_rows_copy[i][j])
                    self._rows.append(tmp_row[::])
                    tmp_row = []
        self._timestep = time_step
        self._last_modified = time.localtime()

# Load lump data from an Excel file using openpyxl for xlsx files and xlrd for xls files
def load_lump(filename, reader='openpyxl', date_str=None):
    _lump = ETAP_Lump()
    if reader == 'openpyxl':
        _lump._wb = openpyxl.load_workbook(filename)
        _ws = _lump._wb.active
        P = []; Q = []; PF = []; V = []; Angle = []; Humidity = []; Temp = []
        Wind = []; Irradiance = []; Hour = []; Min = []; Sec = []; Date = []
        for row in range(2, _ws.max_row+1):
            P.append(         _ws.cell(row=row, column=1).value)
            Q.append(         _ws.cell(row=row, column=2).value)
            PF.append(        _ws.cell(row=row, column=3).value)
            V.append(         _ws.cell(row=row, column=4).value)
            Angle.append(     _ws.cell(row=row, column=5).value)
            Humidity.append(  _ws.cell(row=row, column=6).value)
            Temp.append(      _ws.cell(row=row, column=7).value)
            Wind.append(      _ws.cell(row=row, column=8).value)
            Irradiance.append(_ws.cell(row=row, column=9).value)
            Hour.append(      _ws.cell(row=row, column=10).value)
            Min.append(       _ws.cell(row=row, column=11).value)
            Sec.append(       _ws.cell(row=row, column=12).value)
            Date.append(      _ws.cell(row=row, column=13).value)
        _lump.set_values(P,Q,PF,Hour,Min,Sec,Date,V,Angle,Humidity,
                         Temp,Wind,Irradiance,date_str=date_str)
    elif reader == 'xlrd':
        _lump._xlrd_wb = xlrd.open_workbook(filename)
        _ws = _lump._xlrd_wb.sheet_by_index(0)
        P = []; Q = []; PF = []; V = []; Angle = []; Humidity = []; Temp = []
        Wind = []; Irradiance = []; Hour = []; Min = []; Sec = []; Date = []
        for row in range(1, _ws.nrows):
            P.append(         _ws.cell_value(rowx=row, colx=0))
            Q.append(         _ws.cell_value(rowx=row, colx=1))
            PF.append(        _ws.cell_value(rowx=row, colx=2))
            V.append(         _ws.cell_value(rowx=row, colx=3))
            Angle.append(     _ws.cell_value(rowx=row, colx=4))
            Humidity.append(  _ws.cell_value(rowx=row, colx=5))
            Temp.append(      _ws.cell_value(rowx=row, colx=6))
            Wind.append(      _ws.cell_value(rowx=row, colx=7))
            Irradiance.append(_ws.cell_value(rowx=row, colx=8))
            Hour.append(      _ws.cell_value(rowx=row, colx=9))
            Min.append(       _ws.cell_value(rowx=row, colx=10))
            Sec.append(       _ws.cell_value(rowx=row, colx=11))
            Date.append(      _ws.cell_value(rowx=row, colx=12))
        _lump.set_values(P,Q,PF,Hour,Min,Sec,Date,V,Angle,Humidity,
                         Temp,Wind,Irradiance,date_str=date_str)
    return(_lump)
