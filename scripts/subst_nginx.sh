#!/usr/bin/env bash

TEMPLATES_PATH=/tmp/scripts
NGINX_CONFIG="/etc/nginx/conf.d/default.conf"

if [[ "${SSL}" == "True" ]]; then
    NGINX_TEMPLATE="${TEMPLATES_PATH}/nginx.conf_ssl.template"
else
    NGINX_TEMPLATE="${TEMPLATES_PATH}/nginx.conf.template"
fi


sed -e 's#${BACKEND}#'"${BACKEND}"'#g' -e \
    's#${BACKEND_PORT}#'"${BACKEND_PORT}"'#g' -e \
    's#${PORT}#'"${PORT}"'#g' -e \
    's#${HOST}#'"${HOST}"'#g' -e \
    's#${SSL_PORT}#'"${SSL_PORT}"'#g' -e \
    's#${SSL_KEYS_PATH}#'"${SSL_KEYS_PATH}"'#g' -e \
    's#${SSL_CERTIFICATE}#'"${SSL_CERTIFICATE}"'#g' -e \
    's#${SSL_CERTIFICATE_KEY}#'"${SSL_CERTIFICATE_KEY}"'#g' -e \
    's#${SSL_DHPARAM}#'"${SSL_DHPARAM}"'#g' -e \
    's#${ROOT}#'"${ROOT}"'#g' < ${NGINX_TEMPLATE} > ${NGINX_CONFIG}
