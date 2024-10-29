# Application backend

Install dependencies:

```sh
# Unix
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

To add `uv` to your `$PATH`, follow the instructions that were printed out when you ran one of the above commands to install it.

Run the API:

```sh
uv run uvicorn api.main:app --reload
```
