#!/bin/bash

set -eu pipefail

# Move to the top-level directory of your git repo
static_dir="$(git rev-parse --show-toplevel)/src/frontend/frontend/static"

# Define URLs and target directories
declare -A files=(
  ["https://cdn.jsdelivr.net/npm/tom-select/dist/css/tom-select.css"]="${static_dir}/css/tom-select.css"
  ["https://cdn.jsdelivr.net/npm/tom-select/dist/js/tom-select.complete.min.js"]="${static_dir}/js/tom-select.complete.min.js"
  ["https://cdn.jsdelivr.net/npm/tom-select/dist/js/tom-select.complete.min.js.map"]="${static_dir}/js/tom-select.complete.min.js.map"
  ["https://cdn.jsdelivr.net/npm/alpinejs/dist/cdn.min.js"]="${static_dir}/js/alpinejs.min.js"
  ["https://cdn.jsdelivr.net/npm/fuse.js/dist/fuse.js"]="${static_dir}/js/fuse.js"
  ["https://cdn.jsdelivr.net/npm/htmx.org/dist/htmx.min.js"]="${static_dir}/js/htmx.min.js"
  ["https://github.com/saadeghi/daisyui/releases/latest/download/daisyui.js"]=${static_dir}/js/daisyui.js
)

# Download the latest versions
for url in "${!files[@]}"; do
  target="${files[$url]}"
  echo "Downloading $url to $target"
  curl --retry 3 --retry-delay 5 --fail --silent --show-error --location "$url" -o "$target"
done

echo "All files downloaded successfully."