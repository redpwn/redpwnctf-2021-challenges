#!/bin/sh

cat >> /tmp/nsjail.cfg << EOF
clone_newnet: false
mount {
  src_content: "nameserver 1.1.1.1"
  dst: "/etc/resolv.conf"
  is_bind: true
}
envar: "RCTF_GOLF_DEBUG"
EOF
