gets stdin l
set i [string first "\t" $l]
puts "[string range $l 0 [expr {$i-1}]]\t[string range $l [expr {$i+1}] end]>Tcl"
