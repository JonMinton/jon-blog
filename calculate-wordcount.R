library(stringr)
library(yaml)

# Function to calculate word count for a single file, excluding YAML header
count_words <- function(file_path) {
  content <- readLines(file_path)
  
  # Find the end of the YAML header (if it exists)
  yaml_end <- which(content == "---")[2]
  if (is.na(yaml_end)) yaml_end <- 0
  
  # Join all lines after the YAML header
  text <- paste(content[(yaml_end + 1):length(content)], collapse = " ")
  
  # Count words
  word_count <- str_count(text, "\\S+")
  return(word_count)
}

# Get all .qmd files in the blog directory
qmd_files <- list.files(pattern = "\\.qmd$", recursive = TRUE, full.names = TRUE)

# Calculate total word count
total_word_count <- sum(sapply(qmd_files, count_words))

index_qmd <- readLines("index.qmd")

# Find the line with the "subtitle:" field
subtitle_line <- grep("^subtitle:", index_qmd, value = TRUE)

# Update the subtitle line with the new word count
new_subtitle_line <- paste('subtitle: \"About', format(total_word_count, big.mark = ','), 'random words/words on randomness\"')

# Replace the old subtitle line with the new one
index_qmd[which(index_qmd == subtitle_line)] <- new_subtitle_line

# Write the updated index.qmd file
writeLines(index_qmd, "index.qmd")

cat("Total word count:", total_word_count, "\n")
cat("Word count updated in _quarto.yml\n")