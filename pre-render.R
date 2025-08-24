# Capture warnings
warning_messages <- capture.output({
  withCallingHandlers({
    source("calculate-wordcount.R")
  }, warning = function(w) {
    message("WARNING: ", conditionMessage(w))
    invokeRestart("muffleWarning")
  })
}, type = "message")

# Print captured warnings
cat("Captured warnings:\n")
cat(warning_messages, sep = "\n")

# Write warnings to a file
writeLines(warning_messages, "render_warnings.log")