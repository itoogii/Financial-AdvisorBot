# AI Model experiement

I am experimenting the [Python OpenAI demos project](https://github.com/Azure-Samples/python-openai-demos) in github_models.py file. 

## Github Models
The experiment code is using the code compatible with OpenAI API. 
GitHub model inference URL: https://models.github.ai/inference
### Python environment on my laptop

I use pyenv to manage my python 3.12.12 environment. 
```shell
pyenv install 3.12.12 
pyenv virtualenv 3.12.12 demo-py3.12
pyenv activate demo-py3.12
```  

The requirements.txt file will be used for installing the required packages in the new environment. 

```shell
pip install -U pip
pip install -r requirements.txt
```

## Ollama Model
The WSL provides full transparent GPU access for the Linux environment. 
1. Installed WSL Ubuntu-24.04 on Windows
2. Installed Docker Desktop
3. Ran the docker command
```shell
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name locallama ollama/ollama
```
4. Ran the docker command to run the model
```shell
docker exec -it locallama ollama run llama3.1:8b
```
### .env 
I used the OpenAI API compatible API URL from Ollama.
[Ollama API ref, OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility#simple-v1/chat/completions-example)

```
API_HOST=ollama
OLLAMA_ENDPOINT=http://localhost:11434/v1/
OLLAMA_MODEL=llama3.1:8b
```

### Python environment on subsystem Linux on Windows PC
I used the uv in the WSL. 
The .venv is created for local environment
```shell
uv python install 3.12
uv venv --python 3.12
# assuming already in the code directory
source ./.venv/bin/activate
uv pip install -r ./requirements.txt
python ./1.1_multi_turn_chat_stream.py
```

## Dev
I use pydantic [Dotenv support](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support) to use the environment variables from the .env file. 

