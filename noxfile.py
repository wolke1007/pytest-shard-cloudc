import json
import pathlib
import shutil
import subprocess
import sys

import nox

nox.options.default_venv_backend = "none"
nox.options.sessions = ["tests", "shard-0", "shard-1", "lint", "typing"]

ALLURE_RESULTS_DIR = pathlib.Path("allure-results")
ALLURE_REPORT_DIR = pathlib.Path("allure-report")


@nox.session(name="tests", python=False)
def tests(session: nox.Session) -> None:
    session.run("python", "-m", "pytest", "tests", external=True)


@nox.session(name="shard-0", python=False)
def shard_zero(session: nox.Session) -> None:
    session.run(
        "python",
        "-m",
        "pytest",
        "--shard-id=0",
        "--num-shards=2",
        "tests",
        external=True,
    )


@nox.session(name="shard-1", python=False)
def shard_one(session: nox.Session) -> None:
    session.run(
        "python",
        "-m",
        "pytest",
        "--shard-id=1",
        "--num-shards=2",
        "tests",
        external=True,
    )


@nox.session(name="lint", python=False)
def lint(session: nox.Session) -> None:
    session.run("python", "-m", "ruff", "check", "pytest_shard", "tests", external=True)
    session.run(
        "python",
        "-m",
        "ruff",
        "format",
        "--check",
        "pytest_shard",
        "tests",
        external=True,
    )


@nox.session(name="typing", python=False)
def typing(session: nox.Session) -> None:
    session.run("python", "-m", "mypy", "pytest_shard", external=True)


@nox.session(name="allure-shard-0", python=False)
def allure_shard_zero(session: nox.Session) -> None:
    """Run shard 0/2 and write Allure results to allure-results/shard-0."""
    shard_dir = ALLURE_RESULTS_DIR / "shard-0"
    shutil.rmtree(shard_dir, ignore_errors=True)
    session.run(
        "python", "-m", "pytest",
        "--shard-id=0", "--num-shards=2",
        f"--alluredir={shard_dir}",
        "tests",
        external=True,
    )


@nox.session(name="allure-shard-1", python=False)
def allure_shard_one(session: nox.Session) -> None:
    """Run shard 1/2 and write Allure results to allure-results/shard-1."""
    shard_dir = ALLURE_RESULTS_DIR / "shard-1"
    shutil.rmtree(shard_dir, ignore_errors=True)
    session.run(
        "python", "-m", "pytest",
        "--shard-id=1", "--num-shards=2",
        f"--alluredir={shard_dir}",
        "tests",
        external=True,
    )


@nox.session(name="allure-merge", python=False)
def allure_merge(session: nox.Session) -> None:
    """Merge Allure results from all shards and generate a combined report."""
    combined_dir = ALLURE_RESULTS_DIR / "combined"
    shutil.rmtree(combined_dir, ignore_errors=True)
    combined_dir.mkdir(parents=True)

    for shard_dir in sorted(ALLURE_RESULTS_DIR.iterdir()):
        if shard_dir.name == "combined" or not shard_dir.is_dir():
            continue
        for result_file in shard_dir.iterdir():
            shutil.copy2(result_file, combined_dir / result_file.name)

    shutil.rmtree(ALLURE_REPORT_DIR, ignore_errors=True)
    session.run(
        "allure", "generate", str(combined_dir),
        "-o", str(ALLURE_REPORT_DIR),
        "--clean",
        external=True,
    )
    session.log(f"Allure report generated at: {ALLURE_REPORT_DIR.resolve()}")


@nox.session(name="demo-10-shards", python=False)
def demo_ten_shards(session: nox.Session) -> None:
    """Run demo/demo_tests/ across 10 shards and produce a merged Allure report."""
    demo_results = ALLURE_RESULTS_DIR / "demo"
    demo_report = ALLURE_REPORT_DIR.parent / "allure-report-demo"
    num_shards = 10

    shutil.rmtree(demo_results, ignore_errors=True)

    for shard_id in range(num_shards):
        shard_dir = demo_results / f"shard-{shard_id}"
        session.run(
            "python", "-m", "pytest",
            f"--shard-id={shard_id}",
            f"--num-shards={num_shards}",
            f"--alluredir={shard_dir}",
            "-v",
            "demo/demo_tests",
            external=True,
        )

    combined_dir = demo_results / "combined"
    combined_dir.mkdir(parents=True)
    for shard_id in range(num_shards):
        shard_dir = demo_results / f"shard-{shard_id}"
        if shard_dir.is_dir():
            for result_file in shard_dir.iterdir():
                shutil.copy2(result_file, combined_dir / result_file.name)

    shutil.rmtree(demo_report, ignore_errors=True)
    session.run(
        "allure", "generate", str(combined_dir),
        "-o", str(demo_report),
        "--clean",
        external=True,
    )
    session.log(f"Demo Allure report generated at: {demo_report.resolve()}")


@nox.session(name="demo-3-shards-parallel", python=False)
def demo_three_shards_parallel(session: nox.Session) -> None:
    """Run demo/demo30_tests/ across 3 shards in parallel processes and produce a merged Allure report."""
    num_shards = 3
    demo_results = ALLURE_RESULTS_DIR / "demo30"
    demo_report = ALLURE_REPORT_DIR.parent / "allure-report-demo30"

    shutil.rmtree(demo_results, ignore_errors=True)
    for shard_id in range(num_shards):
        (demo_results / f"shard-{shard_id}").mkdir(parents=True)

    # Launch all shards concurrently — each gets its own OS process
    log_files = []
    procs = []
    for shard_id in range(num_shards):
        shard_dir = demo_results / f"shard-{shard_id}"
        log_path = demo_results / f"shard-{shard_id}.log"
        log_file = log_path.open("w")
        log_files.append(log_file)
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "pytest",
                f"--shard-id={shard_id}",
                f"--num-shards={num_shards}",
                f"--alluredir={shard_dir}",
                "-v",
                "demo/demo30_tests",
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        procs.append(proc)
        session.log(f"Shard {shard_id} started  (PID {proc.pid})")

    # Wait for all shards to finish
    for shard_id, (proc, log_file) in enumerate(zip(procs, log_files)):
        proc.wait()
        log_file.close()
        log_text = (demo_results / f"shard-{shard_id}.log").read_text()
        session.log(f"─── shard-{shard_id} (exit {proc.returncode}) ───\n{log_text}")
        if proc.returncode != 0:
            session.error(f"Shard {shard_id} failed with exit code {proc.returncode}")

    # Merge results from all shards into combined/
    combined_dir = demo_results / "combined"
    combined_dir.mkdir()
    for shard_id in range(num_shards):
        shard_dir = demo_results / f"shard-{shard_id}"
        for result_file in shard_dir.iterdir():
            shutil.copy2(result_file, combined_dir / result_file.name)

    shutil.rmtree(demo_report, ignore_errors=True)
    session.run(
        "allure", "generate", str(combined_dir),
        "-o", str(demo_report),
        "--clean",
        external=True,
    )
    session.log(f"Allure report generated at: {demo_report.resolve()}")


def _run_shards_parallel(
    session: nox.Session,
    *,
    test_dir: str,
    num_shards: int,
    results_root: pathlib.Path,
    extra_args: list[str],
    per_shard_args: "dict[int, list[str]] | None" = None,
) -> None:
    """Launch `num_shards` pytest processes in parallel, wait for all to finish.

    `per_shard_args` maps shard_id → additional args for that shard only.
    """
    results_root.mkdir(parents=True, exist_ok=True)
    log_files, procs = [], []
    for shard_id in range(num_shards):
        shard_dir = results_root / f"shard-{shard_id}"
        shard_dir.mkdir(parents=True, exist_ok=True)
        log_file = (results_root / f"shard-{shard_id}.log").open("w")
        log_files.append(log_file)
        shard_extra = (per_shard_args or {}).get(shard_id, [])
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "pytest",
                f"--shard-id={shard_id}",
                f"--num-shards={num_shards}",
                f"--alluredir={shard_dir}",
                "-v",
                *extra_args,
                *shard_extra,
                test_dir,
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        procs.append(proc)
        session.log(f"  shard-{shard_id} started (PID {proc.pid})")

    for shard_id, (proc, log_file) in enumerate(zip(procs, log_files)):
        proc.wait()
        log_file.close()
        log_text = (results_root / f"shard-{shard_id}.log").read_text()
        session.log(f"  shard-{shard_id} (exit {proc.returncode}):\n{log_text}")
        if proc.returncode != 0:
            session.error(f"shard-{shard_id} failed")


def _merge_allure_results(results_root: pathlib.Path, report_dir: pathlib.Path, num_shards: int) -> None:
    combined = results_root / "combined"
    shutil.rmtree(combined, ignore_errors=True)
    combined.mkdir()
    for shard_id in range(num_shards):
        shard_dir = results_root / f"shard-{shard_id}"
        if shard_dir.is_dir():
            for f in shard_dir.iterdir():
                if f.is_file():
                    shutil.copy2(f, combined / f.name)
    shutil.rmtree(report_dir, ignore_errors=True)
    subprocess.run(
        ["allure", "generate", str(combined), "-o", str(report_dir), "--clean"],
        check=True,
    )


@nox.session(name="demo-xdist-group-hash-balanced", python=False)
def demo_xdist_group_hash_balanced(session: nox.Session) -> None:
    """Demonstrate hash-balanced mode: LPT bin-packing prevents group collision.

    Compared to plain hash mode where database+auth both land on shard 0 (10 tests),
    hash-balanced spreads groups across shards: ~6 / 5 / 6 tests per shard.
    Open the generated Allure report and navigate to Timeline — groups are evenly
    distributed across threads, and tests within each group stay on the same thread.
    """
    num_shards = 3
    demo_results = ALLURE_RESULTS_DIR / "demo-xdist-group-balanced"
    demo_report = ALLURE_REPORT_DIR.parent / "allure-report-xdist-group-balanced"

    shutil.rmtree(demo_results, ignore_errors=True)

    _run_shards_parallel(
        session,
        test_dir="demo/demo_xdist_group_tests",
        num_shards=num_shards,
        results_root=demo_results,
        extra_args=["--shard-mode=hash-balanced", "-v"],
    )

    _merge_allure_results(demo_results, demo_report, num_shards)
    session.log(f"Allure report generated at: {demo_report.resolve()}")
    session.log("Open with: allure open allure-report-xdist-group-balanced")


@nox.session(name="demo-xdist-group-hash", python=False)
def demo_xdist_group_hash(session: nox.Session) -> None:
    """Demonstrate xdist_group co-location guarantee in hash mode.

    Tests sharing the same xdist_group marker all land on the same shard.
    Open the generated Allure report and navigate to Timeline — every test
    in the same group will appear on exactly one thread (shard process).
    """
    num_shards = 3
    demo_results = ALLURE_RESULTS_DIR / "demo-xdist-group"
    demo_report = ALLURE_REPORT_DIR.parent / "allure-report-xdist-group"

    shutil.rmtree(demo_results, ignore_errors=True)

    _run_shards_parallel(
        session,
        test_dir="demo/demo_xdist_group_tests",
        num_shards=num_shards,
        results_root=demo_results,
        extra_args=["--shard-mode=hash", "-v"],
    )

    _merge_allure_results(demo_results, demo_report, num_shards)
    session.log(f"Allure report generated at: {demo_report.resolve()}")
    session.log("Open with: allure open allure-report-xdist-group")


@nox.session(name="demo-duration-comparison", python=False)
def demo_duration_comparison(session: nox.Session) -> None:
    """Two-run comparison demo using demo/demo_duration_tests/.

    Run 1 — round-robin (default): 3 parallel shards with unequal workloads.
      Each shard also records durations with --store-durations.
      Expected: shard-0 ~40 s, shard-1 ~6 s, shard-2 ~6 s.

    Run 2 — duration mode: shard using the merged .test_durations file.
      Expected: all shards ~17-18 s (LPT bin-packing balances the load).
    """
    num_shards = 3
    base = ALLURE_RESULTS_DIR / "demo-duration"
    first_results = base / "first"
    second_results = base / "second"
    durations_path = base / ".test_durations"
    first_report = pathlib.Path("allure-report-duration-first")
    second_report = pathlib.Path("allure-report-duration-second")

    shutil.rmtree(base, ignore_errors=True)

    # ── Run 1: round-robin + store durations ──────────────────────────────
    session.log("=== Run 1: round-robin (unbalanced) + --store-durations ===")
    _run_shards_parallel(
        session,
        test_dir="demo/demo_duration_tests",
        num_shards=num_shards,
        results_root=first_results,
        extra_args=["--shard-mode=roundrobin", "--store-durations"],
        # Each shard writes to its own durations file to avoid concurrent write conflicts
        per_shard_args={
            i: [f"--durations-path={first_results / f'shard-{i}' / '.test_durations'}"]
            for i in range(num_shards)
        },
    )

    # Merge per-shard duration files into one
    merged: dict[str, float] = {}
    for shard_id in range(num_shards):
        shard_dur = first_results / f"shard-{shard_id}" / ".test_durations"
        if shard_dur.exists():
            merged.update(json.loads(shard_dur.read_text()))
    durations_path.write_text(json.dumps(merged, indent=2, sort_keys=True))
    session.log(f"Merged durations written to {durations_path} ({len(merged)} tests)")

    _merge_allure_results(first_results, first_report, num_shards)
    session.log(f"Run 1 report → {first_report.resolve()}")

    # ── Run 2: duration mode ───────────────────────────────────────────────
    session.log("=== Run 2: duration mode (balanced) ===")
    _run_shards_parallel(
        session,
        test_dir="demo/demo_duration_tests",
        num_shards=num_shards,
        results_root=second_results,
        extra_args=[
            "--shard-mode=duration",
            f"--durations-path={durations_path}",
        ],
    )

    _merge_allure_results(second_results, second_report, num_shards)
    session.log(f"Run 2 report → {second_report.resolve()}")
