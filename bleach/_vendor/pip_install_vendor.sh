#!/bin/bash

# installs and patches vendored dependencies into env var DEST which
# defaults to the CWD
#
# runs from bleach/_vendor
SCRIPTPATH=$(dirname "$(readlink -f "$0")")

DEST=${DEST:-"$(pwd)"}
echo "installing vendored packages into ${DEST}"

pip install --upgrade --no-binary all --no-compile --no-deps -r "${SCRIPTPATH}/vendor.txt" --target "${DEST}"
rm -rf "${DEST}/bin/"

# keep django django/core/validators.py and init files to import it
# remove everything else
echo "cleaning files in ${DEST}/django"
find "${DEST}/django" -type f -not -wholename "${DEST}/django/core/validators.py" -delete
find "${DEST}/django" -empty -type d -delete
touch "${DEST}/django/__init__.py" "${DEST}/django/core/__init__.py"

# patch django/core/validators.py so we don't need the rest of django and expose the regexes we want to use
# NB: can't use git apply since vendor_verify.sh runs in a temp dir
echo "patching file in ${DEST} with ${SCRIPTPATH}/0001-patch-validator.patch"
patch --directory="${DEST}" --batch -p3 < "${SCRIPTPATH}/0001-patch-validator.patch"
