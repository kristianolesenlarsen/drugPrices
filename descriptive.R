library(tidyverse)

df <- data.table::fread("medicine_prices.csv")


# simple plot of average price by year
df %>%
  filter(substr(Variabel,1,1) == "a") %>%
  mutate(Variabel = ifelse(Variabel == "aip", "Apotekets indkøbspris", "Registerpris")) %>%
  group_by(time, Variabel) %>%
  summarise(price = mean(price, na.rm = TRUE)) %>%
  ungroup() %>%
  mutate(time = as.Date(time)) %>%
  ggplot(aes(x=time, y =price, color = Variabel)) +
    geom_line() +
    theme_bw() +
    labs(title = "Average price of all drugs") +
    xlab("Year") +
    ylab("Price (DKK)") +
  theme(legend.position = "bottom") +
  guides(fill=guide_legend(title="Price type")) +
  scale_color_manual(values = c("red", "blue"))

ggsave("img/averages.png")

