# ArbiterBench website

Static website for https://arbiterbench.com, built with stdlib Python and browser JavaScript.
No application server, package manager, analytics, or runtime external requests are needed.

## Preview and validate

Use Python 3.12, matching the repository's CI (older Python versions use different floating-point summation and fail the existing exact metric reproduction check).

```sh
python3 site/build.py
python3 site/check.py
python3 tools/check.py
node --check site/app.js
python3 -m http.server 8765 --bind 127.0.0.1 --directory _site
```

Open http://127.0.0.1:8765/. The build output is ignored by Git. `site/check.py` checks the complete deployment file allowlist, metric fidelity, public item identities, trial counts, quoted evidence, and local asset links.

## Content and provenance

- Full-set results: `results/full_set_metrics.json` (71 items; aggregate data only).
- Public results: `results/metrics.json` (36 items; copied exactly, not rescored by the website).
- Cases: `data/items.jsonl`, joined by exact case ID to `results/trials.jsonl` and `data/mechanism_pairs.jsonl`.
- Failure taxonomy: `data/mechanisms.json`.
- Worked example and original plot: `docs/CASES.md`, `figures/case_gcode_plot.png`.
- Audit funnel and claims: `docs/METHOD.md`, cross-checked against the published [writeup](https://heuristic.build/blog/arbiterbench/).
- Shared figures are copied from `figures/`; the social card reuses `figures/leaderboard.png`.
- Model/provider SVGs are the same assets used at `https://heuristic.build/blog/arbiterbench/fig/icons/`. The favicon is the existing Heuristic mark, also used in the launch materials. Logos identify their respective providers; no endorsement is implied.
- Source Serif 4 and Inter match the writeup. Fonts are self-hosted, with their SIL Open Font Licenses in `site/assets/fonts/`.

The build takes no internal-repository input and publishes no held-out case records. Internal launch materials were consulted for context and branding, but all shipped numbers and evidence are already in the public release. Public case material retains the repository's evaluation-only policy and upstream licenses. The generated dataset retains the benchmark canary.

The high-effort Astra subset is explained separately, not mixed into the main ranking. Missing verdicts are not scored as failures. Selecting-judge flags and differing coverage stay visible; the page explicitly distinguishes hard-set accuracy from population accuracy. Cases expand to the recorded mechanisms and link to full task packages and judge logs on GitHub.

## Deployment

`.github/workflows/site.yml` builds and checks PRs, attaching a `website-preview` artifact. PR runs do not deploy. A merge to `main` builds and deploys `_site` to the `github-pages` environment via GitHub's Pages actions. The workflow can also be dispatched on `main`.

Repository Pages settings must use **GitHub Actions**, with custom domain **arbiterbench.com**. With Actions publishing, the custom domain is configured in repository settings; a `CNAME` file is not required.

Cloudflare DNS configuration:

| Type | Name | Value | Proxy |
| --- | --- | --- | --- |
| A | @ | 185.199.108.153 | DNS only |
| A | @ | 185.199.109.153 | DNS only |
| A | @ | 185.199.110.153 | DNS only |
| A | @ | 185.199.111.153 | DNS only |
| CNAME | www | raphael-64.github.io | DNS only |
| TXT | _github-pages-challenge-raphael-64 | Account verification record, retained in Cloudflare | N/A |

Domain ownership is verified in the GitHub account's Pages settings. Keep that TXT record. GitHub Pages manages the certificate and the www-to-apex redirect. After the first deployment, confirm certificate provisioning and **Enforce HTTPS** in repository settings. The PR does not publish or merge itself.

See [GitHub's custom domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

## Design references

[DeepRSI](https://www.deeprsi.com/) for compact research results; [SWE-bench](https://www.swebench.com/) for result filters; [Terminal-Bench](https://www.tbench.ai/) for task access and confidence intervals. The final visual baseline is the existing Heuristic writeup: Source Serif 4 / Inter, actual provider logos, restrained blue, and plain section headings.
