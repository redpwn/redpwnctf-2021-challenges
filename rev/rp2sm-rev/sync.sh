#!/bin/sh

basedir=$(dirname "$0")

if [ $# -lt 1 ] || [ ! -d "$1" ] || [ ! -e "$1/pack/source.tar" ] || [ ! -e "$1/pack/dist.tar" ]; then
	echo "usage: $0 <path to rp2sm repo>" >&2
	echo "Packed tarballs must be already built" >&2
	exit 1
fi

rm -rf rp2sm
cp "$1/pack/dist.tar" "$basedir/"
tar -xf "$1/pack/source.tar"
cat <<EOF >rp2sm/.dockerignore
solve
EOF
