Impact Factor
Time limit: 1000 ms
Memory limit: 256 MB

IEEE Xplore
Warm greetings to all IEEExtreme Participants from the Xplore API Team!

As part of the IEEExtreme Competition, you will be tasked with a programming challenge to determine the Impact Factor of an academic journal. The input content file of this exercise is static (non changing) to allow for consistent results during this competition.

For a full dynamic database search IEEE Xplore API is available for your IEEE research needs. Xplore API provides metadata on 4.9mm academic works and is now delivering full-text content on 50k 'Open Access' articles. Xplore API will make your research needs fast and easy. The Xplore API Portal supports PHP, Python and Java as well as providing output in Json and XML formats. Many API use cases are listed within the API Portal.

Xplore API registration is free. To learn more about IEEE Xplore API please visit developer.ieee.org/ and register for an API key TODAY!

Challenge
The impact factor (IF) of an academic journal is a scientometric index which reflects the yearly average number of citations to recent articles published in that journal. In any given year, the impact factor of a journal is the number of citations, received in that year, of articles published in that journal during the two preceding years, divided by the total number of citable items published in that journal during the two preceding years:

\mathrm{IF}_y = \dfrac{\mathrm{Citations}_{y-1} + \mathrm{Citations}_{y-2}}{\mathrm{Publications}_{y-1} + \mathrm{Publications}_{y-2}}IF
​y
​​ =
​Publications
​y−1
​​ +Publications
​y−2
​​
​
​Citations
​y−1
​​ +Citations
​y−2
​​
​​

Standard input
The first line is the number of records to process. The second line is the publications to be included in the report. The publicationNumber is the unique key to identify the publication. The publicationTitle is the title of the publication. The articleCounts array contains the year and articleCount for that year and publication.

The subsequent lines are JSON packets containing citations for random publications. The paperCitations contains an array, called ieee, with information about the cited papers. The publicationNumber in the array is the publication number of the publication the cited article appears in. The year is the year the article was published.

Standard output
List the publication title and its Impact Factor. Order by descending Impact Factor. Format the output with one journal name per line and with the name and the score (with two decimal places) separated by a colon. Example: Letters on IEEEXtreme: 1.78

In case multiple publications have the same impact factor, print them in alphanumerical order.

Constraints and notes
The maximum number of records is 1001
