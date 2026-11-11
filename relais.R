l <- readLines(file("stdin"), n = 1)
p <- strsplit(l, "\t", fixed = TRUE)[[1]]
cat(p[1], "\t", paste(p[-1], collapse = "\t"), ">R\n", sep = "")
