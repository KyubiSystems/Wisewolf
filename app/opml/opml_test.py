#!/usr/bin/env python
"""
Testing OPML import
(c) 2015 KyubiSystems: www.kyubi.co.uk
"""
import Opml

#o = Opml.OpmlReader('./testing.xml')
o = Opml.OpmlReader('./opml-example.xml')

o.parseOpml()
