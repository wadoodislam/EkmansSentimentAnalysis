from nltk.parse.stanford import StanfordDependencyParser
#   from nltk import internals
#   internals.config_java("C:/Program Files/Java/jdk1.8.0_102/bin")
path_to_jar = 'C:/stanford-parser-full-2018-02-27/stanford-parser.jar'
path_to_models_jar = 'C:/stanford-parser-full-2018-02-27/stanford-parser-3.9.1' \
                     '-models.jar '
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

result = dependency_parser.raw_parse('I shot an elephant in my sleep')
dep = result.__next__()
temp = list(dep.triples())
print(temp)
