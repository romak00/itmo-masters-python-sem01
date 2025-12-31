import multiprocessing as mp
import threading
import time
from collections import deque
from queue import Empty
import codecs

SEND_INTERVAL = 5.0

def timestamp_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def process_a(parent_to_a: mp.Queue, a_to_b: mp.Queue):
    local_q = deque()
    finishing = False

    last_sent = time.time()

    while True:
        try:
            item = parent_to_a.get(timeout=0.5)
        except Empty:
            item = None
        else:
            if item is None:
                finishing = True
            else:
                local_q.append(item)

        now = time.time()
        if (now - last_sent) >= SEND_INTERVAL and local_q:
            msg = local_q.popleft()
            try:
                a_to_b.put(msg.lower())
            except Exception:
                pass
            last_sent = now

        if finishing and not local_q:
            try:
                a_to_b.put(None)
            except Exception:
                pass
            break
    return


def process_b(a_to_b: mp.Queue, b_to_parent: mp.Queue):
    while True:
        item = a_to_b.get()
        if item is None:
            try:
                b_to_parent.put(None)
            except Exception:
                pass
            break
        
        encoded = codecs.encode(item, "rot_13")
        ts = timestamp_now()
        print(f"[{ts}] {encoded}", flush=True)
        try:
            b_to_parent.put((ts, encoded))
        except Exception:
            pass
    return

def main():
    parent_to_a = mp.Queue()
    a_to_b = mp.Queue()
    b_to_parent = mp.Queue()

    proc_a = mp.Process(target=process_a, args=(parent_to_a, a_to_b), daemon=False)
    proc_b = mp.Process(target=process_b, args=(a_to_b, b_to_parent), daemon=False)
    proc_a.start()
    proc_b.start()
    
    shutdown_event = threading.Event()

    def b_reader():
        while True:
            try:
                item = b_to_parent.get(timeout=0.5)
            except Empty:
                if shutdown_event.is_set() and not proc_b.is_alive():
                    break
                continue

            if item is None:
                break
            ts, encoded = item
            line = f"[{ts}] FROM_B: {encoded}"
            print(f"(logged) {line}", flush=True)

    t_b_reader = threading.Thread(target=b_reader, daemon=True)
    t_b_reader.start()

    print("Enter lines. Type Ctrl-C or Ctrl-D to abort.")

    try:
        while True:
            try:
                line = input()
            except EOFError:
                print("EOF received, sending termination sentinel to A...", flush=True)
                parent_to_a.put(None)
                shutdown_event.set()
                break
            text = line.rstrip("\n")
            parent_to_a.put(text)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received, sending termination sentinel to A...")
        try:
            parent_to_a.put(None)
        except Exception:
            pass
        shutdown_event.set()

    start_wait = time.time()
    print("Waiting for processes A and B to finish...")
    try:
        proc_a.join(timeout=SEND_INTERVAL)
    except Exception:
        pass
    try:
        proc_b.join(timeout=SEND_INTERVAL)
    except Exception:
        pass

    shutdown_event.set()
    t_b_reader.join(timeout=SEND_INTERVAL)

    print("Shutdown complete.", flush=True)

if __name__ == "__main__":
    main()
