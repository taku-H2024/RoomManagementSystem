// 日付のフォーマット関数 (YYYY-MM-DD)
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 過去1週間の日付を生成
function generateLastWeekDates() {
    const dates = [];
    const today = new Date();
    for (let i = 0; i < 7; i++) {
        const date = new Date();
        date.setDate(today.getDate() - i);
        dates.push(formatDate(date));
    }
    return dates;
}

// 初期化
document.addEventListener('DOMContentLoaded', () => {
    const dateDisplay = document.getElementById('date-display');
    const dropdown = document.getElementById('dropdown');
    const currentDateSpan = document.getElementById('current-date');

    // サンプルユーザー名
    const name = "{{ name }}"; // 必要に応じてサーバー側から取得する

    // 初期日付設定
    // const initialDate = new Date();
    // currentDateSpan.textContent = formatDate(initialDate);

    // 過去1週間のプルダウンリストを作成
    const lastWeekDates = generateLastWeekDates();
    lastWeekDates.forEach(date => {
        const dateOption = document.createElement('div');
        dateOption.textContent = date;
        dateOption.addEventListener('click', () => {
            // URL先に遷移する
            const targetUrl = `/status/${name}/${date}`;
            window.location.href = targetUrl;
        });
        dropdown.appendChild(dateOption);
    });

    // 日付クリックでプルダウンを表示/非表示
    dateDisplay.addEventListener('click', () => {
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });

    // 他の箇所をクリックした際にプルダウンを閉じる
    document.addEventListener('click', (event) => {
        if (!dateDisplay.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.style.display = 'none';
        }
    });
});