""" Simulation server for Maxwell.

    Executes uploaded jobs.

    Consists of an infinite loop which does the following:
    1.  Find the oldest job.
    2.  Run the solver on it.
    3.  Repeat.
"""

import os, time
import maxwell_config
import subprocess, shlex

def find_oldest_job():
    req = maxwell_config.list_requests() # Get the requests.
    if not req:
        return None

    req_with_time = {}
    for r in req:
        req_with_time[r] = os.stat(maxwell_config.path + r).st_ctime

    return min(req_with_time) # Run this job.

if __name__ == '__main__':
    path_to_solver_dir = os.path.abspath(__file__).replace( \
                            __file__.split('/')[-1], 'maxwell-solver') + '/'
    while True:
        req = find_oldest_job()
        job = req.rstrip('.request')
        if job:
            print "Solving %s..." % job
            # os.remove(maxwell_config.path + job)
            return_code = subprocess.call(shlex.split( \
                                           "mpirun -n 3 python " + \
                                           path_to_solver_dir + "fdfd.py " + \
                                           maxwell_config.path + job))
               
#             try:
#                 # Solve it!
#                subprocess.check_output(shlex.split( \
#                    "mpirun -n 3 python maxwell-solver/fdfd.py " + path + job, \
#                    stderr=subprocess.STDOUT))
#             except:
#                 pass
        break
        time.sleep(1)


