// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 找到选项卡容器元素
    const tabsContainer = window.parent.document.querySelector('.stTabs [data-testid="stHorizontalTabs"]');
    if (tabsContainer) {
        // 创建logo容器
        const logoContainer = document.createElement('div');
        logoContainer.id = 'logo-container';

        // 创建logo图片元素
        const logoImg = document.createElement('img');
        logoImg.id = 'logo-img';
        logoImg.src = logo_base64_data;  // 这个变量会在加载脚本时由Python替换
        logoImg.alt = 'ProToxin Logo';

        // 将logo添加到容器中
        logoContainer.appendChild(logoImg);

        // 将logo容器添加到选项卡容器前面
        tabsContainer.parentNode.insertBefore(logoContainer, tabsContainer);

        // 添加点击事件处理
        logoImg.addEventListener('click', function() {
            // 找到Home选项卡并点击
            const tabs = window.parent.document.querySelectorAll('[role="tab"]');
            for (let i = 0; i < tabs.length; i++) {
                if (tabs[i].textContent.includes('Home')) {
                    tabs[i].click();
                    break;
                }
            }
        });
    }
});

