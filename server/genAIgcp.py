import google.generativeai as genai
genai.configure(api_key='AIzaSyB-JV9h00I_lFNurzTZWc46qulRzYD--VI')
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def main() -> None:
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(read_text_file('./transcriptions.txt'))
    print(response.text)
    with open('response.txt', 'w') as t:
        t.write(response.text)

if __name__ == "__main__":
    main()