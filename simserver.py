""" Simulation server for Maxwell.

    Executes uploaded jobs.

    Consists of an infinite loop which does the following:
    1.  Find the oldest job.
    2.  Run the solver on it.
    3.  Repeat.
"""

import os, time
import maxwell_config

def find_oldest_job():
    req = maxwell_config.list_requests() # Get the requests.
    if not req:
        return None

    req_with_time = {}
    for r in req:
        req_with_time[r] = os.stat(maxwell_config.path + r).st_ctime

    return min(req_with_time) # Run this job.

if __name__ == '__main__':
    while True:
        job = find_oldest_job()
        if job:
            print "Solving %s..." % job
            os.remove(maxwell_config.path + job)
            try:
                # Solve it!
                pass
            except:
                pass

        time.sleep(1)


