# AI Model experiement

I am experimenting the [Python OpenAI demos project](https://github.com/Azure-Samples/python-openai-demos) in github_models.py file. 

## Python environment

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
## Dev
I use pydantic [Dotenv support](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support) to use the environment variables from the .env file. 