#!/usr/bin/env python

from bs4 import BeautifulSoup

html_doc="""&lt;div class=&#34;hnews hentry item&#34;&gt;
  &lt;h4&gt;
    &lt;a class=&#34;url entry-title&#34; href=&#34;http://hosted2.ap.org/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5/Article_2015-06-25-AS--Pakistan-Heat Wave/id-52c62b13029a4cdebb0997d28753ab0e&#34; rel=&#34;bookmark&#34;&gt;Heat wave subsides in Pakistan as death toll reaches 860&lt;/a&gt;
  &lt;/h4&gt;
  &lt;div&gt;
    &lt;small&gt; &lt;span class=&#34;source-org author vcard&#34;&gt;&lt;a class=&#34;url org fn&#34; href=&#34;http://www.ap.org&#34;&gt;Associated Press&lt;/a&gt;&lt;/span&gt;&lt;a href=&#34;http://www.ap.org/newsvalues/index.html&#34; rel=&#34;principles&#34; title=&#34;THE ASSOCIATED PRESS STATEMENT OF NEWS VALUES AND PRINCIPLES&#34;&gt;&lt;img alt=&#34;THE ASSOCIATED PRESS STATEMENT OF NEWS VALUES AND PRINCIPLES&#34; src=&#34;http://hosted2.ap.org/NewsArchive/images/icon/principles-book-blue.png&#34; style=&#34;border-style: none;&#34; /&gt;&lt;/a&gt; - &lt;span class=&#34;updated dtstamp&#34; title=&#34;2015-06-25T19:08:45Z&#34;&gt;25 June 2015 15:08-04:00&lt;/span&gt;&lt;/small&gt;
  &lt;/div&gt;
  &lt;div&gt;&lt;/div&gt;
  &lt;small id=&#34;license-9d663d39-3d54-4663-b2d9-5d7b505bdaf1&#34;&gt;
    &lt;a href=&#34;http://hosted2.ap.org/atom/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5#license-9d663d39-3d54-4663-b2d9-5d7b505bdaf1&#34; rel=&#34;item-license&#34;&gt;Copyright 2015 The Associated Press. All rights reserved. This material may not be published, broadcast, rewritten or redistributed.&lt;/a&gt;
  &lt;/small&gt;
  &lt;img alt=&#34;&#34; height=&#34;1&#34; src=&#34;http://analytics.apnewsregistry.com/analytics/V2/Image.svc/AP/E/prod/PC/Basic/RWS/hosted2.ap.org/CAI/c1de9719257649308bd7847395f02b50/CVI/52c62b13029a4cdebb0997d28753ab0e/AT/H&#34; width=&#34;1&#34; /&gt;
&lt;/div&gt;"""

soup = BeautifulSoup(html_doc, "lxml")
print(soup.prettify())
