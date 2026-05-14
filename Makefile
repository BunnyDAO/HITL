.PHONY: demo clean test

# Render vision-centroid into tests/generated/test_demo.py and run pytest on it.
# This is the "hand-rendered" demo flow — no agent skill involved.
demo:
	mkdir -p tests/generated
	sc-compose render --mode file \
		--file templates/vision-centroid.py.j2 \
		--var-file vars.example.json \
		--output tests/generated/test_demo.py
	.venv/bin/pytest tests/generated/ -v

# Wipe generated tests.
clean:
	rm -rf tests/generated/

# Run the repo's own test suite (the tracer bullet, etc.).
test:
	.venv/bin/pytest -v
