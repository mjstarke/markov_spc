import markov

paragraphs = markov.read_paragraphs("sample.txt", ("SUMMARY...", "DISCUSSION...", "\n"))
paragraphs = markov.random_slice(paragraphs, len(paragraphs) // 2)
superdict = markov.create_superdict(paragraphs)
for _ in range(5):
    print(markov.generate_text(superdict))
    print()
