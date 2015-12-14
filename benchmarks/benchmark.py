import os
import tempfile
import stat
from lib.cmd_utils import *
from lib.statistic_utils import *

__author__ = "Fabian Holler <fabian.holler@profitbricks.com>"

log = logging.getLogger(__name__)


class BenchmarkError(Exception):
    wrapped_exception = None
    msg = ""

    def __init__(self, msg, wrapped_exception=None):
        self.wrapped_exception = wrapped_exception
        self.msg = msg

    def __str__(self):
        if not self.wrapped_exception:
            return "%s" % self.msg
        return "%s\n%s" % (self.msg, self.wrapped_exception)


class Benchmark(object):
    def __init__(self, benchmark_path):
        self._path = benchmark_path
        if not os.path.isdir(self._path):
            raise BenchmarkError("Benchmark %s doesn't exist" % benchmark_path)

        self.name = os.path.basename(benchmark_path)

        self._run_file = os.path.join(benchmark_path, "run.sh")
        if not os.path.exists(self._run_file):
            raise BenchmarkError("No run file (%s) found for Benchmark %s" %
                                 (self._run_file, self.name))

        self._prepare_file = os.path.join(benchmark_path, "prepare.sh")
        self.results = []
        self.runs = 0

        self._stats_outdated = False
        self._avg = float('nan')
        self._median = float('nan')
        self._std_dev = float('nan')
        self._min = float('nan')
        self._max = float('nan')
        self._confidence_intvl = float('nan')

    def _chmod755(self, file):
        """Sets permission of a file to 755."""
        os.chmod(file, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH |
                 stat.S_IRGRP | stat.S_IRUSR | stat.S_IROTH | stat.S_IWUSR)

    def prepare(self):
        if os.path.exists(self._prepare_file):
            log.debug("Preparing benchmark %s" % self.name)
            self._chmod755(self._prepare_file)
            cmd_result = exec_cmd([self._prepare_file], working_dir=self._path)

    def run(self, cpu_threads=1):
        # make sure the run.sh is executeable
        self._chmod755(self._run_file)

        log.debug("Executing benchmark %s" % self.name)

        log_file = tempfile.mktemp()
        bench_env = os.environ.copy()
        bench_env['RESULT_FILE'] = log_file
        bench_env['CPU_THREADS'] = str(cpu_threads)

        try:
            cmd_result = exec_cmd([self._run_file], working_dir=self._path,
                                  env=bench_env)

            # read result
            with open(log_file, 'r') as f:
                line = f.readline().rstrip()
                log.debug("Content of RESULT_FILE: '%s'" % line)
                if not line:
                    raise BenchmarkError("Result File '%s' is empty" % log_file)
                result = float(line)
        except Exception as e:
            raise(e)
        finally:
            os.remove(log_file)

        self.results.append(result)
        self._stats_outdated = True
        self.runs = self.runs + 1

        return result

    def _recalc_stats(self):
        if not self._recalc_stats:
            return

        if len(self.results) > 1:
            (self._avg, self._median, self._std_dev, self._min, self._max,
             self._confidence_intvl) = stats(self.results, 0.001)
        elif len(self.results) == 1:
            self._avg = self.results[0]
            self._median = self.results[0]
            self._min = self.results[0]
            self._max = self.results[0]
        self._stats_outdated = False

    @property
    def avg(self):
        """Returns the average result value.

        If not enough benchmarks values exist for the calculation None is
        returned."""

        self._recalc_stats()
        return self._avg

    @property
    def median(self):
        self._recalc_stats()
        return self._median

    @property
    def std_dev(self):
        """Returns the standard deviation.

        If not enough benchmarks values exist for the calculation NaN is
        returned."""

        self._recalc_stats()
        return self._std_dev

    @property
    def std_dev_pct(self):
        """Returns the standard in percent.

        If not enough benchmarks values exist for the calculation NaN is
        returned."""

        if not self.std_dev:
            return self.std_dev
        return (100 * self.std_dev) / self.avg

    @property
    def min(self):
        self._recalc_stats()
        return self._min

    @property
    def max(self):
        self._recalc_stats()
        return self._max

    @property
    def confidence_intvl_pct(self):
        """ Returns the 99.9% confidence interval in percent.

        If not enough benchmarks values exist for the calculation NaN is
        returned."""

        if not self.confidence_intvl:
            return self.confidence_intvl
        return (100 * self.confidence_intvl) / self.avg

    @property
    def confidence_intvl(self):
        """ Returns the 99.9% confidence interval.

        If not enough benchmarks values exist for the calculation NaN is
        returned."""

        self._recalc_stats()
        return self._confidence_intvl
