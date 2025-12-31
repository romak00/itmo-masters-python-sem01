import time
import threading
import multiprocessing as mp
from typing import List

def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def run_sync(n: int, tasks: int) -> float:
    t0 = time.perf_counter()
    for _ in range(tasks):
        fib(n)
    t1 = time.perf_counter()
    return t1 - t0

def run_threads(n: int, tasks: int) -> float:
    threads: List[threading.Thread] = []
    t0 = time.perf_counter()
    for _ in range(tasks):
        th = threading.Thread(target=fib, args=(n,))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
    t1 = time.perf_counter()
    return t1 - t0

def run_processes(n: int, tasks: int) -> float:
    procs: List[mp.Process] = []
    t0 = time.perf_counter()
    for _ in range(tasks):
        p = mp.Process(target=fib, args=(n,))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    t1 = time.perf_counter()
    return t1 - t0

def summarize(times: List[float]) -> str:
    avg = sum(times) / len(times)
    mn = min(times)
    mx = max(times)
    return f"runs: {len(times)}, avg: {avg:.4f}s, min: {mn:.4f}s, max: {mx:.4f}s\n" \
           + "\n".join(f"{i+1:2d}: {t:.4f}s" for i, t in enumerate(times))

def main():
    n = 30
    repeats = 10
    tasks = 10

    print(f"Platform: CPUs={mp.cpu_count()}")
    print(f"Parameters: n={n}, tasks={tasks}, repeats={repeats}")

    sync_times = []
    thread_times = []
    process_times = []

    for rep in range(1, repeats + 1):
        print(f"\n--- Repeat {rep}/{repeats} ---")

        print("Running sync...")
        t_sync = run_sync(n, tasks)
        print(f"sync total: {t_sync:.4f}s")
        sync_times.append(t_sync)

        print("Running threads...")
        t_threads = run_threads(n, tasks)
        print(f"threads total: {t_threads:.4f}s")
        thread_times.append(t_threads)

        print("Running processes...")
        t_procs = run_processes(n, tasks)
        print(f"processes total: {t_procs:.4f}s")
        process_times.append(t_procs)

    report_lines = []
    report_lines.append("SYNCHRONOUS:\n")
    report_lines.append(summarize(sync_times))
    report_lines.append("\nTHREADS:\n")
    report_lines.append(summarize(thread_times))
    report_lines.append("\nPROCESSES:\n")
    report_lines.append(summarize(process_times))

    report = "\n".join(report_lines)
    out_path = "task_1/artifacts.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print("\nReport written to:", out_path)
    print("\nSUMMARY:\n")
    print(report)

if __name__ == "__main__":
    main()
