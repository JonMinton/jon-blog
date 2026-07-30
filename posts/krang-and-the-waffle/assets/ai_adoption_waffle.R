# Regenerated "Each dot is ~N million people" waffle chart, 2023-2026
# Static (latest snapshot) + animated (gganimate) versions.
#
# Requires: tidyverse, gganimate, gifski (for gif rendering)
# Data: ai_adoption_timeseries.csv (tidy; value/low/high in millions)
#
# Categories are converted to mutually exclusive tiers per snapshot:
#   offline (no internet) | online, never used gen AI | free-tier user |
#   paid subscriber | coding-tool user
# Tiers are nested in reality (coding users mostly pay; paid users are users),
# so exclusive counts are formed by subtraction, as in the original chart.

library(tidyverse)
library(gganimate)

n_side <- 50L
n_dots <- n_side^2  # 2,500 dots, matching the original

df <- read_csv("ai_adoption_timeseries.csv", show_col_types = FALSE) |>
  select(snapshot_date, category, value_millions) |>
  pivot_wider(names_from = category, values_from = value_millions) |>
  mutate(
    coding  = coding_tool_users,
    paid    = pmax(paid_subscribers - coding_tool_users, 0),
    free    = pmax(genai_users_ever - paid_subscribers, 0),
    offline = offline_no_internet,
    never_online = world_population - genai_users_ever - offline_no_internet
  ) |>
  select(snapshot_date, world_population,
         offline, never_online, free, paid, coding) |>
  pivot_longer(-c(snapshot_date, world_population),
               names_to = "tier", values_to = "millions") |>
  mutate(tier = factor(
    tier,
    levels = c("offline", "never_online", "free", "paid", "coding"),
    labels = c("Offline (no internet)", "Online, never used gen AI",
               "Free-tier user", "Paid subscriber", "Coding-tool user")
  ))

# Largest-remainder rounding to exactly n_dots per snapshot,
# with a guaranteed minimum of 1 dot for any non-zero tier
# (the original chart made the same choice for the red block).
allocate_dots <- function(millions, total_millions, n = n_dots) {
  raw   <- millions / total_millions * n
  base  <- floor(raw)
  base  <- if_else(millions > 0 & base == 0, 1, base)
  short <- n - sum(base)
  rem   <- raw - floor(raw)
  order_idx <- order(rem, decreasing = TRUE)
  add <- integer(length(millions))
  if (short > 0) add[order_idx[seq_len(short)]] <- 1L
  if (short < 0) {
    # remove from the largest tier(s) if minimums overshot
    big <- order(base, decreasing = TRUE)
    add[big[seq_len(-short)]] <- -1L
  }
  base + add
}

grid <- df |>
  group_by(snapshot_date) |>
  mutate(dots = allocate_dots(millions, first(world_population))) |>
  reframe(tier = rep(tier, dots)) |>
  group_by(snapshot_date) |>
  mutate(idx = row_number() - 1L,
         col = idx %% n_side,
         row = idx %/% n_side) |>
  ungroup()

pal <- c(
  "Offline (no internet)"     = "#A89F93",
  "Online, never used gen AI" = "#D9D5CD",
  "Free-tier user"            = "#6FA877",
  "Paid subscriber"           = "#D9A441",
  "Coding-tool user"          = "#B5493F"
)

base_plot <- function(d) {
  ggplot(d, aes(col, -row, fill = tier)) +
    geom_tile(width = 0.82, height = 0.82) +
    scale_fill_manual(values = pal, name = NULL) +
    coord_equal() +
    theme_void(base_family = "mono") +
    theme(legend.position = "bottom",
          plot.title = element_text(family = "serif", size = 18, hjust = 0.5),
          plot.subtitle = element_text(size = 9, hjust = 0.5,
                                       colour = "grey40"))
}

# ---- Static: latest snapshot --------------------------------------------
latest <- max(grid$snapshot_date)
pop_latest <- df |> filter(snapshot_date == latest) |>
  pull(world_population) |> first()

p_static <- base_plot(filter(grid, snapshot_date == latest)) +
  labs(
    title = sprintf("Each dot is ~%.1f million people",
                    pop_latest / n_dots),
    subtitle = sprintf(
      "2,500 dots = %.2f billion humans. Colour = deepest gen-AI engagement, %s.",
      pop_latest / 1000, format(latest, "%b %Y"))
  )
ggsave("ai_adoption_waffle_latest.png", p_static,
       width = 7, height = 8, dpi = 200)

# ---- Animated: motion chart over all snapshots --------------------------
p_anim <- base_plot(grid) +
  labs(title = "Each dot is ~3.3 million people",
       subtitle = "Deepest gen-AI engagement, {closest_state}") +
  transition_states(snapshot_date, transition_length = 2,
                    state_length = 3) +
  enter_fade() + exit_fade()

anim <- animate(p_anim, nframes = 140, fps = 12,
                width = 700, height = 800, renderer = gifski_renderer())
anim_save("ai_adoption_waffle_motion.gif", anim)

# Note: dot identity is positional, so tiles recolour in place as bands
# grow -- visually this reads as the green/amber/red bands advancing up
# the grid, which is the intended effect.
