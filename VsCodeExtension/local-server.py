from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)

#For drive model
drive_path = 'path-to-your-model'
device = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForCausalLM.from_pretrained(drive_path)
tokenizer = AutoTokenizer.from_pretrained(drive_path)

if device == "cuda":
    model = model.cuda()  # Move to GPU
else:
    model = model.cpu()   # Ensure it's on the CPU

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        print(data)
        prompt = data.get("input", "")

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        # suggestions = []
        # outputs = [model.generate(
        #     inputs["input_ids"],
        #     max_length=100,
        #     num_return_sequences=1,
        #     temperature=0.5,
        #     do_sample=True,
        #     top_p=0.9,
        #     pad_token_id=tokenizer.eos_token_id
        # ),
        # model.generate(
        #     inputs["input_ids"],
        #     max_length=100,
        #     num_return_sequences=1,
        #     temperature=0.6,
        #     top_k=100,
        #     do_sample=True,
        #     pad_token_id=tokenizer.eos_token_id
        # ),
        # model.generate(
        #     inputs["input_ids"],
        #     max_length=100,
        #     num_return_sequences=1,
        #     do_sample=True,
        #     top_k=100,
        #     temperature=0.8,
        #     pad_token_id=tokenizer.eos_token_id
        # )]
        # for output in outputs:
        #   for sequence in output:
        #     suggestions.append(tokenizer.decode(sequence, skip_special_tokens=True))

        # Generate multiple outputs manually
        suggestions = []
        for _ in range(3):  # Generate three suggestions
            output = model.generate(
                inputs.input_ids,
                max_length=len(prompt)+16,
                temperature=0.8,  # Control randomness
                top_k=50,         # Limit to top-k tokens
                do_sample=True,   # Enable sampling for diversity
            )
            decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
            formatted_output,_,_ = decoded_output[len(prompt):].rpartition('\n')
            suggestions.append(formatted_output)

        # Sort by length (as a proxy for "accuracy" or completion suitability)
        sorted_suggestions = sorted(set(suggestions), key=lambda x: len(x))  # Remove duplicates
        for suggestion in sorted_suggestions:
          print(suggestion)
        response = jsonify({"suggestions": sorted_suggestions})


        return response

    except Exception as e:
        print("Error during generation:", e)
        return jsonify({"error": str(e)}), 500

app.run(host='0.0.0.0', port=5004)
