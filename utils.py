from openpyxl.worksheet.worksheet import Worksheet

def optimum(sheet : Worksheet):
  rows, columns = sheet.max_row, sheet.max_column
  last_process = sheet.cell(column=columns, row = 1).value
  frames, fails, lasted = rows - 2, 0, 0
  previous_row = [None]

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

  return 'Optimo', columns - 1, fails
      

def fifo(sheet : Worksheet):
  rows, columns = sheet.max_row, sheet.max_column
  frames, fails, lasted = rows - 2, 0, 0
  previous_row = [None]

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
      if None not in previous_row:
        assert new_value == row[lasted % frames], 'Este no es el algoritmo fifo'
        lasted += 1

    previous_row = row

  return 'FIFO', columns - 1, fails

def not_recently_used(sheet : Worksheet):
  rows, columns = sheet.max_row, sheet.max_column
  fails = 0
  previous_row = [None]
  last_used = []

  for cols in sheet.iter_cols(min_col = 2, max_col = columns, max_row = rows):
    row = []
    for cell in cols:
      if cell.row == 1:
        new_value = cell.value
        if new_value in last_used:
          last_used.pop(last_used.index(new_value))
        last_used.append(new_value)

      if 1 < cell.row < rows:
        row.append(cell.value)

      if cell.row == rows:
        if cell.value is not None:
          fails += 1

    if new_value not in previous_row:
      if None not in previous_row:
        deleted = last_used.pop(0)
        assert deleted not in row, 'No es el algoritmo no usadas recientemente'
    previous_row = row

  return 'No usadas recientemente', columns - 1, fails
  