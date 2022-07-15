import torch
#Wfrom caffe2.quantization.server.observer_test import net as nn
from simplet5 import SimpleT5
from flask import Flask, render_template, request

app = Flask(__name__)
import pickle

#model = pickle.load(open('T5model.pkl', 'rb'))
model = torch.load('T5model.pkl', map_location=torch.device('cpu'),pickle_module=pickle)
#my_model = nn.load_state_dict(torch.load('T5model.pkl', map_location=torch.device('cpu')))
#model = torch.load('T5model.pkl',map_location ='cpu')

@app.route('/')
def home_page():
    return render_template('index.html', button_name="SUBMIT")


@app.route('/', methods=['GET', 'POST'])
def data():
    if request.method == "POST":
        ARTICLE = request.form['text']
        length = len(ARTICLE)
        max_chunk = length // 6
        ARTICLE = ARTICLE.replace('.', '.<eos>')
        ARTICLE = ARTICLE.replace('?', '?<eos>')
        ARTICLE = ARTICLE.replace('!', '!<eos>')
        sentences = ARTICLE.split('<eos>')
        current_chunk = 0
        chunks = []
        for sentence in sentences:
            if len(chunks) == current_chunk + 1:
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                print(current_chunk)
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])

        str= ""
        for i in range(len(chunks)):
            if (i != 0):
                chunks[i] = "summarize:" + chunks[i]

            str = str + chunks[i]

        return render_template('index.html', Output=str, button_name="REDO")

app.run()
