#!/usr/bin/env python

import config
import multiprocessing
import datetime
import logging
import os
import signal
import sys
from benchmarks.benchmark import Benchmark

__author__ = "Fabian Holler <fabian.holler@profitbricks.com>"

sys.path.append("lib")
benchmarks_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              "benchmarks")


def get_benchmark(name):
    benchmark_dir = os.path.join(benchmarks_dir, name)
    return Benchmark(benchmark_dir)


def load_benchmarks():
    for benchmark in config.benchmarks.keys():
        b = get_benchmark(benchmark)
        log.info("Preparing Benchmark: %s" % b.name)
        b.prepare()

        config.benchmarks[benchmark]["cls"] = b
        config.benchmarks[benchmark]["status"] = "OK"


def bench_results_to_csv():
    with open(result_file, 'w') as f:
        f.write("#benchmark;average;median;min;max;std_dev_pct;"
                "conf_interval99.9_pct;conf_interval99.9_start;"
                "conf_interval99.9_end;value_cnt\n")
        for benchmark in config.benchmarks.values():
            if "cls" not in benchmark:  # can happen if strg+c was pressed
                                        # before all benchmarks were loaded
                continue
            b = benchmark['cls']
            f.write("%s;%.3f;%.3f;%.3f;%.3f;%.3f;%.3f;%.3f;%.3f;%s\n" %
                    (b.name, b.avg, b.median, b.min, b.max, b.std_dev_pct,
                     b.confidence_intvl_pct, (b.avg - b.confidence_intvl),
                     (b.avg + b.confidence_intvl), b.runs))
    log.info("Benchmark results wrote to: %s" % result_file)


def run_benchmarks():
    log.info("Starting benchmarking...")
    benchmarking_finished = False
    while not benchmarking_finished:
        benchmarking_finished = True
        for benchmark in config.benchmarks.values():
            # skip benchmarks that failed one time, to prevent that we run
            # endless because a benchmark fails all the time..
            if benchmark["status"] == "ERROR":
                continue
            b = benchmark['cls']

            if "max_runs" in benchmark and b.runs >= benchmark["max_runs"]:
                break
            if (b.runs >= benchmark['min_runs'] and
                    b.confidence_intvl_pct <= config.conf_interval_goal_pct):
                break

            try:
                b.run(config.cpu_threads)
                log.info(("[{0:<15}] avg: {1:>10.3f}|"
                          " std. dev.: {2:>10.3f}%| confidence intvl 99.9:"
                          " [{3:<10.3f},{4:>10.3f}]|").
                         format(b.name, b.avg, b.std_dev_pct,
                                (b.avg - b.confidence_intvl),
                                (b.avg + b.confidence_intvl)))
            except Exception as e:
                log.error("%s failed: %s" % (b.name, e))
                benchmark["status"] = "ERROR"
            benchmarking_finished = False


def exit(signum, stackframe):
    bench_results_to_csv()
    os.killpg(0, signal.SIGKILL)  # ensure all created processes terminate
    sys.exit(1)


# main
logging.basicConfig(level=logging.INFO, format="%(message)s",
                    datefmt='%m-%d %H:%M')
log = logging.getLogger(__name__)

if len(sys.argv) > 1:
    if sys.argv[1] == "-h":
        print("usage: %s [log-file]" % sys.argv[0])
        print("\nIf the log file isn't specified the results are logged to"
              " pb-bench-<date>.log")
        sys.exit(0)
    result_file = os.path.realpath(sys.argv[1])
else:
    ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    result_file = os.path.realpath("pb-bench-%s.log" % ts)

log.info("Results are logged to: %s" % result_file)

if config.cpu_threads == 0:
    config.cpu_threads = multiprocessing.cpu_count()

os.setpgrp()

# write logfile and terminate all subprocesses on SIGINT, SIGTERM
signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)

load_benchmarks()

run_benchmarks()
bench_results_to_csv()
log.info("Benchmarks finished")
