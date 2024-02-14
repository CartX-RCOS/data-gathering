from transformers import GPTNeoForCausalLM, GPT2Tokenizer

import json

# Load model and tokenizer
model_name = "EleutherAI/gpt-neo-2.7B"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPTNeoForCausalLM.from_pretrained(model_name)

def getGPTAnswer(input_text):
   input_ids = tokenizer.encode(input_text, return_tensors="pt")

   # Generate text
   output = model.generate(input_ids, max_length=100, num_return_sequences=1)

   # Decode and print output
   generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
   return generated_text


# data = ""
# with open("./response_data.json", 'r') as file:
#    data = json.load(file)

# data_string = json.dumps(data)

# inputText = "Parse the following string to make it a cleaner format for name. Return just the parsed string. For example if I give you crispy_appples then you should return Crispy Apples: advil-liqui-gels-200-mg-ibuprofen-capsules"
inputText = "What is 5 + 5"

# print(inputText)

# Prepare input
print("Starting GPT")
print(getGPTAnswer(inputText))

