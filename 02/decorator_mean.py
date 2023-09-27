from time import time


def mean_last_calls(k: int = 1):
    def inner_mean(func):
        times = []
        call_num = 0

        def inner(*args, **kwargs):
            nonlocal times, call_num

            start_time = time.time()
            res = func(*args, **kwargs)
            res_time = time.time() - start_time

            if len(times) < k:
                times += [res_time]
            else:
                times = times[1:] + [res_time]

            call_num += 1
            mean_time = sum(times) / len(times)
            print(f'mean time for calls {call_num - len(times)} - {call_num} = {mean_time:.3f}')

            return res

        return inner

    return inner_mean
