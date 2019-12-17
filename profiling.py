import cProfile
import logparser
import tempfile
ENTRIES=30
PIDS=5000
print("Analyzing logfile with {} pids with {} entries each".format(PIDS, ENTRIES))
with tempfile.NamedTemporaryFile(mode="w+t") as f:
    for iteration in range(ENTRIES):
        for pid in range(PIDS):
            f.writelines("2019-4-2 13:33:56 [{}] iteration {}\n".format(pid, iteration))
    f.writelines("2019-4-2 13:33:56 [1000] ERROR: error occured\n")
    f.seek(0)
    cProfile.run('logparser.print_errors("{}")'.format(f.name))
