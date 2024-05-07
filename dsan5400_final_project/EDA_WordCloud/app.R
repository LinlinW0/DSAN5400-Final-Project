library(shiny)

server <- function(input, output, session) {
  # Define a reactive expression for the document term matrix
  terms <- reactive({
    # Change when the "update" button is pressed...
    input$update
    # ...but not for anything else
    isolate({
      withProgress({
        setProgress(message = "Processing corpus...")
        getTermMatrix(input$selection)
      })
    })
  })
  
  # Make the wordcloud drawing predictable during a session
  wordcloud_rep <- repeatable(wordcloud)
  
  output$plot <- renderPlot({
    v <- terms()
    wordcloud_rep(names(v), v, scale=c(3, 1),
                  min.freq = input$freq, max.words=input$max,
                  colors=brewer.pal(8, "Set2"))
  }, width = 800, height = 1000)
}

ui <- fluidPage(
  # Application title
  titlePanel("Word Cloud"),
  
  sidebarLayout(
    # Sidebar with a slider and selection inputs
    sidebarPanel(
      selectInput("selection", "Choose a website:",
                  choices = website),
      actionButton("update", "Change"),
      hr(),
      sliderInput("freq",
                  "Minimum Frequency:",
                  min = 1,  max = 50, value = 15),
      sliderInput("max",
                  "Maximum Number of Words:",
                  min = 1,  max = 300,  value = 100)
    ),
    
    # Show Word Cloud
    mainPanel(
      plotOutput("plot")
    )
  )
)


# Run the application 
shinyApp(ui = ui, server = server)

#rsconnect::setAccountInfo(name='cathyzwn', 
#                          token='B91E7C4DAA5A59090CE561CF3AB7CA59', 
#                          secret='YFodyJqUct2CKsB1M39b7fC8txVrsaI5UY2/FQua')

#library(rsconnect)
#deployApp()
