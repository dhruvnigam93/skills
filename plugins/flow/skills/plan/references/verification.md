# Verification

Applies to every step's `Verify:` and every success criterion. Use the highest rung that can work:

1. **Test** — a unit or integration test at the interface. Give its name and the behavior it asserts, with exact values.
2. **Other automated check** — an API call, a script, a Playwright run, or deploy + end-to-end check + log grep. Give the literal command and the output that means pass.
3. **`MANUAL:`** — only when nothing automated can observe it. State what the user checks and what counts as pass. The step cannot self-certify; implementation pauses for the user.

## Rules

**It must fail before the change.** A check that passes today proves nothing about the step.
- ✅ `uv run pytest tests/orders/test_cancel.py -k shipped -v` → `test_cancel_shipped_order_raises PASSED` (fails today — the test doesn't exist yet)
- ❌ `make test` → green (green before the change too)

**Expected output is literal and observable.**
- ✅ `curl -s -X POST localhost:8000/orders/123/cancel | jq -r .status` → `cancelled`
- ❌ "the endpoint works"

**Use the project's own entry points.** Find them in the Makefile, `package.json`, `pyproject.toml`, or CI config. Never guess.
- ✅ `make -C api test` when the repo defines it
- ❌ `python -m pytest` in a repo that runs everything through `uv run`

**Narrow per step, broad at the end.** A step's check targets that step's behavior; add the fast full suite (`make test`, lint) when it is cheap. The full suite, lint, and typecheck belong in the success criteria.

**Run stochastic checks more than once.** Anything flaky or model-driven runs N=5, and the expected output says so.
- ✅ `for i in 1 2 3 4 5; do uv run pytest tests/agent/test_router.py -q || exit 1; done` → exit 0
- ❌ one run passed

## Beyond tests

- **API:** `curl -s localhost:8000/health | jq -r .db` → `ok`
- **Browser:** `npx playwright test e2e/cancel.spec.ts` → `1 passed`
- **Deploy:** `make deploy-staging && kubectl logs deploy/orders --since=2m | grep -c "cancel_order ok"` → at least `1`
- **Data:** `psql $DB -tAc "select count(*) from orders where status='cancelled' and refund_id is null"` → `0`

## MANUAL

- ✅ `MANUAL:` open `/orders/123` on staging — the Cancel button is disabled and its tooltip reads "Already shipped"
- ❌ `MANUAL:` check the UI looks right
