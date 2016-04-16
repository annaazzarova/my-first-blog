import feedparser
d = feedparser.parse('http://гранитанца.рф')
for e in d.entries:
    print ("Title: " + e.title)
    print ("Link: " + e.link)
    print ("Content: " + e.summary)