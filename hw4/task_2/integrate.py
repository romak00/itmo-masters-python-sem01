from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import importlib
import math
import time
import multiprocessing as mp
from typing import List, Dict

A = 0.0
B = math.pi / 2.0

def _partial_sum(func_module: str, func_name: str, a: float, step: float, start_idx: int, count: int) -> float:
    mod = importlib.import_module(func_module)
    f = getattr(mod, func_name)
    acc = 0.0
    x = a + start_idx * step
    _f = f
    _step = step
    for _ in range(count):
        acc += _f(x) * _step
        x += _step
    return acc


def integrate_parallel(func, a: float, b: float, n_jobs: int, n_iter: int, executor_type: str) -> float:
    n_jobs = min(n_jobs, n_iter)
    step = (b - a) / n_iter

    q, r = divmod(n_iter, n_jobs)
    args = []
    start = 0
    for i in range(n_jobs):
        cnt = q + (1 if i < r else 0)
        args.append((func.__module__, func.__name__, a, step, start, cnt))
        start += cnt

    total = 0.0
    if executor_type == "thread":
        with ThreadPoolExecutor(max_workers=n_jobs) as ex:
            futures = [ex.submit(_partial_sum, *arg) for arg in args]
            for fut in as_completed(futures):
                total += fut.result()
    else:
        with ProcessPoolExecutor(max_workers=n_jobs) as ex:
            futures = [ex.submit(_partial_sum, *arg) for arg in args]
            for fut in as_completed(futures):
                total += fut.result()

    return total

def run_threads(n_iter: int, n_jobs: int) -> float:
    t0 = time.perf_counter()
    integrate_parallel(math.cos, A, B, n_jobs=n_jobs, n_iter=n_iter, executor_type="thread")
    t1 = time.perf_counter()
    return t1 - t0


def run_processes(n_iter: int, n_jobs: int) -> float:
    t0 = time.perf_counter()
    integrate_parallel(math.cos, A, B, n_jobs=n_jobs, n_iter=n_iter, executor_type="process")
    t1 = time.perf_counter()
    return t1 - t0


def summarize(times: List[float]) -> str:
    avg = sum(times) / len(times)
    mn = min(times)
    mx = max(times)
    return f"runs: {len(times)}, avg: {avg:.4f}s, min: {mn:.4f}s, max: {mx:.4f}s\n" \
           + "\n".join(f"{i+1:2d}: {t:.4f}s" for i, t in enumerate(times))

def main():
    cpu_cnt = mp.cpu_count()
    max_jobs = cpu_cnt * 2
    
    repeats = 3
    n_iter = 10000000

    print(f"Platform: CPUs={cpu_cnt}")
    print(f"Parameters: n_iter={n_iter}, repeats={repeats}, jobs range=1..{max_jobs}\n")

    thread_times: Dict[int, List[float]] = {j: [] for j in range(1, max_jobs + 1)}
    process_times: Dict[int, List[float]] = {j: [] for j in range(1, max_jobs + 1)}


    for rep in range(1, repeats + 1):
        print(f"--- Repeat {rep}/{repeats} ---\n")

        for n_jobs in range(1, max_jobs + 1):
            print(f"--- n_jobs = {n_jobs} ---")

            print("Running threads...")
            t_threads = run_threads(n_iter, n_jobs)
            print(f"threads total: {t_threads:.4f}s")
            thread_times[n_jobs].append(t_threads)

            print("Running processes...")
            t_procs = run_processes(n_iter, n_jobs)
            print(f"processes total: {t_procs:.4f}s\n")
            process_times[n_jobs].append(t_procs)

    report_lines: List[str] = []
    report_lines.append(f"Benchmark integrate(math.cos, {A}, {B})\n")
    report_lines.append(f"Parameters: n_iter={n_iter}, repeats={repeats}, jobs_range=1..{max_jobs}\n")
    
    report_lines.append("\nTHREADS (per n_jobs):\n")
    for n_jobs in range(1, max_jobs + 1):
        report_lines.append(f"\nn_jobs = {n_jobs}:\n")
        report_lines.append(summarize(thread_times[n_jobs]))

    report_lines.append("\nPROCESSES (per n_jobs):\n")
    for n_jobs in range(1, max_jobs + 1):
        report_lines.append(f"\nn_jobs = {n_jobs}:\n")
        report_lines.append(summarize(process_times[n_jobs]))

    report = "\n".join(report_lines)

    out_path = "task_2/artifacts.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print("\nReport written to:", out_path)
    print("\nSUMMARY:\n")
    print(report)

if __name__ == "__main__":
    main()
