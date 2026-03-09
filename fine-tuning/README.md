## Fine-tuning Qwen-3 model

I adapted and used the Jupyter notebook files from Unsloth AI (Credit to Unsloth AI).

### Model Selection 
My plan switched from Llama-3.2/Gemma-3 to Qwen-3. While I initially considered them for my project, their acceptable use policies include specific restrictions on financial services. To avoid any potential licensing ambiguity, even for a non-commercial project, I've decided to use Qwen instead.

**Note** 
The Jupyter notebook file is copied from unsloth tutorial. 

The fine-tuned Qwen3 model is uploaded to [Huggingface hub](https://huggingface.co/Battogtokh/Qwen3-4B-Instruct-unsloth-FinAdvisor-gguf). 

### Installation

The python environment is created using 'uv' and the required packages are installed. Please refer to the Jupyter notebooks for details. 

### Running the model

I used Ollama to use the model. 
</br>
First, the Modelfile is created. </br>
Second, the model is created from the Modelfile instruction for Ollama. 

```shell
ollama create qwen3-unsloth-finadvisor -f ./Modelfile-qwen3
```

Third, model is tested to run
```shell
ollama run qwen3-unsloth-finadvisor:latest
```
