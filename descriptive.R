

df <- data.table::fread("medicine_prices.csv")


# simple plot of average price by year
df %>%
  group_by(time) %>%
  summarise(price = mean(price, na.rm = TRUE)) %>%
  ungroup() %>%
  mutate(time = as.Date(time)) %>%
  ggplot(aes(x=time, y =price)) +
    geom_line() +
    theme_bw() +
    labs(title = "Average price of all drugs") +
    xlab("Year") +
    ylab("Price (DKK)")

ggsave("img/averages.png")
