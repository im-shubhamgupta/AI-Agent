

## Install Ollama (AI Model)

    https://ollama.com/download ( Qwen 3)


    - Ollama serve  ## run the ollama model

    - ollama list #check your model

    - ollama pull qwen3:4b

    - nohup ollama serve > ~/.ollama/ollama.log 2>&1 &

    #debugging:--

    - curl http://localhost:11434/

    - curl http://localhost:11434/api/tags


# Run you python

  Make sure ollma server is running

  python3 assistant.py

  ollama pull phi4-mini







