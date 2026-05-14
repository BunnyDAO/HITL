.PHONY: demo demo-multi clean test

# Render vision-centroid into tests/generated/test_demo.py and run pytest on it.
# This is the "hand-rendered" demo flow — no agent skill involved.
demo:
	mkdir -p tests/generated
	sc-compose render --mode file \
		--file templates/vision-centroid.py.j2 \
		--var-file vars.example.json \
		--output tests/generated/test_demo.py
	.venv/bin/pytest tests/generated/test_demo.py -v

# Render the multi-assert template (loops over a list of assertion calls).
demo-multi:
	mkdir -p tests/generated
	sc-compose render --mode file \
		--file templates/vision-multi-assert.py.j2 \
		--var-file vars.multi-assert.json \
		--output tests/generated/test_multi.py
	.venv/bin/pytest tests/generated/test_multi.py -v

# Render the smoke-test template (demonstrates @<path> include of setup_preamble + assert_intensity primitives).
demo-smoke:
	mkdir -p tests/generated
	sc-compose render --mode file \
		--file templates/smoke-test.py.j2 \
		--var-file vars.smoke.json \
		--output tests/generated/test_smoke.py
	.venv/bin/pytest tests/generated/test_smoke.py -v

# Render the engineer-authored example template (demonstrates /hitl-author output).
demo-authored:
	mkdir -p tests/generated
	sc-compose render --mode file \
		--file templates/centroid-with-intensity.py.j2 \
		--var-file vars.centroid-with-intensity.json \
		--output tests/generated/test_authored.py
	.venv/bin/pytest tests/generated/test_authored.py -v

# Wipe generated tests.
clean:
	rm -rf tests/generated/

# Run the repo's own test suite (the tracer bullet, etc.).
test:
	.venv/bin/pytest -v
