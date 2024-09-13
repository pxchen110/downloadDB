import os

def refineUrl(db_source, pathway_query):
    if db_source == 'kegg_db':
        if 'http' in pathway_query:
            splstr = pathway_query.strip().split('/')[-1] ## always get the last one 
            if ':' in splstr:
                pathway_name = str(splstr.replace(':',''))
            else:
                pathway_name = str(splstr)
        else:
            if ':' in pathway_query:
                pathway_name = str(pathway_query.strip().replace(':',''))
            else:
                pathway_name = str(pathway_query.strip())
            
    elif db_source == 'harmo_db':
        if 'http' in pathway_query:
            splstr = "_".join(pathway_query.strip().split('/')[-2:])
            pathway_name = splstr
        else: 
            repstr = pathway_query.replace('/','_')
            pathway_name = str(repstr)

    return pathway_name

if __name__ == '__main__':
    refineUrl()