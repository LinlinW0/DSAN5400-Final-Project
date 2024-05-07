library(tm)
library(wordcloud)
library(memoise)

# The list of valid books
website <<- list("IMDB" = "df_imdb",
               "Rotten Tomato: Audiences" = "df_rt_audience",
               "Rotten Tomato: Critics" = "df_rt_critics")
getwd()

df_imdb <- read.csv("data/reviews_imdb_cleaned.csv")
df_imdb$Review <- df_imdb$reviewText

df_rt_audience <- read.csv("data/movie_reviews_rottentomato_audience.csv")

df_rt_critics <- read.csv("data/critics_reviews.csv")

df_list <- list(df_imdb = df_imdb, df_rt_audience = df_rt_audience, df_rt_critics = df_rt_critics)


for (df_name in names(df_list)) {
  df <- df_list[[df_name]]
  if ("Review" %in% names(df)) {
    concatenated_reviews <- paste(df$Review, collapse = " ")
    txt_file <- paste0(getwd(), "/data/", df_name, ".txt")
    writeLines(concatenated_reviews, txt_file)
  } else {
    warning(paste("DataFrame", df_name, "does not have a 'Review' column."))
  }
}

getwd()
# Using "memoise" to automatically cache the results
getTermMatrix <- memoise(
  function(df_name) {
    txt_filename <- paste0("/Users/ziningwang/dsan5400/finalproject/data/", df_name, ".txt")
    
    if (!file.exists(txt_filename)) {
      stop("The text file does not exist: ", txt_filename)
    }
    
    # Read the text file
    text <- readLines(paste0("/Users/ziningwang/dsan5400/finalproject/data/", df_name, ".txt"), encoding = "UTF-8")
    
    myCorpus = Corpus(VectorSource(text))
    myCorpus = tm_map(myCorpus, content_transformer(tolower))
    myCorpus = tm_map(myCorpus, removePunctuation)
    myCorpus = tm_map(myCorpus, removeNumbers)
    myCorpus = tm_map(myCorpus, removeWords, c(stopwords("SMART"), "movie", "film"))
    
    # Convert corpus to a plain text vector for sampling
    plainTextVector <- sapply(myCorpus, as.character)
    allWords <- unlist(strsplit(plainTextVector, "\\s+"))
    
    # Check if there are enough words to sample
    if (length(allWords) < 10000) {
      stop("Not enough words to sample 10,000 words from ", df_name)
    }
    
    # Sample 10,000 words randomly
    sampledWords <- sample(allWords, 10000, replace = FALSE)
    
    # Rebuild a corpus from the sampled words
    sampledCorpus = Corpus(VectorSource(sampledWords))
    
    myDTM = TermDocumentMatrix(sampledCorpus,
                               control = list(minWordLength = 1))
    
    m = as.matrix(myDTM)
    
    sort(rowSums(m), decreasing = TRUE)
  }
)

#getwd()
#text <- readLines("WorldCloudDSAN5400/df_imdb.txt", warn = FALSE)

# Combine lines into a single string if necessary
#text_combined <- paste(text, collapse = " ")

#library(stringr)
# Use str_split to split the text into words based on whitespace
#words <- str_split(text_combined, "\\s+")

# Count the number of words
#num_words <- length(unlist(words))
