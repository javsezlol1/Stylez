import os
import datetime
import urllib.parse
import gradio as gr
from PIL import Image
from modules import scripts
from pathlib import Path
from typing import List, Tuple
import json
import csv
from json import loads
stylespath = ""

refresh_symbol = '\U0001f504'  # 🔄
close_symbol = '\U0000274C'  # ❌
save_symbol = '\U0001F4BE' #💾
delete_style = '\U0001F5D1' #🗑️
clear_symbol = '\U0001F9F9' #🧹


card_size_value = 0
card_size_min = 0
card_size_max = 0
favourites = []

def save_card_def(value):
    global card_size_value
    save_settings("card_size",value)
    card_size_value = value

config_json = os.path.join(os.path.dirname(__file__), "config.json")

def reload_favourites():
    with open(config_json, "r") as json_file:
        data = json.load(json_file)
        global favourites
        favourites = data["favourites"]

with open(config_json, "r") as json_file:
    data = json.load(json_file)
    card_size_value = data["card_size"]
    card_size_min = data["card_size_min"]
    card_size_max = data["card_size_max"]
    autoconvert = data["autoconvert"]
    favourites = data["favourites"]

def save_settings(setting,value):
    with open(config_json, "r") as json_file:
        data = json.load(json_file)
    data[setting] = value
    with open(config_json, "w") as json_file:
        json.dump(data, json_file, indent=4)

def img_to_thumbnail(img):
    return gr.update(value=img)

def create_json_objects_from_csv(csv_file):
    json_objects = []
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get('name', None)
            prompt = row.get('prompt', None)
            negative_prompt = row.get('negative_prompt', None)
            if name is None or prompt is None or negative_prompt is None:
                print("Warning: Skipping row with missing values.")
                continue
            json_data = {
                "name": name,
                "description": "converted from csv",
                "preview": f"{name}.jpg",
                "prompt": prompt,
                "negative": negative_prompt,
            }
            json_objects.append(json_data)
    return json_objects

def save_json_objects(json_objects):
    if not json_objects:
        print("Warning: No JSON objects to save.")
        return

    styles_dir = os.path.join("extensions", "Stylez", "styles")
    csv_conversion_dir = os.path.join(styles_dir, "CSVConversion")
    os.makedirs(csv_conversion_dir, exist_ok=True)

    for json_obj in json_objects:
        json_file_path = os.path.join(csv_conversion_dir, f"{json_obj['name']}.json")
        with open(json_file_path, 'w') as jsonfile:
            json.dump(json_obj, jsonfile, indent=4)
        image_path = os.path.join(csv_conversion_dir, f"{json_obj['name']}.jpg")
        img = Image.open(os.path.join("extensions", "Stylez", "nopreview.jpg"))
        img.save(image_path)
if (autoconvert == True):
    csv_file_path = os.path.join(os.getcwd(), "styles.csv")
    if os.path.exists(csv_file_path):
        json_objects = create_json_objects_from_csv(csv_file_path)
        save_json_objects(json_objects)
    else:
        save_settings("autoconvert", False)

def generate_html_code():
    reload_favourites()
    style = None
    style_html = ""
    categories_list = ["All","Favourites"]
    save_categories_list =[]
    styles_dir = os.path.join("extensions", "Stylez", "styles")
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S.%f')
    formatted_time = formatted_time.replace(":", "")
    formatted_time = formatted_time.replace(".", "")
    try:
        for root, dirs, _ in os.walk(styles_dir):
            for directory in dirs:
                subfolder_name = os.path.basename(os.path.join(root, directory))
                if subfolder_name.lower() not in categories_list:
                    categories_list.append(subfolder_name)
                if subfolder_name.lower() not in save_categories_list:
                    save_categories_list.append(subfolder_name)    
        for root, _, files in os.walk(styles_dir):
            for filename in files:
                if filename.endswith(".json"):
                    json_file_path = os.path.join(root, filename)
                    subfolder_name = os.path.basename(root)
                    with open(json_file_path, "r", encoding="utf-8") as f:
                        try:
                            style = json.load(f)
                            title = style.get("name", "")
                            preview_image = style.get("preview", "")
                            description = style.get("description", "")
                            img = os.path.join(os.path.dirname(json_file_path), preview_image)
                            img = os.path.abspath(img)
                            prompt = style.get("prompt", "")
                            prompt_negative = style.get("negative", "")
                            imghack = img.replace("\\", "/")
                            json_file_path = json_file_path.replace("\\", "/")
                            encoded_filename = urllib.parse.quote(filename, safe="")
                            titlelower = str(title).lower()
                            color = ""
                            stylefavname =subfolder_name + "/" + filename
                            if (stylefavname in favourites):
                                color = "#EBD617"
                            else:
                                color = "#ffffff"
                            style_html += f"""
                            <div class="style_card" data-category='{subfolder_name}' data-title='{titlelower}' style="height:{card_size_value}px;">
                                <img class="styles_thumbnail" src="{"file=" + img +"?timestamp"+ formatted_time}" alt="{title} Preview">
                                <div class="EditStyleJson">
                                    <button onclick="editStyle('{title}','{imghack}','{description}','{prompt}','{prompt_negative}','{subfolder_name}','{encoded_filename}')">🖉</button>
                                </div>
                                <div class="favouriteStyleJson">
                                    <button class="favouriteStyleBtn" style="color:{color};" onclick="addFavourite('{subfolder_name}','{encoded_filename}', this)">★</button>
                                </div>
                                    <div onclick="applyStyle('{prompt}','{prompt_negative}')" onmouseenter="event.stopPropagation(); hoverPreviewStyle('{prompt}','{prompt_negative}')" onmouseleave="hoverPreviewStyleOut()" class="styles_overlay"></div>
                                    <div class="styles_title">{title}</div>
                                    <p class="styles_description">{description}</p>
                                </img>
                            </div>
                            """
                        except json.JSONDecodeError:
                            print(f"Error parsing JSON in file: {filename}")
                        except KeyError as e:
                            print(f"KeyError: {e} in file: {filename}")
    except FileNotFoundError:
        print("Directory '/models/styles' not found.")
    return style_html, categories_list, save_categories_list

def refresh_styles(cat):
    if cat is None or len(cat) == 0 or cat  == "[]" :
        cat = None
    newhtml = generate_html_code()
    newhtml_sendback = newhtml[0]
    newcat_sendback = newhtml[1]
    newfilecat_sendback = newhtml[2]
    return newhtml_sendback,gr.update(choices=newcat_sendback),gr.update(value="All"),gr.update(choices=newfilecat_sendback)

def save_style(title, img, description, prompt, prompt_negative, filename, save_folder):
    if save_folder and filename:
        if img is None or img == "":
            img = os.path.join("extensions", "Stylez", "nopreview.jpg")
        img = img.resize((200, 200))
        save_folder_path = os.path.join("extensions", "Stylez", "styles", save_folder)
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
        json_data = {
            "name": title,
            "description": description,
            "preview": filename + ".jpg",
            "prompt": prompt,
            "negative": prompt_negative,
        }
        json_file_path = os.path.join(save_folder_path, filename + ".json")
        with open(json_file_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        img_path = os.path.join(save_folder_path, filename + ".jpg")
        img.save(img_path)
        msg = f"""File Saved to '{save_folder}'"""
        info(msg)
    else:
        msg = """Please provide a valid save folder and Filename"""
        warning(msg)
    return filename_check(save_folder,filename)

def info(message):
    gr.Info(message)

def warning(message):
    gr.Warning(message)
    
def tempfolderbox(dropdown):
    return gr.update(value=dropdown)

def filename_check(folder,filename):
    if filename is None or len(filename) == 0 :
        warning = """<p id="style_filename_check" style="color:red;">please add a file name</p>"""
    else:
        save_folder_path = os.path.join("extensions", "Stylez", "styles", folder)
        json_file_path = os.path.join(save_folder_path, filename + ".json")
        if os.path.exists(json_file_path):
            warning = f"""<p id="style_filename_check" style="color:red;">Overwrite!! File Already Exists In '{folder}'</p>"""
        else:
            warning = """<p id="style_filename_check" style="color:green;">Filename Is Valid</p>"""
    return gr.update(value=warning)

def clear_style():
    previewimage = os.path.join("extensions", "Stylez", "nopreview.jpg")
    return gr.update(value=None),gr.update(value=previewimage),gr.update(value=None),gr.update(value=None),gr.update(value=None),gr.update(value=None),gr.update(value=None)

def deletestyle(folder, filename):
    base_path = os.path.join("extensions", "Stylez", "styles", folder)
    json_file_path = os.path.join(base_path, filename + ".json")
    jpg_file_path = os.path.join(base_path, filename + ".jpg")


    if os.path.exists(json_file_path):
        os.remove(json_file_path)
        warning(f"""Stlye "{filename}" deleted!! """)
        if os.path.exists(jpg_file_path):
            os.remove(jpg_file_path)
        else:
            warning(f"Error: {jpg_file_path} not found.")
    else:
        warning(f"Error: {json_file_path} not found.")

def addToFavourite(style):
 global favourites
 if (style not in favourites):
     favourites.append(style)
     save_settings("favourites",favourites)
     info("style added to favourites")

def removeFavourite(style):
 global favourites
 if (style in favourites):
     favourites.remove(style)
     save_settings("favourites",favourites)
     info("style removed from favourites")

def LoadCss():
    cssfile = """
    #Stylez { position: absolute;top: 33%;background: #0b0f19;width: 50%;z-index: 1000;right: 0;height: fit-content;display: none;}
    #style_tags_column{min-width: unset !important;max-width:8vw; background-color: #1f2937; padding: 5px; min-width: min(0px,100%) !important; border-style: solid; border-left: #e76715;}
    #style_cards_column{height: 40vh; min-width: unset !important;width: 26vw;overflow: auto;padding-top: 10px;padding-left: 5px;}
    .style_card{ display: flex; flex-direction: column; align-items: center; justify-content: center; width:auto;float: left; contain: content;margin-top: unset !important; margin: 5px;}
    .styles_overlay{position: absolute;width: 100%; ;height:100% ;background-color: rgba(46, 46, 46, 0.642);opacity: 0; transition:opacity 0.5s ease;}
    .style_card:hover .styles_overlay{ opacity: 1;}
    .style_card:hover {box-shadow: 0px 0px 12px 1px #fff !important;}
    .styles_thumbnail{height:inherit !important; width:auto; object-fit: contain;}
    .styles_title{pointer-events: none;position: absolute;top: 0;left: 0;background:#00000094; padding: 2px;}
    .styles_description{pointer-events: none;position: fixed;text-align: center; opacity: 0; transition:opacity 0.5s ease;}
    .style_card:hover .styles_description{ opacity: 1; }
    #txt2img_styles_popout > div{left: 0.3vw;flex-flow: column;}
    #img2img_styles_popout > div{left: 0.3vw;flex-flow: column;}
    #txt2img_styles_popout {border-left-style: solid;border-left-width: 2px}
    #img2img_styles_popout {border-left-style: solid;border-left-width: 2px}
    #style_refresh{min-width:unset !important;max-width: 2vw;align-self: baseline;}
    #style_tags > label > div{margin-top: 10px;}
    .EditStyleJson{z-index: 9999;position: absolute;background-color: #00000094 !important;right: 0;bottom: 0; padding: 5px !important;}
    .favouriteStyleJson{z-index: 9999;position: absolute;left: 0;bottom: 0; padding: 5px !important;}
    #style_command_btn_row{width: fit-content !important;align-self: end;}
    #style_filename_check_container{top:-20px;}
    #style_cards_Pref{flex-grow: 0; max-height: fit-content; bottom: 0;}
    #gradio_style_savefolder_row{top: -35px;position: relative !important;}
    .styles_checkbox{max-width: fit-content;min-width: unset !important;}
    .styles_dropdown > label > div{background-color: #00000042 !important;}
    .styles_checkbox > label > input{box-shadow: none !important;}
    #previewPromptPos > label > textarea{ max-height:63px ;}
    #previewPromptNeg > label > textarea{ max-height:63px ;}
    .favouriteStyleBtn{font-size: 30px !important;position: absolute;-webkit-text-stroke-width: 1px; -webkit-text-stroke-color: black; bottom: -10px !important;left: 0px !important;}"""

    return cssfile

class Stylez(scripts.Script):
    generate_styles_and_tags = generate_html_code()
    css = LoadCss()
    def __init__(self) -> None:
        super().__init__()
    def title(self):
        return "Stylez"
    def ui(self, is_img2img):
        gr.HTML(f"""<style>{self.css}<\style>">""")
        with gr.Tabs(elem_id = "Stylez"):
            with gr.TabItem(label="Style Libary",elem_id="styles_libary"):
                with gr.Column():
                    with gr.Row(elem_id="style_search_search"):
                        Style_Search = gr.Textbox('', show_label=False, elem_id="style_search", placeholder="Search...", elem_classes="textbox", lines=1)
                        refresh_button = gr.Button(refresh_symbol, label="Refresh", elem_id="style_refresh", elem_classes="tool", lines=1)
                    with gr.Row(elem_id="style_cards_row"):
                        with gr.Column(elem_id="style_tags_column"):
                            category_dropdown = gr.Dropdown(label="Catagory", choices=self.generate_styles_and_tags[1], value="All", lines=1, elem_id="style_Catagory", elem_classes="dropdown styles_dropdown")
                            with gr.Column(elem_id="style_cards_Pref"):
                                card_size_slider = gr.Slider(value=card_size_value,minimum=card_size_min,maximum=card_size_max,label="Size:", elem_id="card_thumb_size")
                                gr.Checkbox(label="Apply Prompt",value=True, default=True, elem_id="styles_apply_prompt", elem_classes="styles_checkbox checkbox", lines=1)
                                gr.Checkbox(label="Apply Negative",value=True, default=True, elem_id="styles_apply_neg", elem_classes="styles_checkbox checkbox", lines=1)
                        with gr.Column(elem_id="style_cards_column"):
                            with gr.Row():
                                Styles_html=gr.HTML(self.generate_styles_and_tags[0])
                    with gr.Row(elem_id="stylesPreviewRow"):
                        gr.Text(elem_id="previewPromptPos",interactive=False,label="Positive:",lines=2)
                        gr.Text(elem_id="previewPromptNeg",interactive=False,label="Negative:",lines=2)
                    with gr.Row(elem_id="stylesPreviewRow"):
                        favourite_temp = gr.Text(elem_id="favouriteTempTxt",interactive=False,label="Positive:",lines=2,visible=False)
                        add_favourite_btn = gr.Button(elem_id="stylezAddFavourite",visible=False)
                        remove_favourite_btn = gr.Button(elem_id="stylezRemoveFavourite",visible=False)
            with gr.TabItem(label="Style Editor",elem_id="styles_editor"):
                with gr.Row():
                    with gr.Column():
                        style_title_txt = gr.Textbox(label="Title:", lines=1,placeholder="Title goes here",elem_id="style_title_txt")
                        style_description_txt = gr.Textbox(label="Description:", lines=1,placeholder="Description goes here", elem_id="style_description_txt")
                        style_prompt_txt = gr.Textbox(label="Prompt:", lines=2,placeholder="Prompt goes here", elem_id="style_prompt_txt")
                        style_negative_txt = gr.Textbox(label="Negative:", lines=2,placeholder="Negative goes here", elem_id="style_negative_txt")
                    with gr.Column():
                        with gr.Row():
                            style_save_btn = gr.Button(save_symbol,label="Save Style", lines=1,elem_classes="tool", elem_id="style_save_btn")
                            style_clear_btn = gr.Button(clear_symbol,label="Clear", lines=1,elem_classes="tool" ,elem_id="style_clear_btn")
                            style_delete_btn = gr.Button(delete_style,label="Delete Style", lines=1,elem_classes="tool", elem_id="style_delete_btn")
                        thumbnailbox = gr.Image(value=None,label="Thumbnail:",elem_id="style_thumbnailbox",elem_classes="image",interactive=True,type='pil')
                        style_img_url_txt = gr.Text(label=None,lines=1,placeholder="Invisible textbox", elem_id="style_img_url_txt",visible=False)
                with gr.Row():
                    style_grab_current_btn = gr.Button("Grab Prompts",label="Grab Current", lines=1, elem_id="style_grab_current_btn")
                    style_lastgen_btn =gr.Button("Grab Last Generated Image",label="Save Style", lines=1,elem_id="style_lastgen_btn")
                with gr.Row():
                    with gr.Column():
                            style_filename_txt = gr.Textbox(label="Filename Name:", lines=1,placeholder="Filename", elem_id="style_filename_txt")
                            style_filname_check = gr.HTML("""<p id="style_filename_check" style="color:red;">Please Add a Filename</p>""",elem_id="style_filename_check_container")
                    with gr.Column():
                        with gr.Row():
                            style_savefolder_refrsh_btn = gr.Button(refresh_symbol, label="Refresh", lines=1,elem_classes="tool")
                            style_savefolder_txt = gr.Dropdown(label="Save Folder (Type To Create A New Folder):", value="Styles", lines=1, choices=self.generate_styles_and_tags[2], elem_id="style_savefolder_txt", elem_classes="dropdown",allow_custom_value=True)
                            style_savefolder_temp = gr.Textbox(label="Save Folder:",value="Styles", lines=1, elem_id="style_savefolder_temp",visible=False)

        refresh_button.click(fn=refresh_styles,inputs=[category_dropdown], outputs=[Styles_html,category_dropdown,category_dropdown,style_savefolder_txt])
        card_size_slider.release(fn=save_card_def,inputs=[card_size_slider])
        card_size_slider.change(fn=None,inputs=[card_size_slider],_js="cardSizeChange")
        category_dropdown.change(fn=None,_js="filterSearch",inputs=[category_dropdown,Style_Search])
        Style_Search.change(fn=None,_js="filterSearch",inputs=[category_dropdown,Style_Search])
        style_img_url_txt.change(fn=img_to_thumbnail, inputs=[style_img_url_txt],outputs=[thumbnailbox])
        style_grab_current_btn.click(fn=None,_js='grabCurrentSettings')
        style_lastgen_btn.click(fn=None,_js='grabLastGeneratedimage')
        style_savefolder_refrsh_btn.click(fn=refresh_styles,inputs=[category_dropdown], outputs=[Styles_html,category_dropdown,category_dropdown,style_savefolder_txt])
        style_save_btn.click(fn=save_style, inputs=[style_title_txt, thumbnailbox, style_description_txt,style_prompt_txt, style_negative_txt, style_filename_txt, style_savefolder_temp], outputs=[style_filname_check])
        style_filename_txt.change(fn=filename_check, inputs=[style_savefolder_temp,style_filename_txt], outputs=[style_filname_check])
        style_savefolder_txt.change(fn=tempfolderbox, inputs=[style_savefolder_txt], outputs=[style_savefolder_temp])
        style_savefolder_temp.change(fn=filename_check, inputs=[style_savefolder_temp,style_filename_txt], outputs=[style_filname_check])
        style_clear_btn.click(fn=clear_style, outputs=[style_title_txt,style_img_url_txt,thumbnailbox,style_description_txt,style_prompt_txt,style_negative_txt,style_filename_txt])
        style_delete_btn.click(fn=deletestyle, inputs=[style_savefolder_temp,style_filename_txt])
        add_favourite_btn.click(fn=addToFavourite, inputs=[favourite_temp])
        remove_favourite_btn.click(fn=removeFavourite, inputs=[favourite_temp])

