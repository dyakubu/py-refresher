import time
import dis
from functools import wraps

def decorator(fn):
	def wrapper(*args, **kwargs):
		start = time.perf_counter()
		print(f"This is a decrator around {fn.__name__}, with args = {args} and kwargs = {kwargs}")
		res = fn(*args, **kwargs)
		print(f"After execution, time taken: {time.perf_counter() - start}")
		return res
	return wrapper

@decorator
def add(a,b):
	return a + b

dis.dis(decorator)
print(add(1,2))
