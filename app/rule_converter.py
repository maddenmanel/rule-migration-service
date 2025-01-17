from transformers import T5Tokenizer, T5ForConditionalGeneration
import os
import json

class RuleConverter:
    def __init__(self, model_dir: str = "./model", pretrained_model: str = "t5-small"):
        """
        初始化 T5 模型和分词器
        """
        self.model_dir = model_dir
        self.pretrained_model = pretrained_model
        self._load_model()

    def _load_model(self):
        """
        加载训练后的模型，如果不存在则加载预训练模型
        """
        if os.path.exists(self.model_dir):
            print("Loading fine-tuned model...")
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_dir)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_dir)
        else:
            print("Loading pre-trained model...")
            self.tokenizer = T5Tokenizer.from_pretrained(self.pretrained_model)
            self.model = T5ForConditionalGeneration.from_pretrained(self.pretrained_model)

    def reload_model(self):
        """
        手动重新加载模型
        """
        self._load_model()

    def convert_rule(self, input_rule: str) -> str:
        """
        使用 T5 模型将 XML 规则转换为 JSON
        """
        # 准备包含 XML 输入的提示
        prompt = f"Convert the following XML rule to standard JSON format:\n{input_rule}\nOutput JSON:"
        
        # 对输入进行分词
        inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
        
        # 使用模型生成输出
        outputs = self.model.generate(inputs, max_length=1024, num_beams=4, early_stopping=True)
        
        # 解码输出并返回 JSON 字符串
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 使用 json.loads() 来验证并格式化输出为标准 JSON
        try:
            json_output = json.loads(result)
            return json.dumps(json_output, indent=2)  # 格式化输出为漂亮的 JSON
        except json.JSONDecodeError:
            return f"Error: Unable to decode JSON: {result}"