import asyncio
import time


# allows to limit the amount of times a function is called per time interval.
class rateLimiter:
    def __init__(self, rate_limit, time_interval):
        self.rate_limit = rate_limit
        self.time_interval = time_interval
        self.tokens = rate_limit
        self.last_time = time.time()

    async def __aenter__(self):
        await self.wait_for_token()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb): # a linter can tell these are not accessed but they got to stay
        pass

    async def wait_for_token(self):
        while self.tokens <= 0:
            elapsed_time = time.time() - self.last_time
            if elapsed_time >= self.time_interval:
                self.tokens = self.rate_limit
                self.last_time = time.time()
            # this determines the rate at which the rate checker works. also frees up the CPU and 
            # the program continues from the previous call 
            else:
                await asyncio.sleep(0.1)

        self.tokens -= 1
