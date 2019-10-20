def count_iter(x, r=4.0, epsilon=1e-9, threshold=1e7):
	i = 0
	while x > epsilon:
		if i > threshold:
			return -1
		x = r * x * (1-x)
		i += 1
	return i

if __name__ == '__main__':
	for x in [round(x * 0.0001, 4) for x in range(0, 10000)]:
		count = count_iter(x)
		if (count >= 0):
			print(x, count)
