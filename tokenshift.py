<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>75 Token Master Decoder</title>
    <!-- GPT-4o ve o1/o3 destekleyen o200k_base sözlüğü -->
    <script src="https://cdn.jsdelivr.net/npm/gpt-tokenizer/dist/o200k_base.js"></script>
    <style>
        body {
            background-color: #0b0f19;
            color: #f1f5f9;
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }
        .card {
            background-color: #1e293b;
            padding: 24px;
            border-radius: 12px;
            width: 100%;
            max-width: 520px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            border: 1px solid #334155;
        }
        h2 { margin-top: 0; text-align: center; color: #38bdf8; font-size: 1.2rem; }
        textarea {
            width: 100%;
            height: 100px;
            background-color: #0f172a;
            border: 1px solid #475569;
            border-radius: 8px;
            color: #fff;
            padding: 10px;
            box-sizing: border-box;
            resize: none;
            font-size: 13px;
            outline: none;
            margin-bottom: 12px;
        }
        .btn-group { display: flex; gap: 10px; margin-bottom: 15px; }
        button {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 13px;
            transition: 0.2s;
        }
        .btn-enc { background-color: #2563eb; color: white; }
        .btn-dec { background-color: #16a34a; color: white; }
        button:hover { opacity: 0.9; }
        .result-box {
            background-color: #0f172a;
            border: 1px dashed #475569;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            min-height: 50px;
            word-break: break-word;
            white-space: pre-wrap;
            color: #4ade80;
            user-select: all;
        }
    </style>
</head>
<body>

<div class="card">
    <h2>⚡ 75 Token Decoder (o200k_base)</h2>
    
    <textarea id="inputText" placeholder="Metin yaz (Şifrele) veya Sayıları yapıştır (Çöz)..."></textarea>
    
    <div class="btn-group">
        <button class="btn-enc" onclick="sifrele()">🔐 Metni Şifrele (+75)</button>
        <button class="btn-dec" onclick="coz()">🔓 Şifreyi Çöz (-75 & Metin)</button>
    </div>

    <div style="font-size: 12px; margin-bottom: 5px; color: #94a3b8;">Sonuç:</div>
    <div class="result-box" id="output">-</div>
</div>

<script>
    function getTokenizer() {
        if (typeof GPTTokenizer_o200k_base !== 'undefined') {
            return GPTTokenizer_o200k_base;
        }
        return null;
    }

    function sifrele() {
        const tokenizer = getTokenizer();
        if (!tokenizer) {
            showResult("❌ Kütüphane yüklenemedi! İnternet bağlantını kontrol et.", "#f87171");
            return;
        }

        const text = document.getElementById('inputText').value.trim();
        if (!text) {
            showResult("❌ Lütfen metin gir!", "#f87171");
            return;
        }

        try {
            const tokens = tokenizer.encode(text);
            const shifted = tokens.map(t => t + 75);
            showResult("[" + shifted.join(", ") + "]", "#38bdf8");
        } catch (e) {
            showResult("Hata: " + e.message, "#f87171");
        }
    }

    function coz() {
        const tokenizer = getTokenizer();
        if (!tokenizer) {
            showResult("❌ Kütüphane yüklenemedi! İnternet bağlantını kontrol et.", "#f87171");
            return;
        }

        const input = document.getElementById('inputText').value;
        const matches = input.match(/\d+/g);
        
        if (!matches || matches.length === 0) {
            showResult("❌ Yapıştırdığın metinde sayı bulunamadı!", "#f87171");
            return;
        }

        try {
            // 75 çıkar
            const rawTokens = matches.map(s => Number(s) - 75);
            // Decode et
            const decoded = tokenizer.decode(rawTokens);
            showResult(decoded, "#4ade80");
        } catch (e) {
            showResult("Hata: " + e.message, "#f87171");
        }
    }

    function showResult(text, color) {
        const out = document.getElementById('output');
        out.innerText = text;
        out.style.color = color;
    }
</script>

</body>
</html>
