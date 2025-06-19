# ProToxin-webserver
A web server to predict proteins' toxin via Streamlit.

## Dockerfile build instruction
The developer's computer is Macintosh with arm64 architecture. The Dockerfile is built for arm64 architecture.
If you want to build an image for amd64 arch in arm64 mac, run the following command:
```bash
docker buildx build --platform linux/amd64 -t nullland1027:0.1.0-amd64 . --load
```
