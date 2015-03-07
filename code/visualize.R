library(dplyr)
library(ggplot2)

options(stringsAsFactors = FALSE)

annotation.dirs <- file.path('annotations', list.files('annotations'))

for (annotation.dir in annotation.dirs) {
  
  annotation.df <- dplyr::bind_rows(
    file.path(annotation.dir, 'annotations-unprop.tsv') %>%
      read.delim() %>%
      dplyr::mutate(propagation = 'unpropagated'),
    file.path(annotation.dir, 'annotations-prop.tsv') %>%
      read.delim() %>%
      dplyr::mutate(propagation = 'propagated')) %>%
    dplyr::mutate(propagation = factor(propagation, levels=c('unpropagated', 'propagated')))

  gg <- annotation.df %>%
    ggplot(aes(x = size, fill = propagation)) +
    geom_density(alpha = 0.42, color = NA, adjust = 2) +
    scale_x_log10(breaks = c(1, 2, 3, 5, 10, 25, 100, 1000, 5000)) +
    scale_y_sqrt() +
    theme_bw() +
    scale_fill_manual(name = '', values = c("#FF0000", "#0000FF")) +
    theme(legend.justification = c(1, 1), legend.position = c(1, 1)) +
    xlab('Number of annotated genes per GO term') + ylab('Density')

  file.path(annotation.dir, 'annotations.svg') %>%
    ggsave(width = 5, height = 4)

}
