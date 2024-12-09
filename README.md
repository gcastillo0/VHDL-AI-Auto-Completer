## DISCLAIMER
This is a college project is not intended to be sold or used for commercial purposes. Is a project done by me in one semester, it is not a finish ready for deployment project is more of a big proof of concept to confirm that this has potential. Feel free to use this is a non-commercial way, please give credits if u use it. This is not a project for new users if you don't know Python programming or a little about LLM it could be difficult to move around is not an easy project to deploy

## SUMMARY 

You can implement this project with two forms, first doing the fine-tuning yourself and second just deploying the extension

## PROJECT INSTALLATION FOR FINE-TUNING
### PREVIOUS WORK
I used Ubuntu 22.04 for other OS i can't assure it will work.
1. Get a HuggingFace account and an access token https://huggingface.co/
2. Get a Docker Hub account and an access token https://hub.docker.com/
3. Get a credentials file from Google Drive https://help.qlik.com/talend/en-US/components/8.0/google-drive/how-to-access-google-drive-using-client-secret-json-file-the
4. Get the token.pickle file using the savetoken.py script, you might need to install libraries:
```bash
    pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```
Steps 3 and 4 are to be able to download your fine-tuned-model to google drive if you are using any other storage system feel free to change it

5. Get the vhdl_dataset file -> https://drive.google.com/file/d/1FYSe6CwuLMVAR4zJKzh1l3nzmKHqHyhl/view?usp=sharing
6. Modify train2.py script and add in the token variable (line 11) your HUGGING FACE token.
7. Install Docker in your computer (You may want to add your user to the docker group, otherwise you might need to use sudo) 
8. Now we are ready to build. Make sure that dockerfile, train2.py, token.pickle are in the same folder you run this commands also vhdl_dataset.json has to be in a subfolder named dataset (If you now how to use docker feel free to modify the docker file):
```bash
    docker login -u <your username> (It will prompt you for a password use the DOCKER TOKEN)
    docker build -t <image name>:<tag> .
    docker tag <image name>:<tag> <docker username>/<image name>:<tag>
    docker push <docker username>/<image name>:<tag>
``` 
Now we have our docker uploaded and ready to deploy.(Recommended tag: latest). You can test it or run it on your computer if you have the resources:
```bash
    docker run v $(pwd):/workdir <image name>
```
7-Bis. If you have the resources in your computer and don't want to use docker just install the libraries of the docker file in your computer and run train2.py in your computer

### FINE TUNING

1. Create an account on vast.ai
2. Go to templates -> Create New template
    Image Path/Tag -> <docker username>/<image name>:<tag>
    Docker Options ->  -v $(pwd):/workdir <image name>
    LaunchMode -> Run interactive Shell Server (Use direct ssh connection)
    Disk Space -> Depends on the model you are using, for the one I used I will say at least 64 GB recommended ~100 GB.
3. Go to instances select one GPU and create the instance (For the one I used with one RTX4090 I had enough)
4. Once the instance is up connect through SSH -> https://vast.ai/docs/instance-setup/ssh
5. Go to ../workdir and run train2.py
6. Wait until the training is complete (it may take > 20 hours).
7. Once training is done run drive_utils.py and you will have your model uploaded to drive

If you get the error of not enough space to allocate you probably need to get more or bigger GPUs

## VSCODE EXTENSION DEPLOYMENT

Right now the VSCODE extension can only use a Cloud server. The Local Server is needs more but you can try to make it work.

### LOCAL SERVER -- (HARD)(NOT RECOMMENDED)
1. Create a vscode extension using this tutorial https://code.visualstudio.com/api/get-started/your-first-extension
2. Add the files extension.ts and languageModelServide.ts to your src folder and also add the local-server folder to it 
3. Go to src/extension.ts and uncomment line 45
4. You will need to create a python env and add the path to the line 11 of extension.ts and download the local-server.py file and add the path to your model in it(line 8)
5. Go to languageModelService.ts and change the url in line 9 for your loopback address (probably 127.0.0.1) and port 5004-> https://127.0.01:5004/generate
6. Compile the extension in the command line with 
```bash
    npm run compile
```
6. Run the extension and try it (right now it will be active in any plain text file).

### CLOUD SERVER -- (EASY)
1. Go to Google Colab and upload the notebook AIServer.ipynb
2. Change the drive path in the last block to the path of your model in google drive (alternatively you can just upload the model manually to google colab).
3. Create a vscode extension using this tutorial https://code.visualstudio.com/api/get-started/your-first-extension
4. Add the files extension.ts and languageModelServide.ts to your src folder. 
    
5. Go to languagueModelService.ts line 9 and change the url to the provided by Ngrok something like this:
https://7756-34-125-148-182.ngrok-free.app (be sure to add /generate after the url)
6. Compile the extension in the command line with 
```bash
    npm run compile
```

7. Run the extension and try it (right now it will be active in any plain text file).

## My FINE-TUNED-MODEL URL
(If you just want to try the extension you need this for colab)
https://drive.google.com/drive/folders/1WQpmYLVVL65QcnFoxAlSNOJ5WtZYy6zj?usp=sharing
## Cite This Repository

If you use this repository in your research or projects, please cite it as:

```bibtex
@misc{gcastillo2024vhdl,
  author       = {Gonzalo Castillo},
  title        = {VHDL-AI-Auto-Completer: A tool for AI-assisted VHDL code completion},
  year         = {2024},
  howpublished = {\url{https://github.com/gcastillo0/VHDL-AI-Auto-Completer/tree/main}},
  note         = {GitHub repository},
  url          = {https://github.com/gcastillo0/VHDL-AI-Auto-Completer/tree/main}
}
