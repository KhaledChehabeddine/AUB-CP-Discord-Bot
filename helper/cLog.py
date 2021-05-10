from helper.cTime import MyDate

def elog(ex, stk):
  fs  = open("./logs/error_log.txt", "a")
  frame = str(stk[0][0]).strip('<>').split(',')
  path = frame[1][8:-1].split('/')
  _file = '/'.join(path[3:])
  call = frame[3][6:] + '()'
  fs.write(MyDate().footer() + " " + _file + " CALL " + call + " ERROR-MSG " + str(ex) + '\n') 
  fs.close()

def alog(ex):
  fs  = open("./logs/activity_log.txt", "a")
  fs.write(MyDate().footer() + " " + str(ex) + '\n') 
  fs.close()