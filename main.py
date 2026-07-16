"""Project entrypoint: run the Krishiva AI backend with uvicorn."""

import uvicorn


def main() -> None:
    """Start the development server."""

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
