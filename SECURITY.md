# Security

## Reporting vulnerabilities

Do **not** open a public issue for undisclosed security problems.

Contact the maintainer privately (for example via GitHub profile or org security contact). Include: summary, affected area, reproduction steps, and impact.

## Secrets and configuration

- Never commit real credentials. Use `.env` locally (gitignored) and `.env.example` for names only.
- For CI/CD, store values in **GitHub Actions secrets** (and hosting provider env vars), not in workflow source.
- If a secret was ever committed: **revoke and rotate it** immediately, then remove it from git history if the repo was or will be public.

## Dependency updates

Keep Python dependencies reasonably current (`requirements.txt`). Review releases for security advisories.
