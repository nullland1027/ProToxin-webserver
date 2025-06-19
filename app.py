import io
import os
import time
import pandas as pd

from config.config import Config as cfg
from config.config import Warn, Success, Error
from utils import fasta
import streamlit as st

# 导入页面内容
from tabs.disclaimer import show_disclaimer
from tabs.about import show_about
from tabs.prediction import show_prediction

GOLDEN_RATIO_PERCENTAGE = 50
def set_page_container_style():
    # 自定义CSS来设置页面宽度百分比，并居中显示
    st.markdown(
        f"""
        <style>
        .block-container {{
            max-width: {GOLDEN_RATIO_PERCENTAGE}% !important;
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 3rem;
            margin: 0 auto;
        }}
        /* 自定义选项卡样式 */
        .st-cb {{
            font-size: 18px !important;
        }}
        /* 选项卡文本样式 */
        div[data-testid="stVerticalBlock"] div[role="tab"] {{
            font-size: 20px !important;
            font-weight: 500;
        }}
        /* 选项卡列表容器居中 */
        div[role="tablist"] {{
            display: flex;
            justify-content: center;
        }}
        /* 选项卡之间的间距 */
        button[role="tab"] {{
            margin: 0 1rem;
        }}
        /* 选中的选项卡样式 */
        button[role="tab"][aria-selected="true"] {{
            background-color: rgba(0, 104, 201, 0.1);
            border-radius: 5px;
        }}
        /* 页脚样式 */
        footer {{
            visibility: visible;
            width: 100% !important;  /* 使用100%宽度，与内容区域一致 */
            margin-top: 5rem;
            padding-top: 1.5rem;
            padding-bottom: 1rem;
            text-align: center;
            border-top: 1px solid #e1e4e8;
            position: relative; /* 改为相对定位，不浮动 */
            bottom: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def welcome_section():
    """显示欢迎信息的函数"""
    # Logo和标题区域 - 使用columns进行水平排列
    logo_col, title_col = st.columns([1, 4])

    with logo_col:
        # Logo位置
        # 可以使用本地Logo图片
        # st.image("path/to/your/logo.png", use_container_width=True)

        # 或使用占位图作为示例
        st.image("https://placehold.co/150x150?text=LOGO", use_container_width=True)

    with title_col:
        st.title('Welcome to ProToxin')

    # 创建两列布局展示主要内容
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        ProToxin is a machine learning-based predictor for detecting protein toxins from sequences. 
        It is based on a machine learning algorithm, gradient boosting. ProToxin is a fast and efficient 
        method and is freely available. It can be used for small and large numbers of sequences.

        ProToxin was developed in the groups of Prof. Yang Yang (add here the address) and 
        Prof. Mauno Vihinen, Protein Structure and Bioinformatics Research group, Lund University, Sweden.
        """)

    with col2:
        # 图片示例 - 你可以替换为你自己的图片路径
        # 1. 可以使用本地图片（需要放在正确的路径下）
        # st.image("path/to/your/image.png", caption="图片注解", use_container_width=True)

        # 2. 或者使用在线图片URL
        st.image("https://placehold.co/400x300?text=Your+Image+Here", caption="图片注解", use_container_width=True)

        # 图片下方的补充注释
        st.caption("这里可以添加关于图片的更多描述性文字，比如说明图像展示的是什么内容，或者数据来源等信息。")


def home_page():
    """主页内容"""
    welcome_section()


def show_footer():
    """显示页脚信息"""
    # 定义年份和版权信息
    current_year = 2025  # 可以使用datetime.datetime.now().year获取当前年份

    # 创建固定在底部的页脚
    st.markdown(
        f"""
        <div style="position: fixed; bottom: 0; left: 0; right: 0; width: 100%; background-color: white; z-index: 1000; padding-top: 1rem; padding-bottom: 1rem; border-top: 1px solid #c0c0c0;">
            <div style="width: {GOLDEN_RATIO_PERCENTAGE}%; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; color: #666666;">
                <div style="text-align: left;">Protein Structure and Bioinformatics Research Group</div>
                <div style="text-align: center;">© {current_year} ProToxin. All Rights Reserved.</div>
                <div style="text-align: right;">Lund University, Sweden</div>
            </div>
        </div>
        
        <!-- 添加额外的空间，防止内容被固定页脚遮挡 -->
        <div style="margin-bottom: 4rem;"></div>
        """,
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    # 设置页面配置
    st.set_page_config(
        page_title="ProToxin",
        layout="centered",  # 改回居中布局，我们将通过自定义CSS控制具体宽度
    )

    # 应用自定义宽度设置
    set_page_container_style()

    os.makedirs(cfg.FASTA_SAVE_DIR, exist_ok=True)

    # 使用Streamlit原生的选项卡组件创建导航，添加Prediction选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["Home", "Prediction", "Disclaimer", "About"])

    with tab1:
        home_page()  # 首页只显示欢迎信息

    with tab2:
        show_prediction()  # 使用从prediction.py导入的函数

    with tab3:
        show_disclaimer()

    with tab4:
        show_about()

    # 在所有选项卡内容渲染后显示页脚
    show_footer()
