from datetime import datetime, timedelta

offset = 3

def get_in_date_format(st):
  dt = st.split('/')
  month = dt[0]
  d = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
      'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09',
      'Oct': '10', 'Nov': '11', 'Dec': '12'}
  month = d[dt[0]]
  return month + '/' + '/'.join(dt[1:])

def current_date():
    dt = datetime.now()
    dt += timedelta(hours = offset)
    return str(dt.month) + '/' + str(dt.day) + '/' + str(dt.year) + ' ' + str(dt.hour) + ':' + str(dt.minute)

class MyDate():
  month, day, year = int(), int(), int()
  hour, minute = int(), int()

  def days_in_month(self):
    if (self.month == 2):
      if (self.year % 4 == 0 and self.year % 100 != 0): return 29
      if (self.year % 400 == 0): return 29
      return 28
    if (self.month in [4, 6, 9, 11]): return 30
    return 31

  def __init__(self, st = current_date()):
    d = [int(x) for x in st.split(' ')[0].split('/')]
    t = [int(x) for x in st.split(' ')[1].split(':')[:2]]

    self.month, self.day, self.year = d[0], d[1], d[2]
    self.hour, self.minute = t[0], t[1]
    
  def is_valid(self):
    try:
      if not (1 <= self.month <= 12): return False
      if not (1 <= self.day <= 31): return False
      if not (2021 <= self.year): return False

      if (self.day > self.days_in_month()): return False

      if not (0 <= self.hour <= 23): return False
      if not (0 <= self.minute <= 59): return False

      today = MyDate()

      if (self.year < today.year or self.year > today.year + 1): return False
      if (self.year == today.year and self.month < today.month): return False
      if (self.year == today.year and self.month == today.month and self.day < today.day): return False

      is_today = (self.year == today.year and self.month == today.month and self.day == today.day)
      if (is_today and self.hour < today.hour): return False
      if (is_today and self.hour == today.hour and self.minute < today.minute): return False

      return True

    except Exception:
      return False

  def add(self, duration):
    dt = datetime(self.year, self.month, self.day, self.hour, self.minute)
    dt += timedelta(hours = duration)
    d = [int(x) for x in str(dt).split(' ')[0].split('-')]
    self.year, self.month, self.day = d[0], d[1], d[2]
    t = [int(x) for x in str(dt).split(' ')[1].split(':')[:2]]
    self.hour, self.minute = t[0], t[1]
    return str(self)

  def delta(self):
    dt = datetime(self.year, self.month, self.day, self.hour, self.minute)
    ct = datetime.now()
    ct += timedelta(hours = offset)
    return int((dt - ct).total_seconds() / 60)

  def __lt__(self, d2):
    dt = datetime(self.year, self.month, self.day, self.hour, self.minute)
    ct = datetime(d2.year, d2.month, d2.day, d2.hour, d2.minute)
    return (int((dt - ct).total_seconds() / 60) < 0)

  def __str__(self):
    m, d, y = str(self.month), str(self.day), str(self.year)
    h, mn = str(self.hour), str(self.minute)
    if (self.month < 10): m = "0" + m
    if (self.day < 10): d = "0" + d
    if (self.hour < 10): h = "0" + h
    if (self.minute < 10): mn = "0" + mn
    return m + "/" + d + "/" + y + " " + h + ":" + mn

  def footer(self):
    return str(self).split()[0] + ' at ' + str(self).split()[1]