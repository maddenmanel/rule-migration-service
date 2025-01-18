import unittest
from unittest.mock import patch

from app.rule_converter import RuleConverter

class TestRuleConverter(unittest.TestCase):
    
    def test_convert_rule(self):
        # Input XML rule
        input_xml = """
        <Rule>
            <Name>Test Rule</Name>
            <Condition field="field1" operator=">" value="30" />
            <Condition field="field2" operator=">" value="50" />
            <Action field="field3" value="Submit" />
        </Rule>
        """
        
        # Initialize the RuleConverter class
        rule_converter = RuleConverter()

        print("The input XML is \n" + input_xml)
        
        # Call the method and get the result
        result = rule_converter.convert_rule(input_xml)

        print("The fact result is \n" + result)
        
        # Expected output (adjusted for multiple conditions)
        expected_output = '''{
            "Rule": {
                "Name": "Test Rule",
                "Condition": [
                    {
                        "field": "field1",
                        "operator": ">",
                        "value": "30"
                    },
                    {
                        "field": "field2",
                        "operator": ">",
                        "value": "50"
                    }
                ],
                "Action": {
                    "field": "field3",
                    "value": "Submit"
                }
            }
        }'''
        
        print("The expected result is \n" + expected_output)
        
        # Check if the result matches the expected output
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()