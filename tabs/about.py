import streamlit as st

def show_about():
    """显示关于页面内容"""
    st.title("About ProToxin")

    st.markdown("""
    ## Citing ProToxin

    PON-P3 was developed by Haohan Zhang, Yang Yang and Mauno Vihinen.

    Manuscript describing the method has been submitted.

    In the meantime, cite the URL of the predictor.

    ## How to run ProToxin

    1. **Upload your sequence(s)**: Upload a FASTA format file or paste your sequence(s) in FASTA format in the text area.
    2. **Submit**: Click the submit button to validate your input.
    3. **Run the prediction**: Click the "Start" button to start the analysis.
    4. **Results**: View your prediction results in the table showing toxicity probabilities.

    ### Example submission:
    ```
    >sp|P01375|TNFA_HUMAN Tumor necrosis factor
    MSTESMIRDVELAEEALPKKTGGPQGSRRCLFLSLFSFLIVAGATTLFCLLHFGVIGPQREEFPRDLSLISPLAQAVRSSSRTPSDKPVAHVVANPQAEGQLQWLNRRANALLANGVELRDNQLVVPSEGLYLIYSQVLFKGQGCPSTHVLLTHTISRIAVSYQTKVNLLSAIKSPCQRETPEGAEAKPWYEPIYLGGVFQLEKGDRLSAEINRPDYLDFAESGQVYFGIIAL
    ```

    ## Datasets

    Datasets were obtained with extensive data mining.

    [Download dataset](https://drive.google.com/drive/folders/19vRYJw3JuLg0hYpwIUaMeIVm-VC8Vx11?usp=sharing)

    ## Contact

    If you have any problems, please contact:
    
    Prof. Yang Yang: [yang.yang@example.edu](mailto:yang.yang@example.edu)
    
    Prof. Mauno Vihinen, Protein Structure and Bioinformatics Research group, Lund University, Sweden: [mauno.vihinen@example.edu](mailto:mauno.vihinen@example.edu)
    """)
