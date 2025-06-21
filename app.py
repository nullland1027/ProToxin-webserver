import io
import os
import time
import pandas as pd

from config.config import Config as cfg
from config.config import Warn, Success, Error
from utils import fasta
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

    # 创建固定在底部的页脚，使用固定宽度而非百分比
    st.markdown(
        f"""
        <div style="position: fixed; bottom: 0; left: 0; right: 0; width: 100%; background-color: white; z-index: 1000; padding-top: 1rem; padding-bottom: 1rem;">
            <div style="max-width: {MAX_CONTENT_WIDTH}px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; color: #666666; border-top: 1px solid #c0c0c0; padding-top: 1rem;">
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
        layout="centered",  # 使用居中布局，通过自定义CSS控制具体宽度
    )

    # 应用自定义宽度设置
    set_page_container_style()

    os.makedirs(cfg.FASTA_SAVE_DIR, exist_ok=True)

    # 创建水平排列的Logo和导航栏
    header_container = st.container()
    with header_container:
        logo_col, tabs_col = st.columns([1, 14])  # 分配左侧1/10给logo，右侧9/10给导航标签页

        with logo_col:
            # 加载logo图像
            try:
                logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'toxin-logo.png')
                if os.path.exists(logo_path):
                    st.image(logo_path, width=80)
                else:
                    st.warning("Logo图像不存在")
            except Exception as e:
                st.error(f"加载logo时出错：{str(e)}")

        with tabs_col:
            # 使用Streamlit原生的选项卡组件创建导航
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

    # 在所有选项卡内容渲染后显示页脚
    show_footer()
