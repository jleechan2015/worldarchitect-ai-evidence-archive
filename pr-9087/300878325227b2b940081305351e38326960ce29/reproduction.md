# Clean-Computer Reproduction: PR #9087

These commands reproduce the exact checkout and the two validation entrypoints.
They require Python 3.12, NVM, Git, GitHub CLI, `lsof`, `ffmpeg`, `asciinema`,
and `agg`. Supply a dedicated service-account JSON path in
`WORLDAI_GOOGLE_APPLICATION_CREDENTIALS`; do not copy credential contents into
logs or evidence.

```bash
git clone https://github.com/jleechanorg/worldarchitect.ai.git
cd worldarchitect.ai
git fetch origin refs/pull/9087/head
git checkout --detach 300878325227b2b940081305351e38326960ce29
test "$(git rev-parse HEAD)" = "300878325227b2b940081305351e38326960ce29"
test -z "$(git status --porcelain)"

nvm install 22.22.0
nvm use 22.22.0
test "$(node --version)" = "v22.22.0"

python3.12 -m venv venv
./venv/bin/python -m pip install --upgrade pip
./venv/bin/python -m pip install -r mvp_site/requirements.txt
./venv/bin/playwright install chromium
npm ci
```

Run the focused deterministic contract suite:

```bash
EXPECTED_PR9087_SHA=300878325227b2b940081305351e38326960ce29 \
  ./venv/bin/python -m pytest -q \
  testing_ui/test_pr9087_harness_contracts.py
```

Expected result: `22 passed`. The recorded terminal evidence also checks the
live PR head before the test and the exact clean SHA after it.

For an authorized one-shot browser capture, first point to a dedicated existing
service-account file. The harness dynamically selects a free localhost port,
starts real Gunicorn, verifies `/health.git_commit`, drives real headless
Chromium at desktop and mobile viewports, and stops the owned server afterward.

```bash
export WORLDAI_GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/dedicated-service-account.json
test -f "$WORLDAI_GOOGLE_APPLICATION_CREDENTIALS"

PATH="$HOME/.nvm/versions/node/v22.22.0/bin:/usr/bin:/bin:/usr/sbin:/sbin" \
env -u MOCK_SERVICES_MODE -u TEST_MODE -u USE_MOCK_FIREBASE \
  -u USE_MOCK_GEMINI -u SMOKE_TOKEN -u WORLDAI_MOCK_MODE \
  EXPECTED_PR9087_SHA=300878325227b2b940081305351e38326960ce29 \
  PYTHONPATH="$PWD:$PWD/mvp_site" \
  ./vpython testing_ui/test_pr9087_real_browser_cache_control_es.py
```

Expected result: four of four scenarios PASS. Do not rerun a failed expensive
capture merely to obtain a passing artifact; preserve and investigate the first
result.
