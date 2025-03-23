# functions.py
import zipfile
import os
import scanpy as sc
import matplotlib.pyplot as plt
import tempfile

def process_zip_and_umap(zip_path):
    extract_dir = "/Users/azratuncay/Desktop/IEEE/shiny erros & fixes/IEEE_DATASET_H3AD/IEEE_H5AD.zip"
    os.makedirs(extract_dir, exist_ok=True)
    h5ad_file = None

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        for filename in os.listdir(extract_dir):
            if filename.endswith(".h5ad"):
                h5ad_file = os.path.join(extract_dir, filename)
                break

        if not h5ad_file:
            raise FileNotFoundError("No .h5ad file found in the ZIP archive.")

        adata = sc.read_h5ad(h5ad_file)
        sc.pp.calculate_qc_metrics(adata, inplace=True)
        adata.raw = adata
        sc.pp.filter_cells(adata, min_genes=200, max_genes=8000)
        sc.pp.filter_genes(adata, min_cells=3)
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)
        sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
        adata = adata[:, adata.var.highly_variable]
        sc.pp.scale(adata, max_value=10)
        sc.pp.neighbors(adata, n_neighbors=15, n_pcs=50)
        sc.tl.umap(adata)
        sc.pl.umap(adata, color="Cell type", show=False, palette=sc.pl.palettes.vega_20_scanpy)

        temp_image = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        plt.savefig(temp_image.name, bbox_inches="tight")
        plt.close()
        return temp_image.name

    except Exception as e:
        print(f"Error processing ZIP/UMAP: {e}")
        return None