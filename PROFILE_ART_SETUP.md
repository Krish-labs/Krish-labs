# Profile art setup

The profile uses repository-owned SVGs rather than third-party statistics widgets. GitHub Actions refreshes the public contribution calendar daily.

## First run

1. Merge the animated profile README branch into `main`.
2. Open **Actions → Update profile art → Run workflow** to fetch the first contribution calendar. The workflow also regenerates the ASCII avatar and terminal card.
3. The generated SVGs are committed back to the repository automatically.

## Use a personal photo for the ASCII portrait

The default is generated from your public GitHub avatar. For a different image, save it as `source-photo.jpg` in the repository directory on your own computer, then run:

```bash
python -m pip install -r scripts/requirements-daily.txt
python scripts/make_ascii_svg.py source-photo.jpg
```

Review the generated `krish-ascii.svg` and commit it if you want to publish it. Keep private photos out of a public repository unless you intend to make them public. If you want the Actions workflow to keep using that custom photo, store the image in the repository intentionally and adjust the script's source path.

## Local preview

```bash
python -m pip install -r scripts/requirements-daily.txt
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
python scripts/make_ascii_svg.py
python scripts/make_info_card.py
```

The fetcher uses the public GitHub contributions HTML page and does not require a personal access token. GitHub may change that HTML structure; if no contribution cells are found, the script exits with an explanatory error rather than silently producing fake data.
