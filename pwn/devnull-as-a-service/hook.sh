#!/bin/sh

cat >> /tmp/nsjail.cfg << EOF
mount {
  dst: "/tmp"
  fstype: "tmpfs"
  rw: true
  options: "size=0"
  nosuid: true
  nodev: true
  noexec: true
}
EOF
