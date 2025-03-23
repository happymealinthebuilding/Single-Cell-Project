
from shiny import App, ui, render, input, session
import os
from functions import process_zip_and_umap

def app_ui():
    return ui.page_fluid(
        ui.h1("UMAP Explorer", style="color: #336699;"),
        ui.p("Upload a ZIP file containing an .h5ad dataset for UMAP visualization."),
        ui.input_file("file_upload", "Select ZIP File", accept=".zip"),
        ui.output_text("status_message"),
        ui.output_image("umap_plot")
    )

def server(input, output, session):
    @render.text
    def status_message():
        if not input.file_upload():
            return "Please upload a ZIP file."
        try:
            image_path = process_zip_and_umap(input.file_upload()[0]["datapath"])
            if image_path:
                return "UMAP visualization generated."
            else:
                return "Failed to generate UMAP visualization."
        except Exception as e:
            return f"Error: {e}"

    @render.image
    def umap_plot():
        if not input.file_upload():
            return None
        try:
            image_path = process_zip_and_umap(input.file_upload()[0]["datapath"])
            if image_path:
                return {"src": image_path, "alt": "UMAP Plot"}
            else:
                return None
        except Exception as e:
            print(f"Image generation error: {e}")
            return None

    @session.on_ended
    def cleanup_data():
        data_dir = "./extracted_data"
        try:
            if os.path.exists(data_dir):
                for filename in os.listdir(data_dir):
                    filepath = os.path.join(data_dir, filename)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                os.rmdir(data_dir)
        except Exception as e:
            print(f"Cleanup error: {e}")

app = App(app_ui(), server)