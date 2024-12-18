import json
import os
import subprocess
import tempfile


class TerminalTestRunner:
    def __init__(self, test_dir, command):
        """
        Initialize the test runner.
        :param test_dir: Directory containing test cases.
        :param command: Terminal command template to run the application.
        """
        self.test_dir = test_dir
        self.command = command

    def load_test_cases(self):
        """
        Load and parse a test case with multiple untagged JSON parts.
        Assumes the file contains exactly three JSON objects in order:
        input -> intermediate state -> expected output.
        """
        test_files = [os.path.join(self.test_dir, f) for f in os.listdir(self.test_dir) if f.endswith("in.json")]
        print(test_files)

        for test_file in test_files:
            json_parts = []
            with open(test_file, 'r') as f:
                content = f.read()
                decoder = json.JSONDecoder(strict=False)
                idx = 0
                while idx < len(content):
                    try:
                        obj, idx = decoder.raw_decode(content, idx)
                        json_parts.append(obj)
                        while idx < len(content) and content[idx].isspace():
                            idx += 1
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        break

            if len(json_parts) != 3:
                raise ValueError(f"Expected exactly 3 parts in the test case, but found {len(json_parts)}")

            #print(json_parts[0])
            #print(json_parts[1])
            #print(json_parts[2])

            file = {
                "first": json_parts[0],
                "second": json_parts[1],
                "third": json_parts[2],
            }

            self.get_expected(test_file)

            #return {
                #"first": json_parts[0],
                #"second": json_parts[1],
                #"third": json_parts[2],
            #}

    def get_expected(self, test_file):
        result_files = [os.path.join(self.test_dir, f) for f in os.listdir(self.test_dir) if f.endswith("-out.json")]
        print(result_files[0][12])

        #for file in os.listdir(self.test_dir):
            #if file:

        for file in result_files:
            if file is test_file:
                print(file)

    def new(self):

        in_results = []
        out_results = []

        json_objects = []

        json_parts = []
        with open(result_files[0], 'r') as f:
            content = f.read()
            decoder = json.JSONDecoder(strict=False)
            idx = 0
            while idx < len(content):
                try:
                    obj, idx = decoder.raw_decode(content, idx)
                    json_parts.append(obj)
                    while idx < len(content) and content[idx].isspace():
                        idx += 1
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    break

        if len(json_parts) != 2:
            raise ValueError(f"Expected exactly 3 parts in the test case, but found {len(json_parts)}")

        #print(json_parts[0])
        #print(json_parts[1])

        return {
            "first": json_parts[0],
            "second": json_parts[1],
        }

        #for test_file in test_files:
            #json_parts = []
            #with open(test_file, 'r') as f:
                #for line in f:
                    #line = line.strip()
                    #if line:
                        #try:
                            #json_parts.append(json.loads(line))
                        #except json.JSONDecodeError as e:
                            #print(f"Error decoding JSON: {e}")
                #TerminalTestRunner.run_single_test(json_parts)
            #return json_parts

        #for test_file in test_files:
            #with open(test_file, 'r') as f:
                #print(test_file)
                #for line in f:
                    #json_objects.append(json.load(line))
                    #test_case = json.load()
            #result = self.run_single_test(test_case)
            #in_results.append(result)

        #self.print_results(in_results)

    def run_single_test(self, test_case):
        #input_data = #test_case["input"]
        #expected_output = #test_case["expected"]

        # Create a temporary file for the input
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_input:
            temp_input.write(json.dumps(input_data))
            temp_input.flush()

            command = f"{self.command} < {temp_input.name}"

            try:
                actual_output = subprocess.check_output(command, shell=True, text=True).strip()
                success = json.loads(actual_output) == expected_output
            except subprocess.CalledProcessError as e:
                actual_output = e.output.strip()
                success = False
            except json.JSONDecodeError:
                actual_output = "Invalid JSON output"
                success = False
            finally:
                os.unlink(temp_input.name)

        return {
            "expected": expected_output,
            "actual": json.loads(actual_output) if success else actual_output,
            "success": success,
        }

    def print_results(self, results):
        for i, result in enumerate(results):
            status = "PASS" if result["success"] else "FAIL"
            print(f"Test {i + 1}: {status}")
            if not result["success"]:
                print(f"  Input: {result['input']}")
                print(f"  Expected: {result['expected']}")
                print(f"  Actual: {result['actual']}")


# Example Usage
if __name__ == "__main__":
    test_runner = TerminalTestRunner(test_dir="ForStudents", command="./xgames-blogic")
    test_runner.load_test_cases()
