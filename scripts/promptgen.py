import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import gradio as gr
from git import Repo
from git.remote import RemoteProgress

model_folder = ""
tokenizer = ""
model = ""
num_return_sequences =1
def modelcheck():
    global model_folder
    global tokenizer
    global model
    global num_return_sequences
    if os.path.exists(os.path.join("extensions", "Stylez", "distilgpt2-stable-diffusion-v2")):
        model_folder = os.path.join("extensions", "Stylez", "distilgpt2-stable-diffusion-v2")
        tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model = GPT2LMHeadModel.from_pretrained(model_folder)
        return True
    else:
        print("""No Model Found, Please run 'git clone https://huggingface.co/FredZhang7/distilgpt2-stable-diffusion-v2' to the extensions/Stylez folder""")
        return False

def generate(prompt,temperature,top_k,max_length,repitition_penalty,usecomma):
    model_found = modelcheck()
    if (model_found == True):
        input_ids = tokenizer(prompt, return_tensors='pt').input_ids
        if(usecomma == False):
            output = model.generate(input_ids, do_sample=True, temperature=temperature, top_k=top_k, max_length=max_length, num_return_sequences=num_return_sequences, repetition_penalty=repitition_penalty, penalty_alpha=0.6, no_repeat_ngram_size=1, early_stopping=False)
        else:
            output = model.generate(input_ids, do_sample=True, temperature=temperature, top_k=top_k, max_length=max_length, num_return_sequences=num_return_sequences, repetition_penalty=repitition_penalty, early_stopping=True)
        print('\nInput:\n' + 100 * '-')
        print('\033[96m' + prompt + '\033[0m')
        print('\nOutput:\n' + 100 * '-')
        for i in range(len(output)):
            output_decoded = (tokenizer.decode(output[i], skip_special_tokens=True))
            print('\033[92m' + tokenizer.decode(output[i], skip_special_tokens=True) + '\033[0m\n')
        return(output_decoded)
    else:
        gr.Warning("No Model Found. Check Command Console")
