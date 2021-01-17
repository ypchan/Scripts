from xml.etree.ElementTree import parse

xml = parse("H:\jupyter\ena_genome_assembly_20201221-0757.xml")

for items in xml.iterfind("ASSEMBLY accession"):
    print(items)
    print(type(items))
