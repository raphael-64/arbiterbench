#!/usr/bin/env python3
"""Stage the OSWorld screenshots that this repository does not redistribute. Stdlib only.

    python3 tools/fetch_osworld_images.py /path/to/OSWorldSurfer-Holo3-35B-A3B-20260330-OSWorld-Verified_20260420_verified-run_with-local-rewards.zip

Download that archive yourself from https://huggingface.co/datasets/xlangai/ubuntu_osworld_verified_trajs (MIT; several GB).
For every case whose environment holds `*.png.REF.json` pointers, the script streams the archive once, takes the screenshots of
that case's trajectory, checks each against the pointer's SHA-256 and byte count, and writes the PNG beside its pointer.
Nothing is written unless the hash matches. Re-running is safe."""
import gzip, hashlib, json, pathlib, sys, tarfile, zipfile
ROOT = pathlib.Path(__file__).resolve().parents[1]

def main():
    if len(sys.argv) != 2: sys.exit(__doc__)
    items = [json.loads(l) for l in (ROOT / "data/items.jsonl").open()]
    want = {}                                            # trajectory id -> {image name: pointer path}
    for i in items:
        refs = list((ROOT / "cases" / i["case_id"]).rglob("*.png.REF.json"))
        if refs: want[i["source_case_id"].split("__")[-1]] = {r.name[:-len(".REF.json")]: r for r in refs}
    todo = sum(len(v) for v in want.values()); done = bad = 0
    print(f"{len(want)} case(s), {todo} screenshot(s) to stage")
    with zipfile.ZipFile(sys.argv[1]) as z:
        nested = next(n for n in z.namelist() if n.endswith(".tar.gz"))
        with z.open(nested) as raw, tarfile.open(fileobj=raw, mode="r|gz") as tar:
            for m in tar:
                p = pathlib.PurePosixPath(m.name)
                if not m.isfile() or not p.name.endswith((".png", ".png.gz")): continue
                tid, name = p.parent.parent.name, p.name.removesuffix(".gz")
                ref = want.get(tid, {}).get(name)
                if ref is None: continue
                data = tar.extractfile(m).read()
                if p.name.endswith(".gz"): data = gzip.decompress(data)
                meta = json.loads(ref.read_text())
                if hashlib.sha256(data).hexdigest() != meta["sha256"] or len(data) != meta["bytes"]:
                    bad += 1; print("hash mismatch, not written:", ref); continue
                ref.with_name(name).write_bytes(data); done += 1
                if done == todo: break
    print(f"staged {done}/{todo}" + (f", {bad} mismatched" if bad else "")); sys.exit(0 if done == todo else 1)
if __name__ == "__main__": main()
