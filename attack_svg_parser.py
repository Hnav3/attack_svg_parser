import xml.etree.ElementTree as ET
import csv
import argparse

def arg_parse():
    """Function to handle script arguments."""
    parser = argparse.ArgumentParser(description = "Parses SVG file dumped from ATT&CK Navigator and maps Technique IDs to svg object ids. To be used for Splunk Chloropleth SVG dashboarding.")
    parser.add_argument('input_file', type=str, help="SVG file to parse.")
    return parser


def main(args):
    tree = ET.parse(args.input_file)
    root = tree.getroot()


    ns_array = {
        'svg':'http://www.w3.org/2000/svg',
        'xlink':'http://www.w3.org.1999/xlink',
        'rec':'http://www.w3.org/2000/svg'
    }

    #tactic layer
    lst = root.findall('svg:g/svg:g/svg:g/svg:g', ns_array)
    
    writeable_results = []
    recid=1
    for l in lst:
        for sub in l:
            if sub.attrib['class'] == 'techniques':
                 for tech in sub:
                     technique_id = tech.attrib['class'].split(' ')
                     technique_id = technique_id[1]
                     for obj in tech:
                          for rec in obj.iter('{http://www.w3.org/2000/svg}rect'):
                              rec_id = 'rect'+str(recid)
                              rec.set('id',rec_id)
                              recid=recid+1
                              tech_obj = {'technique_id':technique_id, 'rec_id':rec_id}
                              writeable_results.append(tech_obj)

    csv_fields = ['technique_id','rec_id']
    with open("tech_to_rec.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(writeable_results)


if __name__ == "__main__":
    parser = arg_parse()
    args = parser.parse_args()
    main(args)
