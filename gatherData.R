library("readxl")
library("tidyverse")


df = read_csv("raw_data.csv")

# gather prices with time as key
df2 <- df %>% 
  gather("time", "price", c(starts_with("2"))) %>%
  mutate(year = substr(time, 1,4),
         month = substr(time,5,6),
         day = substr(time,7,8),
         time = as.Date(time, format = "%Y%m%d"))

data.table::fwrite(df2, "medicine_prices.csv")

