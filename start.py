"""
Unified launcher – starts both the Flask backend and Next.js frontend
with a single command:

    python start.py

Press Ctrl+C to stop both servers.
"""

import subprocess
import sys
import os
import signal
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

# Detect npm command (npm.cmd on Windows, npm on Unix)
NPM_CMD = "npm.cmd" if os.name == "nt" else "npm"


def main():
    processes = []

    try:
        # ── 1. Start Flask backend ──────────────────────────────────────
        print("Starting Flask backend on http://127.0.0.1:5000 ...")
        backend = subprocess.Popen(
            [sys.executable, "web_server.py"],
            cwd=ROOT_DIR,
        )
        processes.append(("Backend", backend))

        # ── 2. Start Next.js frontend ──────────────────────────────────
        print("Starting Next.js frontend on http://localhost:3000 ...")
        frontend = subprocess.Popen(
            [NPM_CMD, "run", "dev"],
            cwd=FRONTEND_DIR,
        )
        processes.append(("Frontend", frontend))

        print("\n" + "=" * 60)
        print("  AI Health Monitor is running!")
        print("  Backend  → http://127.0.0.1:5000")
        print("  Frontend → http://localhost:3000")
        print("  Press Ctrl+C to stop both servers.")
        print("=" * 60 + "\n")

        # Wait for either process to exit
        while True:
            for name, proc in processes:
                ret = proc.poll()
                if ret is not None:
                    print(f"\n{name} exited with code {ret}. Shutting down...")
                    raise KeyboardInterrupt
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
        for name, proc in processes:
            if proc.poll() is None:
                print(f"  Stopping {name} (PID {proc.pid}) ...")
                if os.name == "nt":
                    # On Windows, terminate the whole process tree
                    subprocess.call(
                        ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                else:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        print("All servers stopped.")


if __name__ == "__main__":
    main()
