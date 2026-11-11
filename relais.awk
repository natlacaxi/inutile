BEGIN { FS = "\t"; OFS = "\t" }
{ print $1, $2 ">awk" }
