
# Create the model with consistent settings
model = ChatOpenAI(temperature=0
# Bind tools to enable tool calling - this is the key difference!
model_with_tools = model.bind_tools(tools)
return model_with_tools

def implement_check_for_tool_calls(response: AIMessage) -> bool:
    # Check if tool_calls exists and has content
    return bool(response.tool_calls)

def implement_execute_tool_call(tool_call: Dict, available_tools: List[Tool]) -> str:
    Args:
    tool_call (Dict): Tool call information with 'name' and 'args'
        available_tools (List[Tool]): List of available tools
Returns:
str: The result of the tool execution

💡 HINT:
1. Find the tool by name from available_tools
2. Extract the arguments from tool_cal

l['args']
3. Call the tool with the arguments
Example: tool_name = tool_call['name']
tool_args = tool_call['args']
# Find tool where tool.name == tool_name
# Execute: result = tool.func(tool_args['text'])
"""
# Extract tool name and arguments
tool_name = tool_call['name']
tool_args = tool_call['args']


# Find the tool by name
tool_to_use = None
for tool in available_tools:
    if tool.name == tool_name:
        tool_to_use = tool
        break

if tool_to_use is None:
    raise ValueError(f"Tool with name {tool_name} not found")

# Execute the tool with the provided arguments
# For our text length tool, we expect 'text' parameter
if 'text' in tool_args:
    result = tool_to_use.func(tool_args['text'])
else:
    # Fallback: pass the first argument value
    first_arg = next(iter(tool_args.values()))
    result = tool_to_use.func(first_arg)

return str(result)

def implement_run_agent_with_tool_calling(model_with_tools: ChatOpenAI,
                                    user_input: str,
                                    available_tools: List[Tool]) -> str:
"""
SOLUTION: Run the modern tool calling agent.
This replaces the complex ReAct while loop with a cleaner approach!

Args:
model_with_tools (ChatOpenAI): Model with tools bound
user_input (str): The use
r's question
available_tools (List[Tool]): Available tools for execution

Returns:
str: The final answer

print(f"🚀 Starting tool calling agent with input: {user_input}")

# Step 1: Send user input to the model
response = model_with_tools.invoke(user_input)
if response.content:
    print(f"📨 Model response: {response.content}")
else:
    print("📨 Model response: [Making tool calls - no content]")

# Step 2: Check if response has tool calls
if implement_check_for_tool_calls(response):
    print(f"🔧 Found {len(response.tool_calls)} tool call(s)")

    # Step 3: Execute each tool call and return result directly
    for tool_call in response.tool_calls:
        print(f"⚡ Executing tool: {tool_call['name']} with args: {tool_call['args']}")
        result = implement_execute_tool_call(tool_call, available_tools)
        print(f"✅ Tool result: {result}")

        # For this exercise, return the tool result directly
        return f"The length is {result} characters."
else:
    # No tool calls needed, return model's direct response
    print("💬 No tool calls needed, returning direct response")
    return response.content




