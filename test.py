import gradio as gr

def clear_tab2():
    return "", None, None  # Clear text, file, number

def clear_tab1():
    return "", ""

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Tab 1"):
            input1 = gr.Textbox(label="Input 1")
            input2 = gr.Textbox(label="Input 2")
            clear_btn1 = gr.Button("Clear Tab 2")
        
        with gr.Tab("Tab 2"):
            text_input = gr.Textbox(label="Text")
            file_input = gr.File(label="File")
            number_input = gr.Number(label="Number")
            clear_btn2 = gr.Button("Clear Tab 1")
    
    # Clear Tab 2 from Tab 1
    clear_btn1.click(
        fn=clear_tab2,
        inputs=None,
        outputs=[text_input, file_input, number_input]
    )
    
    # Clear Tab 1 from Tab 2
    clear_btn2.click(
        fn=clear_tab1,
        inputs=None,
        outputs=[input1, input2]
    )

demo.launch()