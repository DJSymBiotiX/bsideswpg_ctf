#!/bin/sh

extract_file () {
    x=${1}
    file=`ls -1 tootsie-$x*`
    ext=`basename $file | cut -d. -f2`

    if [ "$ext" = "zip" ] ; then
        unzip $file
    elif [ "$ext" = "rar" ] ; then
        unrar e $file
    elif [ "$ext" = "7z" ] ; then
        7z e $file
    else
        tar xvf $file
    fi
}

# Extract first tar
tar xvf tootsie.tar.gz

# Extract 998 to 1
for x in $(seq -w 998 -1 1) ; do
    extract_file $x
done

# Extract remaining files
for x in $(seq -w 99999 -1 99990) ; do
    extract_file $x
done

# Show solution
echo -n "Solution: "
echo `cat the-center.txt`

exit 0
