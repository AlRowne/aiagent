import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompts import system_prompt

_ = load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("No Gemini API Key found")


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    client = genai.Client(api_key=api_key)

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if not response.usage_metadata:
            raise RuntimeError("no metadata")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            function_results = []
            for function_call in response.function_calls:
                # print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception(
                        f"Function '{function_call.name}' returned no parts"
                    )
                if not function_call_result.parts[0].function_response:
                    raise Exception(
                        f"Function '{function_call.name}' returned no function_response"
                    )
                if not function_call_result.parts[0].function_response.response:
                    raise Exception(
                        f"Function '{function_call.name}' returned empty response"
                    )
                function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_results))

        elif response.text:
            print(response.text)
            break
        else:
            print("No final response after 20 iterations")
            sys.exit(1)
    else:
        print("No final response after 20 iterations")
        sys.exit(1)


if __name__ == "__main__":
    main()
