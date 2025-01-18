from transformers import T5Tokenizer, T5ForConditionalGeneration
import os
import json
import torch

class RuleConverter:
    def __init__(self, model_dir: str = "./model", pretrained_model: str = "t5-large"):
        """
        Initialize the RuleConverter with the model directory and the pre-trained model name.
        """
        self.model_dir = model_dir
        self.pretrained_model = pretrained_model
        self._load_model()

    def _load_model(self):
        """
        Load the pre-trained or fine-tuned T5 model.
        """
        # if os.path.exists(self.model_dir):
        #     print("Loading fine-tuned model...")
        #     self.tokenizer = T5Tokenizer.from_pretrained(self.model_dir)
        #     self.model = T5ForConditionalGeneration.from_pretrained(self.model_dir)
        # else:
        print("Loading pre-trained model...")
        self.tokenizer = T5Tokenizer.from_pretrained(self.pretrained_model)
        self.model = T5ForConditionalGeneration.from_pretrained(self.pretrained_model)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = self.model.to(device)

    def reload_model(self):
        """
        Manually reload the model after training.
        """
        self._load_model()
    
    def convert_rule(self, xml_rule: str) -> str:
        """
        Convert an XML rule to JSON format using the pre-trained model.
        """
        # Prepare the prompt with the example XML to JSON conversion.
        prompt = f"""
        Convert the following XML rule into a JSON format. Output the JSON representation.

        Example:
        XML:
        <Rule>
            <Name>Example Rule</Name>
            <Condition field="field1" operator=">" value="50" />
            <Action field="field2" value="Approve" />
        </Rule>
        JSON:
        {{
            "Rule": {{
                "Name": "Example Rule",
                "Condition": {{
                    "field": "field1",
                    "operator": ">",
                    "value": "50"
                }},
                "Action": {{
                    "field": "field2",
                    "value": "Approve"
                }}
            }}
        }}

        Now, convert the following XML rule:
        {xml_rule}
        """
        print("The convert XML is \n" + prompt)

        # Use the model to get the result
        answer = self.answer_question(prompt)

        print("The answer result is \n" + answer)
        
        return answer

    def answer_question(self, question: str) -> str:
        """
        Use the pre-trained T5 model to answer a question in a chatbot-like manner.
        This method returns the raw output from the T5 model based on the question.
        """
        # Tokenizing the input prompt
        inputs = self.tokenizer.encode(question, return_tensors="pt", max_length=1024, truncation=True)

        # Generating the model's output
        outputs = self.model.generate(inputs, max_length=1024, num_beams=4, early_stopping=True)

        # Decoding the output to get a human-readable string
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return result 