import NetPerfTest as NetPerfTest
import threading
import xlsxwriter
import json
import time

rowNum=0
# 1: single, 2: multi, 3: both
testMode = 0

def runConcurrentTests():
    global tests, testMode
    if (testMode == 1):
        return
    for t in tests:
        th=threading.Thread(t.runTest())
        th.start()
        th.join()

    for t in tests:
        print('M' + t.getResult(i))
        writeToExcel(t, "M")

def runSingleTests():
    if (testMode == 2):
        return 
    for t in tests:
        t.runTest()
        print('S' + t.getResult(i))
        writeToExcel(t, "S")


def writeToExcel(t, mode):
    global testId, rowNum

    colNum=0
    worksheet.write(rowNum, colNum, testId)        
    colNum+=1
    worksheet.write(rowNum, colNum, mode)        
    colNum+=1
    worksheet.write(rowNum, colNum, i)
    colNum+=1
    for data in t.getResultForReporting():
        worksheet.write(rowNum, colNum, data)
        colNum+=1
    rowNum+=1

def genTestID():
    return time.strftime('%y%m%d%H%M')   

# initialize
# --------------------------------------------
testId = time.strftime('%y%m%d%H%M')
print("Test ID:" + testId)

workbook = xlsxwriter.Workbook('testResult'+testId+'.xlsx')
worksheet = workbook.add_worksheet()

with open('config.json') as f:
        config = json.load(f)

        port = config['param']['port']
        testMode = config['testMode']

        rounds = int(config['howManyrounds'])+1


# --------------------------------------------

test = NetPerfTest.NetPerfTest('pc', 'tv', port)
test.openConnections()
test2 = NetPerfTest.NetPerfTest('pc', 'tv2', str(int(port)+1))
test2.openConnections()

tests=list()
tests.append(test)
tests.append(test2)

# 1. TCP / pc --> tvs
for i in range(1,rounds):
    runConcurrentTests()
    runSingleTests()

# 2. TCP / tvs --> pc
test.changeConnection()
test2.changeConnection()

for i in range(1,rounds):
    runConcurrentTests()
    runSingleTests()

# 3. UDP / tvs --> pc
    
test.setProtocol('UDP')
test2.setProtocol('UDP')

for i in range(1,rounds):
    runConcurrentTests()
    runSingleTests()

# 4. UDP / pc --> tvs
    
test.changeConnection()
test2.changeConnection()

for i in range(1,rounds):
    runConcurrentTests()
    runSingleTests()

workbook.close()
test.closeConnections()
test2.closeConnections()

