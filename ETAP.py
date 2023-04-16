import openpyxl
import xlwt

class ETAP_Lump():
    # Empty initialization
    def __init__(self):
        self._wb = None
        self._xlwt_wb = None
        self._timestep = [0, 15, 0] # HH:MM:SS
        self._rows = [] # row column syntax
        self._gen_header_row()
    
    # Calculate time step used in the current object
    def _calc_step(self):
        self._timestep = [self._rows[1][10] - self._rows[2][10],
                         self._rows[1][11] - self._rows[2][11],
                         self._rows[1][12] - self._rows[2][12]]
    
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
                   Humidity=None, Temp=None, Wind=None, Irradiance=None):
        data = [P, Q, PF, V, Angle, Humidity, Temp, Wind, 
                Irradiance, Hour, Min, Sec, Date]
        tmp_row = []
        for i in range(0, len(P)):
            for j in range(0, 13):
                if data[j] != None:
                    tmp_row.append(data[j][i] if data[j][i] != None else '')
                else:
                    tmp_row.append('')
            self._rows.append(tmp_row[::])
            tmp_row = []
    
    # Save the current data in an Excel file, either xlsx or xls
    def save(self, filename, writer='openpyxl'):
        if writer == 'openpyxl':
            self._wb.save(filename)
        elif writer == 'xlwt':
            if self._xlwt_wb != None:
                self._xlwt_wb.save(filename)
            else:
                self.write_xlwt_wb()
                try:
                    self.save(filename, writer='xlwt')
                except PermissionError:
                    print("Couldn't write to file, close it before running the program")

    # Generate data for an xls file using xlwt
    def write_xlwt_wb(self):
        self._xlwt_wb = xlwt.Workbook()
        ws = self._xlwt_wb.add_sheet('Sheet1')
        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'yyyy-mm-dd hh:mm:ss'
        for i in range(0, len(self._rows)-1):
            for j in range(0, 13):
                if j == 12:
                    ws.write(i,j,self._rows[i][j],date_format)
                else:
                    ws.write(i,j,self._rows[i][j])

# Load lump data from an Excel file, currently only tested for xlsx files
def load_lump(filename):
    _lump = ETAP_Lump()
    _lump._wb = openpyxl.load_workbook(filename)
    _ws = _lump._wb.active
    P = []; Q = []; PF = []; V = []; Angle = []; Humidity = []; Temp = []
    Wind = []; Irradiance = []; Hour = []; Min = []; Sec = []; Date = []
    for row in range(2, _ws.max_row):
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
                     Temp,Wind,Irradiance)
    _lump._calc_step()
    return(_lump)
