# python main.py < testcase1.txt

import json
import sys
import io

def readInt(reader):
    line = reader.readline().replace("\n", "")
    if line == "":
        return None
    else:
        return int(line)

def readString(reader):
    return reader.readline().replace("\n", "")

class Article:

    citations = 0

    def __init__(self, year, publications):
        self.year = year
        self.publications = publications

class Publication:

    IF = 0

    def __init__(self, publicationNumber, publicationTitle, articles):
        self.publicationNumber = publicationNumber
        self.publicationTitle = publicationTitle
        self.articles = articles

def main(argv):

    reader = io.open(sys.stdin.fileno())

    # N: number of articles
    # N <= 1001
    N = readInt(reader)
    #print(N)

    json_publications = json.loads(readString(reader))
    #print(json_publications)

    """
    The publicationNumber is the unique key to identify the publication. 
    The publicationTitle is the title of the publication. 
    The articleCounts array contains the year and articleCount for that year and publication.
    """
    publications = {}
    for json_publication in json_publications["publications"]:
        publicationNumber = json_publication["publicationNumber"]
        publicationTitle = json_publication["publicationTitle"]
        articleCounts = {}
        for json_article_count in json_publication["articleCounts"]:
            year = int(json_article_count["year"])
            article = Article(year, int(json_article_count["articleCount"]))
            articleCounts[year] = article
        publication = Publication(publicationNumber, publicationTitle, articleCounts)
        publications[publicationNumber] = publication
    """
    for publication in list(publications.items()):
        print(publication[1].articles)
    """

    for i in range(N-1):

        json_data = json.loads(readString(reader))
        #print(json_data)

        """
        The paperCitations contains an array, called ieee, with information about the cited papers. 
        The publicationNumber in the array is the publication number of the publication the cited article appears in. 
        The year is the year the article was published.
        """
        for json_citation in json_data["paperCitations"]["ieee"]:
            #print(json_citation)
            publicationNumber = json_citation["publicationNumber"]
            year = int(json_citation["year"])
            if publicationNumber in publications:
                publication = publications[publicationNumber]
                if year in publication.articles:
                    publication.articles[year].citations = publication.articles[year].citations + 1
                    #print(publication.articles[year].citations)

        # article_number = json_data["article_number"]
        # print(article_number)

    result = {}
    for publication in publications.values():
        year_1 = 2018
        year_2 = 2017
        citations_1 = 0
        publications_1 = 0
        if year_1 in publication.articles:
            citations_1 = publication.articles[year_1].citations
            publications_1 = publication.articles[year_1].publications
        citations_2 = 0
        publications_2 = 0
        if year_2 in publication.articles:
            citations_2 = publication.articles[year_2].citations
            publications_2 = publication.articles[year_2].publications
        if citations_1 == 0 and publications_1 == 0 and citations_2 == 0 and publications_2 == 0:
            IF = 0
        elif publications_1 + publications_2 == 0:
            IF = 0
        else:
            IF = float(citations_1+citations_2) / float(publications_1+publications_2)
        publication.IF = IF
        result[publication.publicationTitle] = myRound(IF)
        #print(publication.publicationTitle+": "+myRound(IF))

    # Order by descending Impact Factor.
    sorted_result = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
    for title, IF in sorted_result:
        print(title+": "+IF)

def myRound(n):
    return "%.2f" % round(n, 2)

if __name__ == "__main__":
    main(sys.argv)