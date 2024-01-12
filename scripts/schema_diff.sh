#!/usr/bin/env bash

# The following script prints differences in settings schema between two tags.

# exit when any command fails
set -e

REPO_URL="https://github.com/python-lsp/python-lsp-server"
TEMP_REPO_DIR=$(echo "${REPO_URL}" | command grep -oE '[^/]*$')

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_DIR="$SCRIPT_DIR/.."

if [ "$#" -ne 2 ]; then
   echo 'You must provide 2 arguments - two tags between which to check for diffrences in schema.'
   exit 1
fi

function download_repo_by_tag {
   tag=$1

   if [ ! "$tag" ]; then
      exit "No tag provided"
   fi

   pushd "${REPO_DIR}" > /dev/null || exit

   archive_url="${REPO_URL}/archive/${tag}.zip"
   temp_zip="src-${tag}.zip"
   curl -L "${REPO_URL}/archive/${tag}.zip" -o "${temp_zip}" --silent --show-error
   unzip -q "${temp_zip}"
   rm -f "${temp_zip}" || exit
   mv "${TEMP_REPO_DIR}-"* "${TEMP_REPO_DIR}"
}

tag_from=$1
tag_to=$2

download_repo_by_tag "$tag_from"
schema_from=$(cat "${TEMP_REPO_DIR}/pylsp/config/schema.json")
rm -rf "${TEMP_REPO_DIR}"

download_repo_by_tag "$tag_to"
schema_to=$(cat "${TEMP_REPO_DIR}/pylsp/config/schema.json")
rm -rf "${TEMP_REPO_DIR}"

# This will exit with error code on changes. Make sure to not rely on anything running after it.
diff -u <(echo "$schema_from") <(echo "$schema_to") && echo "No changes"
