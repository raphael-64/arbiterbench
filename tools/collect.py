#!/usr/bin/env python3
"""Turn a Harbor jobs directory into trial rows for tools/score.py. Stdlib only.

    python3 tools/collect.py <harbor_jobs_dir> --judge my-judge > my_trials.jsonl

A trial directory is named <case_id>__<suffix>. The verdict is read from final_judgment.json ("pass/fail" or "pass"),
or from a trailing `VERDICT: {"verdict": "PASS"|"FAIL"}` line in any text file the judge left. Trials with no readable
verdict are reported on stderr and skipped: a missing verdict is a harness failure, not a wrong answer."""
import argparse, json, pathlib, re, sys

def verdict(d):
    for f in d.rglob("final_judgment.json"):
        try: j = json.loads(f.read_text())
        except Exception: continue
        v = j.get("pass/fail", j.get("verdict", j.get("pass")))
        if isinstance(v, bool): return "pass" if v else "fail"
        if isinstance(v, str) and v.strip().lower() in ("pass", "fail"): return v.strip().lower()
    for f in sorted(d.rglob("*")):
        if f.is_file() and f.suffix in (".md", ".txt", ".log", ".json") and f.stat().st_size < 5_000_000:
            m = re.findall(r'VERDICT:\s*\{[^}]*"verdict"\s*:\s*"(PASS|FAIL)"', f.read_text(errors="ignore"))
            if m: return m[-1].lower()
    return None

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("jobs_dir"); ap.add_argument("--judge", required=True, help="name for your judge in the results table")
    a = ap.parse_args(); n = collections_counter = {}
    for d in sorted(pathlib.Path(a.jobs_dir).rglob("jf_*__*")):
        if not d.is_dir(): continue
        cid = d.name.split("__")[0]; v = verdict(d)
        if v is None: print(f"no verdict: {d}", file=sys.stderr); continue
        n[cid] = n.get(cid, 0) + 1
        print(json.dumps({"case_id": cid, "judge": a.judge, "attempt": n[cid], "verdict": v}))
if __name__ == "__main__": main()
