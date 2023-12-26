import NetPerfTest as NetPerfTest
import threading

def runTests(tests):
    for t in tests:
        th=threading.Thread(t.runTest())
        th.start()
        th.join()

    for t in tests:
        print(t.getResult(i))


# --------------------------------------------

test = NetPerfTest.NetPerfTest('pc', 'tv')
test.openConnections()
test2 = NetPerfTest.NetPerfTest('pc', 'tv2', '5002')
test2.openConnections()

tests=list()
tests.append(test)
tests.append(test2)

for i in range(1,6):
    runTests(tests)

test.setProtocol('UDP')
test2.setProtocol('UDP')

for i in range(1,6):
    runTests(tests)

test.changeConnection()
test2.changeConnection()
# test.setProtocol('TCP')

for i in range(1,6):
    runTests(tests)

test.setProtocol('TCP')
test2.setProtocol('TCP')

for i in range(1,6):
    runTests(tests)

test.closeConnections()
test2.closeConnections()
