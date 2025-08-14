import streamlit as st

def show_about():
    """显示关于页面内容"""
    st.title("About ProToxin")

    st.markdown("""
    
    Toxins are naturally poisonous small compounds, peptides and proteins which are produced in all three kingdoms. We developed a novel machine learning-based predictor for detecting protein toxins from their sequences. The gradient boosting method was trained on carefully selected training data. Extensive feature selection was made, starting with 2,614 features. Finally, there were 88 features. Comparison to available predictors indicated that ProToxin showed significant improvement compared to state-of-the-art predictors. On a blind test dataset, the accuracy was 0.906, the Matthews correlation coefficient was 0.796, and the overall performance measure was 0.796.
    """)

    st.markdown("""
    ## Citing ProToxin

    ProToxin was developed by Haohan Zhang, Yang Yang and Mauno Vihinen.

    The manuscript describing the method has been submitted.

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

    [Download the dataset](https://drive.google.com/drive/folders/19vRYJw3JuLg0hYpwIUaMeIVm-VC8Vx11?usp=sharing)

    ## Contact

    If you have any problems, please contact:
    
    Prof. Yang Yang, Suzhou Key Lab of Multi-modal Data Fusion and Intelligent Healthcare, China: [yyang@suda.edu.cn](mailto:yyang@suda.edu.cn)
    
    Prof. Mauno Vihinen, Protein Structure and Bioinformatics Research group, Lund University, Sweden: [mauno.vihinen@med.lu.se](mailto:mauno.vihinen@med.lu.se)
    """)
