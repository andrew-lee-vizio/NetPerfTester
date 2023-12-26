import NetPerfTest as NetPerfTest

test = NetPerfTest.NetPerfTest('pc', 'tv2')
test.openConnections()

for i in range(1,6):
    test.runTest()
    print(test.getResult())

test.setProtocol('UDP')

for i in range(1,6):
    test.runTest()
    print(test.getResult(i))

test.changeConnection()
# test.setProtocol('TCP')

for i in range(1,6):
    test.runTest()
    print(test.getResult(i))

test.setProtocol('TCP')
for i in range(1,6):
    test.runTest()
    print(test.getResult(i))

test.closeConnections()