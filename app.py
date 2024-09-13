# pip install Flask
from flask import Flask
from flask import render_template, request, send_from_directory, send_file
from flask import url_for, redirect, flash
from refine_pathway_url import refineUrl # type: ignore
from request_db_api import queryPathGenes
from save_output import saveOutput, saveZipOutput # type: ignore
import os, json
import zipfile
from io import BytesIO
from zipfile import ZipFile




app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def getPath():
    if request.method == 'POST':
        db_source = request.form.get('db_source')
        #pathway_query = request.form.get('pathway_name')


        ## check if file uploaded or type strings
        if request.form.get('pathway_name'): ## input name='pathway_name'
            pathway_query = request.form.get('pathway_name')
            pathway_name = refineUrl(db_source, pathway_query)

            return redirect(url_for('getGeneList', pathway_name = pathway_name, db_source = db_source )) 
        
        elif 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            file.save(os.path.join('query_input', file.filename))
            file_prefix = file.filename.split('.')[0]

            return redirect(url_for('getManyGeneList', file_prefix = file_prefix, db_source = db_source))
                   
    return render_template('post_path_name.html')



@app.route('/results/multi_query/<db_source>/<file_prefix>')
def getManyGeneList(file_prefix, db_source):
    """
    for multi queries, using loop to get gene lists and save as dict format
    """
    out_file_list = []
    if not os.path.exists(os.path.join(os.getcwd(),'query_input')):
        os.makedirs(os.path.join(os.getcwd(),'query_input'))
    with open('query_input/{}.txt'.format(file_prefix), 'r') as fh:
      total_gene_list = {}
      _count = 0
      for pathway_query in fh:
        pathway_query = pathway_query.strip()
        _count += 1
        
        pathway_name = refineUrl(db_source, pathway_query)
        total_gene_list[pathway_query] = queryPathGenes(db_source, pathway_name)  
        ## save each genelist 
        out_name = saveOutput('query_output', total_gene_list[pathway_query], db_source, pathway_name)
        out_file_list.append(out_name)

    out_prefix = '{}_gene_lists'.format(db_source)
    if not os.path.exists(os.path.join(os.getcwd(),'query_output')):
        os.makedirs(os.path.join(os.getcwd(),'query_output'))

    saveZipOutput('query_output', out_prefix, out_file_list)
       
    return render_template('get_gene_list_multi.html', gene_list = json.dumps(total_gene_list, indent=4), pathway_name = pathway_name, out_prefix = out_prefix )
     

@app.route('/results/single_query/<db_source>/<pathway_name>')
def getGeneList(pathway_name, db_source):
    
    gene_list = queryPathGenes(db_source, pathway_name)
    if not os.path.exists(os.path.join(os.getcwd(),'query_output')):
        os.makedirs(os.path.join(os.getcwd(),'query_output'))
     

    if type(gene_list) == str or len(gene_list) == 0:
        return render_template('no_result.html', pathway_name = pathway_name)
    
    else:
        out_prefix = saveOutput('query_output', gene_list, db_source, pathway_name)
        return render_template('get_gene_list.html', gene_list = gene_list, pathway_name = pathway_name, out_prefix = out_prefix )
    

@app.route('/download/single_query/<out_type>/<out_prefix>')
def download(out_type, out_prefix):
    if out_type == 'download_txt':
        return send_from_directory('query_output','{}_gene_list.txt'.format(out_prefix), as_attachment=True)
    
    elif out_type == 'download_csv':
        return send_from_directory('query_output','{}_gene_list.csv'.format(out_prefix), as_attachment=True)


@app.route('/download/multi_query/<out_type>/<out_prefix>')
def downloadZip(out_type, out_prefix):
    if out_type == 'download_zip':
        return send_file( os.path.join('query_output','{}.zip'.format(out_prefix)), as_attachment=True, mimetype= 'zip')


if __name__ == '__main__':
    app.debug = True
    app.run()


## OK download into txt or json file, or copy OK
#### step1: test for send_from_directory function OK
#### step2: test for write variable into file OK
#### step3: direct to download app route and download OK
#### step4: download format > csv or text OK 
#### TODO as a reminder: don't forget to add function variable in the app route !!!

## OK allow multiple pathway input and separate the results -
#### TODO as a reminder: don't contain '/' string in variable for app route !! Harmonize db report error due to "mapk/GeneRIF+Biological+Term+Annotations"

## OK select database source (now finished: NCBI, KEGG, and Harmonize) 


## OK allow multiple input (maybe upload txt containing list of query pathway?)
## step1: create <form> with <input> type = file OK
## step2: upload and save into existing folders > set config ? OK 
#### TODO as reminder it's important to add attr enctype="multipart/form-data" in form element
## step3: distinguish input type and refine func (to a loop) OK 路由設定也很重要不能重複
#### TODO as reminder: if two route url struc is the same, it will misdirect to the wrong func
#### example: @app.route('/results/<db_source>/<pathway_name>')
#### and @app.route('/results/<db_source>/<file_prefix>')
## step4: download as separate files and zipped folder ? OK finally use zipfile package


## OK add css style or maybe practice the bootstrap ? 
#### bootstrap not work just add border simple css...

## OK jinja template success to reduce duplicate html 

## TODO print json format prettier by javascript
#### json can't receive flask variable ?

## TODO how to clean query_output / input folder regularly ?
### connect to SQL db ?
