#written by alphawastaken

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.isEmpty():
            return self.items.pop()
        return None

    def isEmpty(self):
        return len(self.items) == 0


def is_balanced(string_input):
    stack_list = Stack()
    
    brackets_map = {')': '(', '}': '{', ']': '['}

    #iterate through each character in the input string.
    for char in string_input:
        if char in "([{":  #if the character is an opening bracket.
            stack_list.push(char)  #push it onto the stack.
        elif char in ")]}":  #if the character is a closing bracket.
            top_element = stack_list.pop()  #pop the top element from the stack.
            
            # check if the popped element matches the expected opening bracket.
            if top_element != brackets_map[char]:
                return False  # if not, the string is not balanced.

    #if the stack is empty, the string is balanced.
    return stack_list.isEmpty()



test = "(){}[]"
if is_balanced(test):
    print("Balanced")
else:
    print("Not Balanced")



