PB-Bench
========
(C) Profitbricks GmbH, 2013
Licence: LGPL-3

PB-Bench is a benchmark suite for Linux.

The application focuses on being:
* fast to deploy and to run,
* using a statistical indicator to determine the number of runs for a
  benchmark,
* providing staticial data about the benchmark results,
* being simply to extend with additional benchmarks.

This version of pb-bench comes only with 2 benchmarks as examples.
To get a full-fledged benchmark suite you have to extend the benchmark suite.

Quick Start
-----------
 * Optional: If are remote machine should be benchmarked, run ./make_tar.sh and
	 copy pb-bench.tar to the target host.
 * run pb-bench.py


Dependencies
------------
All test binaries included are for 64-bit Linux systems.
If you want to run these on a non-64-bit system you have to exchange the
binaries with fitting ones for your system.

General dependencies:
* python
* tar


Configuration
-------------
The configuration is done in the config.py file.
Each benchmark runs at least <min_runs times> times until the relative
confidence interval of the result becomes smaller than <conf_interval_goal_pct>
or <max_runs> was reached.


How to add new benchmarks
=========================
* Create a sub-directory for your benchmark in benchmarks/.
* If benchmark must be prepared before it can be run, create a a executable
  benchmarks/<NAME>/prepare.sh file
* Create a executable benchmarks/<NAME>/run.sh file. The script must write the
  result to the file $LOG_RESULT.
* Add a configuration entry to config.py. The benchmark name is the name of the
  directory in benchmarks/.


Benchmark files
---------------
* prepare.sh: The script is executed before the benchmark is run. It can prepare
              the environment by e.g. downloading a program required for the
              benchmark

* run.sh: This file starts a benchmark run. The result of the file must be
          written to the file defined in the environment variable $LOG_FILE.
          The $LOG_FILE variable is set by pb-bench.py and contains a path to a
          temporary result file. Only one result value must written to $LOG_FILE.
