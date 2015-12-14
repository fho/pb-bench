cpu_threads = 0  # Set to 0, to use all available CPUs

# most benchmarks need to run more than 1 time to produce a reasonable
# result!
benchmarks = {
    "ping-rtt":       {"min_runs": 5, "max_runs": 200},
    "cp":             {"min_runs": 5,  "max_runs": 8},
}

# repeatedly run a benchmark until the confidence interval is smaller than X
# percent of the median result
conf_interval_goal_pct = 10
