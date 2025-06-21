import os
from PIL import Image
import base64
from io import BytesIO

from config.config import Config as cfg
from utils.ui_helpers import set_page_container_style, MAX_CONTENT_WIDTH
import streamlit as st

# 导入页面内容
from tabs.disclaimer import show_disclaimer
from tabs.about import show_about
from tabs.prediction import show_prediction


GOLDEN_RATIO_PERCENTAGE = 50


def welcome_section():
    """显示欢迎信息的函数"""
    # 直接显示标题，不再在这里显示logo（logo已移至页眉）
    st.title('Welcome to ProToxin')

    # 创建两列布局展示主要内容
    col1, _, col2 = st.columns([6, 0.5, 8])

    with col1:
        st.markdown("""
        ProToxin is a machine learning-based predictor for detecting protein toxins from sequences. 
        It is based on a machine learning algorithm, gradient boosting. ProToxin is a fast and efficient 
        method and is freely available. It can be used for small and large numbers of sequences.

        ProToxin was developed in the groups of Prof. Yang Yang, Suzhou Key Lab of Multi-modal Data Fusion and Intelligent Healthcare, 
        Suzhou City University and Prof. Mauno Vihinen, Protein Structure and Bioinformatics Research group, Lund University, Sweden.
        """)

    with col2:
        # 使用原始方式显示右侧图像，不添加额外样式控制
        st.image("assets/flowchart.v4.svg", caption="Flow chart of ProToxin", use_container_width=True)
        st.caption("pic by @Haohan Zhang, 2025, Department of Computer science of Soochow University, China")

    left, mid, right = st.columns([1, 1, 1])
    with left:
        st.markdown(
            """
            <div style="display: flex; justify-content: center; margin-top: 55px;">
                <img src="data:image/svg+xml;base64,{}" style="max-width: 400px; height: auto;">
            </div>
            """.format(
                base64.b64encode(open("assets/Lund_university_L_CMYK.svg", "rb").read()).decode()
            ),
            unsafe_allow_html=True
        )
    with mid:
        st.markdown(
            """
            <div style="display: flex; justify-content: center; margin-top: 50px;">
                <img src="data:image/png;base64,{}" style="max-width: 320px; height: auto;">
            </div>
            """.format(
                base64.b64encode(open("assets/suda2.png", "rb").read()).decode()
            ),
            unsafe_allow_html=True
        )
    with right:
        st.markdown(
            """
            <div style="display: flex; justify-content: center; margin-top: 50px;">
                <img src="data:image/png;base64,{}" style="max-width: 320px; height: auto;">
            </div>
            """.format(
                base64.b64encode(open("assets/csxy.png", "rb").read()).decode()
            ),
            unsafe_allow_html=True
        )


def home_page():
    """主页内容"""
    welcome_section()


def show_footer():
    """显示页脚信息"""
    # 定义年份和版权信息
    current_year = 2025  # 可以使用datetime.datetime.now().year获取当前年份

    # 使用HTML创建页脚内容，但不添加样式（样式已在CSS文件中定义）
    st.markdown(
        f"""
        <footer>
            <div style="max-width: {MAX_CONTENT_WIDTH}px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
                <div style="text-align: left;">Protein Structure and Bioinformatics Research Group</div>
                <div style="text-align: center;">© {current_year} ProToxin. All Rights Reserved.</div>
                <div style="text-align: right;">Lund University, Sweden</div>
            </div>
        </footer>
        """,
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    # 设置页面配置
    st.set_page_config(
        page_title="ProToxin",
        page_icon="🧬",
        layout="centered",  # 使用居中布局，通过自定义CSS控制具体宽度
    )

    # 应用自定义宽度设置
    set_page_container_style()

    os.makedirs(cfg.FASTA_SAVE_DIR, exist_ok=True)

    # 添加内容包装器开始标记，用于实现粘性页脚
    st.markdown('<div class="content-wrapper"><div class="main-content">', unsafe_allow_html=True)

    # 创建水平排列的Logo和导航栏
    header_container = st.container()
    with header_container:
        # ===== Logo 整行展示 + 负 margin =====
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'toxin-logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as f:
                    logo_base64 = base64.b64encode(f.read()).decode()

                st.markdown(
                    f"""
                    <div style="margin-bottom: -80px; margin-top: 0px;">
                        <img src="data:image/png;base64,{logo_base64}" style="width:100px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.warning("Logo图像不存在")
        except Exception as e:
            st.error(f"加载logo时出错：{str(e)}")

        # ===== Tabs 样式注入（居中） =====
        st.markdown("""
            <style>
            div[data-baseweb="tab-list"] {
                justify-content: center !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # ===== Tabs 本体 =====
        tab1, tab2, tab3, tab4 = st.tabs(["Home", "Prediction", "Disclaimer", "About"])

    # 使用各个标签页内容
    with tab1:
        home_page()  # 首页内容

    with tab2:
        show_prediction()  # 预测功能

    with tab3:
        show_disclaimer()  # 免责声明

    with tab4:
        show_about()  # 关于页面

    # 添加内容包装器结束标记
    st.markdown('</div>', unsafe_allow_html=True)

    # 在所有选项卡内容渲染后显示页脚
    show_footer()

    # 关闭内容包装器
    st.markdown('</div>', unsafe_allow_html=True)
