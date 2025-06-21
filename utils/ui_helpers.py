import os
import base64
import streamlit as st

# 设置固定的最大宽度（像素）
MAX_CONTENT_WIDTH = 1200  # 可以根据需要调整这个值

def get_base64_encoded_image(image_path):
    """将图片转换为base64编码，以便在HTML中嵌入显示"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def load_css(css_file_path, max_width):
    """从文件加载CSS样式并注入到Streamlit页面"""
    with open(css_file_path, 'r') as f:
        css = f.read()

    # 替换CSS中的变量
    css = css.replace('MAX_CONTENT_WIDTH', f'{max_width}px')

    return f'<style>{css}</style>'

def load_js_with_logo(js_file_path, logo_path):
    """从文件加载JavaScript并注入logo数据"""
    with open(js_file_path, 'r') as f:
        js = f.read()

    # 注入logo的base64数据
    logo_base64 = get_base64_encoded_image(logo_path)
    js = js.replace('logo_base64_data', f'"data:image/png;base64,{logo_base64}"')

    return f'<script>{js}</script>'

def inject_custom_css_and_js(max_width):
    """注入自定义CSS和JavaScript到Streamlit页面"""
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        css_path = os.path.join(base_dir, 'static', 'css', 'style.css')
        js_path = os.path.join(base_dir, 'static', 'js', 'header.js')
        logo_path = os.path.join(base_dir, 'assets', 'toxin-logo.png')

        if not os.path.exists(css_path):
            st.error(f"CSS文件不存在: {css_path}")
            return

        if not os.path.exists(js_path):
            st.error(f"JS文件不存在: {js_path}")
            return

        if not os.path.exists(logo_path):
            st.error(f"Logo文件不存在: {logo_path}")
            return

        # 加载并注入CSS
        custom_css = load_css(css_path, max_width)

        # 加载并注入JavaScript（包含logo数据）
        custom_js = load_js_with_logo(js_path, logo_path)

        # 将CSS和JS注入到页面
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown(custom_js, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"注入CSS和JS时出错: {str(e)}")

def set_page_container_style():
    """设置页面容器样式和加载自定义CSS"""
    # 只加载CSS，不加载JavaScript
    st.markdown(
        f"""
        <style>
        .block-container {{
            max-width: {MAX_CONTENT_WIDTH}px !important;
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 3rem;
            margin: 0 auto;
        }}

        /* 当屏幕宽度小于MAX_CONTENT_WIDTH时，使用百分比宽度 */
        @media (max-width: {MAX_CONTENT_WIDTH}px) {{
            .block-container {{
                max-width: 95% !important;
            }}
        }}

        /* 页脚样式 */
        footer {{
            visibility: visible;
            width: 100% !important;
            margin-top: 5rem;
            padding-top: 1.5rem;
            padding-bottom: 1rem;
            text-align: center;
            border-top: 1px solid #e1e4e8;
            position: relative;
            bottom: 0;
        }}

        /* 自定义标签页样式，使选项卡居中但留出左侧logo空间 */
        .stTabs [data-testid="stHorizontalTabs"] {{
            padding-left: 100px;
            position: relative;
        }}

        /* logo容器样式 */
        .logo-container {{
            position: absolute;
            top: -40px;
            left: 0;
            z-index: 10;
        }}

        /* logo图像样式 */
        .logo-container img {{
            width: 80px;
            height: auto;
            cursor: pointer;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
