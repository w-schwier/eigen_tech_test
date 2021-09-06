from texttable import Texttable


def get_table_from_dict(word_stats: dict, max_table_width: int = 140):
    table = Texttable(max_width=max_table_width)
    table.header(["Word", "No.", "Document", "Sentence"])

    for word in word_stats.items():
        for location in word[1]["locations"]:
            table.add_row([word[0], word[1]["count"], location["document"], location["sentence"]])

    return table.draw()
