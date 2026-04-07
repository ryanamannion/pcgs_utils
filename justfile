default: 
	just --list

@versions:
	uv version
	uv version --package pcgs_api
	uv version --package pcgs_scraper

@build-docs:
	cd {{justfile_dir()}}/packages/pcgs_api/docs && uv run sphinx-build -b html . _build/html -W --keep-going

open-docs:
	xdg-open {{justfile_dir()}}/packages/pcgs_api/docs/_build/html/index.html
