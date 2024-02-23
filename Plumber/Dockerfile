FROM rstudio/plumber:latest

RUN Rscript -e 'remotes::install_version("tidyverse",upgrade="never", version = "1.3.2")'
RUN R -e 'install.packages("ggnewscale")'