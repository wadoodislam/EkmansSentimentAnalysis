from SourceFiles.SA_Module import SentimentAnalysis


example_text = "I was disappointed and angry at the bad quality of a documentary program on TV. In my opinion, " \
               "the topic was important and the program should have been made with seriousness and consideration."
SA = SentimentAnalysis()
print(SA.analyze(example_text))
