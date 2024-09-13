from Bio.KEGG import REST
import requests
import json


def queryPathGenes(db_source, pathway_id):
    ## request api and check status: get or return string
    if db_source == 'kegg_db':
        get_pathway = requests.get('http://rest.kegg.jp/get/{}'.format(pathway_id))
        if get_pathway.status_code == 200:
            gene_pathway = REST.kegg_get(pathway_id).read().split("\n")
            gene_lists = []
            checkpt = False

            for index in gene_pathway:
                if 'GENE' in index:
                   checkpt = True
        
                if 'COMPOUND' in index:
                    checkpt = False

                if checkpt == True:
                    if not ';' in index or 'KO:' not in index: ## for missing gene name case, and double-check gene by [KO:xxx]
                        continue
                    else:
                        tmp = index.strip().split(';')[0]
                        tmp1 = tmp.strip().split('  ')[-1]
                        gene_lists.append(tmp1)
    
        #print(gene_lists)
            return gene_lists
        else:
            return 'Fail due to {}'.format(get_pathway.status_code)

        
    elif db_source == 'harmo_db':
        # break_url = pathway_id.split('/')
        # _tmp = 0
        # for i in range(len(break_url)):
        #     if break_url[i] == 'gene_set':
        #         _tmp = i
        # query_url = '/'.join(break_url[_tmp:])
        # query_url_comb = 'https://maayanlab.cloud/Harmonizome/api/1.0/gene_set/{}'.format(query_url)
        # get_pathway = requests.get(query_url_comb)

        spl_gene = pathway_id.split('_')[0]
        spl_set = pathway_id.split('_')[1]
        get_pathway = requests.get('https://maayanlab.cloud/Harmonizome/api/1.0/gene_set/{}/{}'.format(spl_gene, spl_set))
        
        if get_pathway.status_code == 200:
            geneset = get_pathway.json()

            #print(geneset['associations'])

            gene_lists = []
            for key,val in enumerate(geneset['associations']):
                tmp = val['gene']['symbol']
                gene_lists.append(tmp)

            return gene_lists
        
        else:
            return 'Fail due to {}'.format(get_pathway.status_code)



if __name__ == '__main__':
    queryPathGenes()