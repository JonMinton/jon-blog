# wordcount.R
files <- list.files(pattern = "\\.qmd$", recursive = TRUE)

# Count words in each file
total_words <- sum(sapply(files, function(f) {
  text <- readLines(f, warn = FALSE)
  # Strip YAML front matter
  text <- text[!grepl("^---$", text)]
  words <- unlist(strsplit(paste(text, collapse = " "), "\\s+"))
  length(words)
}))

# Save to file for Quarto to read
writeLines(as.character(total_words), "wordcount.txt")