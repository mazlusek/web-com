#!/usr/bin/env bash
# Regenerates the site from the generator, refreshes the ConfigMaps and restarts the LAN preview.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
SITE="$DIR/../web-com"
NS=mazlusek-web-preview

python3 -I "$DIR/build.py" "$SITE"

kubectl apply -f "$DIR/preview.yaml"

cm() {
  local name="$1"; shift
  kubectl -n "$NS" create configmap "$name" "$@" --dry-run=client -o yaml | kubectl apply -f -
}
cm site-root --from-file="$SITE/index.html" --from-file="$SITE/404.html" --from-file="$SITE/style.css" \
  --from-file="$SITE/app.js" --from-file="$SITE/favicon.svg" --from-file="$SITE/robots.txt" --from-file="$SITE/sitemap.xml"
cm site-en --from-file="$SITE/en/index.html"
cm site-privacy --from-file="$SITE/privacy/index.html"
cm site-en-privacy --from-file="$SITE/en/privacy/index.html"

kubectl -n "$NS" rollout restart deployment/web-preview
kubectl -n "$NS" rollout status deployment/web-preview --timeout=120s
