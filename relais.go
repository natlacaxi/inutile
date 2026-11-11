package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	l, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	p := strings.SplitN(strings.TrimRight(l, "\r\n"), "\t", 2)
	fmt.Printf("%s\t%s>Go\n", p[0], p[1])
}
