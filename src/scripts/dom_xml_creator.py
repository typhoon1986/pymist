import xml.dom.minidom
import sys, os
import codecs

def create_xml(clientname, tpls):
    if not len(tpls) == 7:
        print "%s, templates not in good format"
        return None
    
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, ''.join(("dom-",clientname)), None)
    root = dom.documentElement
    root.setAttribute("name", clientname)
    root.setAttribute("cid", clientname)
    root.setAttribute("sep", "")
    root.setAttribute("dns", "")
    root.setAttribute("alias", "")
    required = dom.createElement("required-field")
    required.appendChild(dom.createTextNode('price'))
    root.appendChild(required)
    urlfilter = dom.createElement("urlfilter")
    urlfilter.setAttribute("regex", ".*\d{5,}.html$")
    root.appendChild(urlfilter)
    
    path = dom.createElement("path")
    path.setAttribute("root", "html/body")
    root.appendChild(path)
    
    template = dom.createElement("template")
    template.setAttribute("root", "")
    template.setAttribute("required", "attribute,detail")
    
    names = ["name", "price", "category", "img", "brand", "attribute", "detail"]
    for idx, tpl in enumerate(tpls):
        tpl = tpl.strip()
        field = dom.createElement("field")
        field.setAttribute("type", "dom")
        field.setAttribute("name", names[idx])
        field.setAttribute("path", tpl)
        template.appendChild(field)
    
    root.appendChild(template)
    # debug
    #print root.toxml()
    
    
    f=file(''.join((clientname,".xml")), 'w')

    writer = codecs.lookup('utf-8')[3](f)
    dom.writexml(writer, encoding='utf-8')
    writer.close()


if __name__ == "__main__":
    # test:
    #create_xml("test", ["aaa","bbb","ccc", "ddd", "eee","fff", "ggg"])
    if not len(sys.argv) == 2:
        print "Usage: python dom_xml_creator.py [template input file]"
        print "will genrate xml files in current dir"
        exit(1)
        
    if not os.access(sys.argv[1], os.R_OK):
        print "file not found"
        exit(1)
        
    fn = open(sys.argv[1], "r")
    linetype = 1
    for line in fn.readlines():
        if linetype == 1:
            clientname = line.strip()
            print "parsing for client: %s"%clientname
            linetype = 2 
        elif linetype == 2:
            tpls = line.split(",")
            create_xml(clientname, tpls)
            linetype = 1