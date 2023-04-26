import pandas as pd
import gradio as gr
from pymed import PubMed
from Bio import Entrez

def search_pubmed_with_gradio(search_term, max_results, include_pubmed_id, include_title, include_abstract):
    pubmed = PubMed(tool="MyTool", email="drishabh521@gmail.com")
    results = pubmed.query(search_term, max_results=max_results)
    article_list = []
    for article in results:
        article_dict = article.toDict()
        if include_pubmed_id:
            pubmed_id = article_dict['pubmed_id'].partition('\n')[0]
        else:
            pubmed_id = ""
        if include_title:
            title = article_dict['title']
        else:
            title = ""
        if include_abstract:
            abstract = article_dict['abstract']
        else:
            abstract = ""
        article_list.append({'pubmed_id': pubmed_id, 'title': title, 'abstract': abstract})
    df = pd.DataFrame(article_list)
    return df

interface = gr.Interface(search_pubmed_with_gradio,
                         [gr.inputs.Textbox(label="Search Term"),
                          gr.inputs.Slider(minimum=1, maximum=10000, default=100, label="Max Results"),
                          gr.inputs.Checkbox("pubmed_id", label="Pubmed ID"),
                          gr.inputs.Checkbox("title", label="Title"),
                          gr.inputs.Checkbox("abstract", label="Abstract")],
                         "dataframe",
                         title="PubMed Search",
                         description="Enter a keyword or more than a keyword to search in PubMed database")
                         
if __name__ == "__main__":
    interface.launch(share=True)