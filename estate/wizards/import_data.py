import base64
import binascii
import csv
import io
import tempfile
from odoo.exceptions import UserError
import xlrd
from odoo import models, fields


class ImportData(models.TransientModel):
    # _inherit = 'base_import.import'
    _name = 'import.data'

    id = fields.Integer(string='Id')
    name = fields.Char(string='Name')
    data_file = fields.Binary(string='File')
    file_name = fields.Char("file name")




    def import_data(self):
        if self.file_name.endswith('.xlsx') or self.file_name.endswith('.xls'):
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.data_file))
            fp.seek(0)
            wb = xlrd.open_workbook(fp.name)
            sheet = wb.sheet_by_index(0)
            for row in range(sheet.nrows):
                if row >=1:
                    row_vals = sheet.row_values(row)
                    print(row_vals)
                    existing_record = self.env['estate.property.tag'].search([('name','=',row_vals[1])])
                    if existing_record:
                        existing_record.write({
                            'ref':int(row_vals[0]),
                            'name': row_vals[1]
                        })
                        print('record update')
                    else:
                        self.env['estate.property.tag'].create({
                            'ref': int(row_vals[0]),
                            'name': row_vals[1]
                        })
                        print('record create')
                else:
                    print('there is no record in excel file')
        elif self.file_name.endswith('.csv'):
            if self.data_file:
                data = base64.b64decode(self.data_file)
                file_input = io.StringIO(data.decode("utf-8"))
                file_input.seek(0)
                reader = csv.reader(file_input)
                for row in reader:
                    existing_record = self.env['estate.property.tag'].search([('name','=',row[1])])
                    print(existing_record)
                    if existing_record:
                        existing_record.write({
                            'ref': row[0],
                            'name': row[1]
                        })
                        print('record update')
                    else:
                        self.env['estate.property.tag'].create({
                            'ref': row[0],
                            'name': row[1]
                        })
                        print("record create")
            else:
                print('there is no record in csv file')
        else:
            raise UserError("File format not supported. Only CSV and XLS files are allowed.")

