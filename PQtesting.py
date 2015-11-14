from Queue import PriorityQueue

#Max size of PQ
n = 11
PQ = PriorityQueue(n)
PQ.put(10)
PQ.put(9)
PQ.put(5)
PQ.put(4)
PQ.put(1)
PQ.put(3)
PQ.put(8)
PQ.put(0)
PQ.put(7)
PQ.put(6)
PQ.put(2)

for i in range(0,n):
	a = PQ.get()
	print(a)