#!/bin/sh

# A basic install script for anime-colorscripts

INSTALL_DIR='/usr/local/opt'
BIN_DIR='/usr/local/bin'

# deleting directory if it already exists
rm -rf $INSTALL_DIR/anime-colorscripts || return 1

# making the necessary folder structure
mkdir -p $INSTALL_DIR/anime-colorscripts || return 1

# moving all the files to appropriate locations
cp -rf colorscripts $INSTALL_DIR/anime-colorscripts
cp anime-colorscripts.sh $INSTALL_DIR/anime-colorscripts
cp charalist.txt $INSTALL_DIR/anime-colorscripts

# create symlink in usr/bin
rm -rf $BIN_DIR/anime-colorscripts || return 1
ln -s $INSTALL_DIR/anime-colorscripts/anime-colorscripts.sh $BIN_DIR/anime-colorscripts

