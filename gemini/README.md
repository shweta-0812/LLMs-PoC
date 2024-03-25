####How to use Gemini LLM for prompt based engineering.


1. go to the gemini dir
``$cd langchain``
2. [Optional] since gemini is written in flask, if you want to run it inside a python virtualenv then you can do the following:
``$pip3 install virtualenv``
``$virtualenv gemini_venv``
``$source gemini_venv/bin/activate``
and remember to run
``$deactivate`` after you have shutdown the flask backend server. 
3. run pip install for requirements.
``$pip3 install -r requirements.txt``
4. create a `.env` file inside the current dir and add the following env vars
  - GOOGLE_API_BASE=<your-val>
  - GOOGLE_API_KEY=<your-val>

5.Once the docker container is up, run the flask backend service
``$python3 app.py --debug``
6.To shut down the server. Simply do Crtl+C


Finally:
1. Check connection:
``GET http://127.0.0.1:5000/``
2. To run different methods, you can initiate the corresponding REST API endpoints for the same.


#### Things you can test

#### Scenario 1: Improve existing code

- Request Body:
{
    "prompt":"I don't think this code is the best way to do it in Python, can you help me? def func_x(array) for i in range(len(array)):print(array[i]). Please explain, in detail, what you did to improve it."
}
- Response JSON:
{
    "response": "**Improved Code:** \n\n ```python\ndef func_x(array):\n    print(*array, sep='\\n')\n```\n\n**Explanation:**\n\n**1. Using the Splat Operator (`*`):**\n\nThe splat operator (`*`) is used to unpack the array into individual elements. This allows us to print them on separate lines.\n\n**2. Using the `sep` Argument:**\n\nThe `sep` argument of the `print` function specifies the separator to use between the elements. Here, we set `sep` to '\\n' to print the elements on new lines.\n\n**Advantages of the Improved Code:**\n\n* **Concise:** The improved code is more concise and easier to read.\n* **Efficient:** It avoids the loop and instead uses the splat operator to unpack the array into individual elements.\n* **Readable:** The use of `sep` makes it clear that the elements are being printed on new lines.\n\n**Original Code:**\n\n```python\ndef func_x(array):\n    for i in range(len(array)):\n        print(array[i])\n```\n\n**Explanation:**\n\nThe original code iterates over the array using a `for` loop and prints each element using the `print` function. This code is verbose and can be improved using the splat operator and the `sep` argument.",
    "status": "success"
}
#### Scenario 2: Simplify code

Can you please simplify this code for a linked list in Python?\n class Node:\n def __init__(self, dataval=None):\n self.dataval = dataval\n self.nextval = None\n class SLinkedList:\n def __init__(self):\n self.headval = None\n list1 = SLinkedList()\n list1.headval = Node("Mon")\n e2 = Node("Tue")\n e3 = Node("Wed")\n list1.headval.nextval = e2\n e2.nextval = e3\n Explain in detail what you did to modify it, and why.
- Request Body:
{
    "prompt":"Can you please simplify this code for a linked list in Python?\\n class Node:\\n def __init__(self, dataval=None):\\n self.dataval = dataval\\n self.nextval = None\\n class SLinkedList:\\n def __init__(self):\\n self.headval = None\\n list1 = SLinkedList()\\n list1.headval = Node('Mon')\\n e2 = Node('Tue)\\n e3 = Node('Wed')\\n list1.headval.nextval = e2\\n e2.nextval = e3\\n Explain in detail what you did to modify it, and why."
}
- Response JSON:
{
    "response": "Certainly! Here's the simplified code for a linked list in Python:\n\n```python\nclass Node:\n    def __init__(self, data=None):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n\n# Create a linked list\nlinked_list = LinkedList()\n\n# Add nodes to the linked list\nnode1 = Node(\"Mon\")\nnode2 = Node(\"Tue\")\nnode3 = Node(\"Wed\")\n\nlinked_list.head = node1\nnode1.next = node2\nnode2.next = node3\n```\n\nHere's a detailed explanation of the modifications I made:\n\n1. **Removed unnecessary `val` suffix from class and method names:** The original code used the suffix `val` for class and method names, which is not a Python convention. I removed it to make the code more concise and readable.\n\n2. **Simplified class creation:** I simplified the class creation syntax by using a single line of code to create the `Node` and `LinkedList` classes.\n\n3. **Used `data` instead of `dataval`:** The `data` attribute is a more common name for the data stored in a node. I changed `dataval` to `data` to make the code more readable.\n\n4. **Used `head` instead of `headval`:** Similarly, `head` is a more common name for the head of a linked list. I changed `headval` to `head` to make the code more readable.\n\n5. **Simplified node creation:** I simplified the node creation syntax by using a single line of code to create each node.\n\n6. **Removed unnecessary `e2` and `e3` variables:** The original code used the variables `e2` and `e3` to store the second and third nodes, respectively. However, these variables are not necessary and only add clutter to the code. I removed them and directly assigned the second and third nodes to `node2` and `node3`.\n\n7. **Removed unnecessary `list1` variable:** The original code used the variable `list1` to store the linked list. However, this variable is not necessary since the linked list is already stored in the `linked_list` variable. I removed `list1` to make the code more concise and readable.\n\nThe resulting code is more concise, readable, and follows Python conventions while maintaining the same functionality as the original code.",
    "status": "success"
}
#### Scenario 3: Write test cases

#### Scenario 4: Make code more efficient

#### Scenario 5: Debug your code