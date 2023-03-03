from openpyxl.worksheet.worksheet import Worksheet

def optimum(sheet : Worksheet):
  rows, columns = sheet.max_row, sheet.max_column
  last_process = sheet.cell(column=columns, row = 1).value
  lasted = 0
  previous_row = [None]
  frames, fails = rows - 2, 0

  for cols in sheet.iter_cols(min_col = 2, max_col = columns, max_row = rows):
    row = []
    for cell in cols:
      if cell.row == 1:
        new_value = cell.value

      if 1 < cell.row < rows:
        row.append(cell.value)

      if cell.row == rows:
        if cell.value is not None:
          fails += 1

    if new_value not in previous_row:
      try:
        if None not in previous_row:
          if previous_row.index(last_process) != row.index(new_value): 
            assert False, 'Este no es el algoritmo optimo'
      except ValueError:
        assert previous_row[lasted % frames] != row[lasted % frames], 'Este no es el algoritmo optimo'
        lasted += 1
    previous_row = row

  return 'Optimo', columns, fails
      
