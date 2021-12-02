#!/bin/sh

# Checking the OS so as to use mac specific utilities on MacOS
OS=$(uname)
if [ $OS = 'Darwin' ]
then
    PROGRAM=$(greadlink -f "$0")
else
    PROGRAM=$(readlink -f "$0")
fi

PROGRAM_DIR=$(dirname "$PROGRAM")
# directory where all the art files exist
POKEART_DIR="$PROGRAM_DIR/colorscripts"
# formatting for the help strings
fmt_help="  %-20s\t%-54s\n"


_help(){
    #Function that prints out the help text

    echo "Description: CLI utility to print out unicode image of a anime in your shell"
    echo ""
    echo "Usage: anime-colorscripts [OPTION] [ANIME NAME]"
    printf "${fmt_help}" \
        "-h, --help, help" "Print this help." \
        "-l, --list, list" "Print list of all anime"\
        "-r, --random, random" "Show a random anime. This flag can optionally be
                        followed by a generation number or range (1-8) to show random
                        anime from a specific generation or range of generations.
                        The generations can be provided as a continuous range (eg. 1-3)
                        or as a list of generations (1 3 6)"\
        "-n, --name" "Select anime by name. Generally spelled like in the games.
                        a few exceptions are nidoran-f,nidoran-m,mr-mime,farfetchd,flabebe
                        type-null etc. Perhaps grep the output of --list if in
                        doubt"
    echo "Examples: anime-colorscripts --name pikachu"
    echo "          anime-colorscripts -r"
    echo "          anime-colorscripts -r 1-3"
    echo "          anime-colorscripts -r 1 2 6"
}


# Index values where the different generations are seperated in the names list
# Cannot think of a better way to do arrays with narrow POSIX compliance
# 0-151 gen 1, 810-898 gen 8
indices="1 91"

_show_random_anime(){
    # # Using mac coreutils if on MacOS
    start_index=1
    end_index=91
    if [ $OS = 'Darwin' ]
    then
        random_index=$(gshuf -i "$start_index"-"$end_index" -n 1)
    else
        random_index=$(shuf -i "$start_index"-"$end_index" -n 1)
    fi

    random_anime=$(sed $random_index'q;d' "$PROGRAM_DIR/charalist.txt")
    echo $random_anime

    # print out the anime art for the anime
    cat "$POKEART_DIR/$random_anime.txt"
}

_get_end_index(){
    local i=0
    local gen=$1
    for index in $indices; do
        if [ "$i" = "$gen" ]; then
            echo $index
            break
        fi
        i=$((i + 1))
    done
}

_get_start_index(){
    local i=0
    local gen=$1
    for index in $indices; do
        if [ "$i" = "$((gen-1))" ]; then
            echo $index
            break
        fi
        i=$((i + 1))
    done
}
_show_anime_by_name(){
    anime_name=$1
    echo $anime_name
    # Error handling. Can't think of a better way to do it
    cat "$POKEART_DIR/$anime_name.txt" 2>/dev/null || echo "Invalid anime"
}

_list_anime_names(){
    cat "$PROGRAM_DIR/charalist.txt"|less
}

# Handling command line arguments
case "$#" in
    0)
        # display help if no arguments are given
        _help
        ;;
    1)
        # Check flag and show appropriate output
        case $1 in
            -h | --help | help)
                _help
                ;;
            -r | --random | random)
                _show_random_anime
                ;;
            -l | --list | list)
                _list_anime_names
                ;;
            *)
                echo "Input error."
                exit 1
                ;;
        esac
        ;;

    *)
        if [ "$1" = '-n' ]||[ "$1" = '--name' ]||[ "$1" = 'name' ]; then
            _show_anime_by_name "$2"
        elif [ "$1" = -r ]||[ "$1" = '--random' ]||[ "$1" = 'random' ]; then
            shift
            _show_random_anime $@
        else
            echo "Input error, too many arguments."
            exit 1
        fi
        ;;
esac
