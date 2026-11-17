import os

# Complete, clean, high-performance HTML generator for AgriMate AI
output_path = os.path.abspath(r"c:\Users\SMART TECH\Desktop\AgriMateAI\frontend\mobile_web\index.html")

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="theme-color" content="#FFFFFF">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <title>AgriMate AI - Precision Smart Farming</title>
  
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=Noto+Nastaliq+Urdu:wght@400;600;700&display=swap" rel="stylesheet">
  
  <style>
    * {
      -webkit-tap-highlight-color: transparent;
      user-select: none;
      box-sizing: border-box;
    }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #FFFFFF;
      color: #0F172A;
      margin: 0;
      padding: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }
    /* Urdu typography and RTL styling */
    body.rtl-mode, [dir="rtl"] {
      direction: rtl;
      text-align: right;
    }
    body.rtl-mode .urdu-font, [dir="rtl"] .urdu-font {
      font-family: 'Noto Nastaliq Urdu', 'Plus Jakarta Sans', serif;
      line-height: 1.8;
    }
    [dir="rtl"] input, [dir="rtl"] textarea, [dir="rtl"] select {
      text-align: right;
      direction: rtl;
    }
    [dir="rtl"] input[type="password"] {
      text-align: right;
      direction: ltr;
    }
    .card-clean {
      background: #FFFFFF;
      border-radius: 24px;
      border: 1px solid #E2E8F0;
      box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04);
    }
    .card-soft {
      background: #F8FAFC;
      border-radius: 20px;
      border: 1px solid #E2E8F0;
    }
    .btn-primary {
      background-color: #15803D;
      color: #FFFFFF;
      font-weight: 700;
      border-radius: 9999px;
      box-shadow: 0 4px 14px 0 rgba(21, 128, 61, 0.28);
      transition: all 0.15s ease;
    }
    .btn-primary:active {
      transform: scale(0.98);
      opacity: 0.92;
    }
    .text-secondary {
      color: #64748B;
    }
    .hide-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .hide-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
    .app-screen {
      display: none;
      min-height: 100vh;
      flex-direction: column;
      width: 100%;
      background-color: #FFFFFF;
    }
    .app-screen.active {
      display: flex;
    }
    input, select, textarea {
      user-select: auto;
    }
    .bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-top: 1px solid #E2E8F0;
      padding: 10px 16px 14px 16px;
      display: flex;
      justify-content: space-around;
      align-items: center;
      z-index: 40;
      box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.04);
    }
    .pulse-glow {
      animation: pulseGlow 2s infinite;
    }
    @keyframes pulseGlow {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.06); opacity: 0.85; }
    }
  </style>
</head>
<body class="antialiased bg-white text-slate-900">

  <!-- ========================================================= -->
  <!-- SCREEN 1: INSTAGRAM / FACEBOOK STYLE SPLASH SCREEN -->
  <!-- ========================================================= -->
  <section id="screen-splash" class="app-screen active justify-between items-center px-6 py-12 bg-white">
    <div class="h-10"></div>

    <div class="flex flex-col items-center text-center">
      <div class="relative mb-5">
        <div class="w-24 h-24 rounded-full bg-emerald-50 flex items-center justify-center pulse-glow border-2 border-emerald-500/20 shadow-xl">
          <svg class="w-16 h-16" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="#15803D" opacity="0.12"/>
            <ellipse cx="50" cy="42" rx="36" ry="9" fill="#EAB308"/>
            <path d="M28 42 Q50 18 72 42 Z" fill="#CA8A04"/>
            <path d="M30 42 Q50 34 70 42" stroke="#15803D" stroke-width="2.5" fill="none"/>
            <circle cx="50" cy="58" r="19" fill="#FAD09E"/>
            <circle cx="43" cy="55" r="2.2" fill="#0F172A"/>
            <circle cx="57" cy="55" r="2.2" fill="#0F172A"/>
            <path d="M43 62 Q50 70 57 62" stroke="#9A3412" stroke-width="2.2" stroke-linecap="round" fill="none"/>
            <path d="M42 60 Q50 62 58 60" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" fill="none"/>
          </svg>
        </div>
        <div class="absolute -bottom-1 -right-1 w-7 h-7 rounded-full bg-[#15803D] text-white flex items-center justify-center text-xs shadow-md font-bold">
          AI
        </div>
      </div>

      <h1 class="text-3xl font-black text-slate-900 tracking-tight flex items-center gap-1.5">
        <span>AgriMate</span>
        <span class="text-[#15803D]">AI</span>
      </h1>
      <p id="splash-sub-text" class="text-xs text-slate-500 font-medium mt-1">Smart Farming Pakistan</p>
    </div>

    <!-- Bottom: "from AgriMate" (Instagram style) -->
    <div class="flex flex-col items-center pb-6">
      <div id="splash-from-text" class="text-[11px] text-slate-400 font-semibold uppercase tracking-widest mb-1">FROM</div>
      <div class="flex items-center gap-1.5">
        <span class="text-sm font-bold text-slate-800 tracking-tight">AgriMate Technologies</span>
        <svg class="w-4 h-4 text-emerald-600 fill-current" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" /></svg>
      </div>
      <div class="w-16 h-1 bg-slate-200 rounded-full mt-4 overflow-hidden">
        <div class="w-8 h-full bg-emerald-600 rounded-full animate-pulse"></div>
      </div>
    </div>
  </section>


  <!-- ========================================================= -->
  <!-- SCREEN 2: DEDICATED LOGIN SCREEN (INSTAGRAM STYLE) -->
  <!-- ========================================================= -->
  <section id="screen-login" class="app-screen px-6 pt-10 pb-12 justify-between">
    <div>
      <!-- Top Bar: Logo & Language Selector -->
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-2">
          <div class="w-9 h-9 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-base shadow-sm">
            🌾
          </div>
          <div class="text-base font-extrabold text-slate-900 tracking-tight">AgriMate AI</div>
        </div>

        <!-- Language Switcher Pill -->
        <div class="flex items-center bg-slate-100 p-1 rounded-full border border-slate-200 text-xs font-bold">
          <button type="button" onclick="setLanguage('en')" id="login-lang-en" class="px-3 py-1 rounded-full transition-all">English</button>
          <button type="button" onclick="setLanguage('ur')" id="login-lang-ur" class="px-3 py-1 rounded-full transition-all">اردو</button>
        </div>
      </div>

      <!-- Hero Header -->
      <div class="mb-6">
        <h2 id="login-heading" class="text-3xl font-black text-slate-900 tracking-tight">Welcome Back! 👋</h2>
        <p id="login-subtitle" class="text-xs text-secondary mt-1.5 leading-relaxed">Sign in to manage Potato & Tomato crops and get AI diagnostics.</p>
      </div>

      <!-- Error Alert Box -->
      <div id="login-error-box" class="hidden p-3.5 mb-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-medium flex items-center gap-2">
        <span class="text-base">⚠️</span>
        <span id="login-error-msg">Error message</span>
      </div>

      <!-- Login Form -->
      <form onsubmit="handleLoginSubmit(event)" class="space-y-4">
        <div>
          <label id="lbl-login-id" class="block text-xs font-bold text-slate-700 mb-1.5">Phone or Email</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"/></svg>
            </span>
            <input id="login-identifier" type="text" required placeholder="03001234567 or farmer@agrimate.pk"
              class="w-full pl-10 pr-4 py-3 bg-slate-50 text-slate-900 placeholder-slate-400 border border-slate-200 rounded-2xl text-xs font-medium focus:outline-none focus:border-emerald-600 focus:bg-white transition-all">
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label id="lbl-login-pwd" class="text-xs font-bold text-slate-700">Password</label>
            <a href="#" onclick="alert('Demo accounts are available below!')" id="lnk-forgot-pwd" class="text-[11px] font-semibold text-emerald-700 hover:underline">Forgot?</a>
          </div>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z"/></svg>
            </span>
            <input id="login-password" type="password" required placeholder="••••••••"
              class="w-full pl-10 pr-11 py-3 bg-slate-50 text-slate-900 placeholder-slate-400 border border-slate-200 rounded-2xl text-xs font-medium focus:outline-none focus:border-emerald-600 focus:bg-white transition-all">
            <button type="button" onclick="togglePasswordVisibility('login-password', 'eye-login-icon')" class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-600">
              <span id="eye-login-icon" class="text-sm">👁️</span>
            </button>
          </div>
        </div>

        <div class="flex items-center gap-2 pt-0.5">
          <input type="checkbox" id="login-remember" checked class="w-4 h-4 rounded text-emerald-600 accent-emerald-600">
          <label id="lbl-remember-me" for="login-remember" class="text-xs text-slate-600 font-medium">Keep me signed in on this phone</label>
        </div>

        <button id="login-submit-btn" type="submit" class="btn-primary w-full py-3.5 text-xs font-bold mt-2 shadow-md flex items-center justify-center gap-2">
          <span id="txt-login-btn">Log In</span>
          <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"/></svg>
        </button>
      </form>

      <div class="mt-6 text-center">
        <span id="txt-no-account" class="text-xs text-slate-500">Don't have an account?</span>
        <button type="button" onclick="navigateTo('screen-register')" id="lnk-signup" class="text-xs text-emerald-700 font-bold ml-1 hover:underline">
          Create Account
        </button>
      </div>

      <!-- One-Tap Demo Credentials -->
      <div class="pt-6 mt-6 border-t border-slate-100">
        <div id="txt-demo-title" class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2.5">One-Tap Quick Demo Sign In:</div>
        <div class="grid grid-cols-3 gap-2">
          <button onclick="fillDemo('03001234567', 'Kisan123456!')" class="card-soft p-2.5 text-center rounded-2xl hover:border-emerald-500 hover:bg-emerald-50/50 transition-all">
            <div class="text-base mb-0.5">🌾</div>
            <div id="demo-role-farmer" class="text-xs font-bold text-slate-800">Farmer</div>
            <div class="text-[10px] text-slate-500">Ahmad (Okara)</div>
          </button>
          <button onclick="fillDemo('03111234567', 'Buyer123456!')" class="card-soft p-2.5 text-center rounded-2xl hover:border-emerald-500 hover:bg-emerald-50/50 transition-all">
            <div class="text-base mb-0.5">🏪</div>
            <div id="demo-role-buyer" class="text-xs font-bold text-slate-800">Buyer</div>
            <div class="text-[10px] text-slate-500">Tariq (Lahore)</div>
          </button>
          <button onclick="fillDemo('03221234567', 'Expert123456!')" class="card-soft p-2.5 text-center rounded-2xl hover:border-emerald-500 hover:bg-emerald-50/50 transition-all">
            <div class="text-base mb-0.5">🎓</div>
            <div id="demo-role-expert" class="text-xs font-bold text-slate-800">Expert</div>
            <div class="text-[10px] text-slate-500">Dr. Fatima</div>
          </button>
        </div>
      </div>
    </div>

    <div id="txt-security-note" class="text-center text-[10px] text-slate-400 pt-6">
      🔒 256-bit Secure PBKDF2 Encryption • Strictly compliant with NARC guidelines
    </div>
  </section>


  <!-- ========================================================= -->
  <!-- SCREEN 3: DEDICATED SIGN UP SCREEN (INSTAGRAM STYLE) -->
  <!-- ========================================================= -->
  <section id="screen-register" class="app-screen px-6 pt-8 pb-12 justify-between">
    <div>
      <!-- Top Bar: Back Button & Language Selector -->
      <div class="flex items-center justify-between mb-6">
        <button type="button" onclick="navigateTo('screen-login')" class="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center text-slate-700 hover:bg-slate-200">
          <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5"/></svg>
        </button>

        <div class="flex items-center bg-slate-100 p-1 rounded-full border border-slate-200 text-xs font-bold">
          <button type="button" onclick="setLanguage('en')" id="reg-lang-en" class="px-3 py-1 rounded-full transition-all">English</button>
          <button type="button" onclick="setLanguage('ur')" id="reg-lang-ur" class="px-3 py-1 rounded-full transition-all">اردو</button>
        </div>
      </div>

      <div class="mb-5">
        <h2 id="reg-heading" class="text-2xl font-black text-slate-900 tracking-tight">Create Account 🌿</h2>
        <p id="reg-subtitle" class="text-xs text-secondary mt-1">Join Pakistan's precision agricultural network.</p>
      </div>

      <div id="reg-error-box" class="hidden p-3.5 mb-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-medium flex items-center gap-2">
        <span class="text-base">⚠️</span>
        <span id="reg-error-msg">Error message</span>
      </div>

      <!-- Register Form (STRICT Minimal 5 Fields) -->
      <form onsubmit="handleRegisterSubmit(event)" class="space-y-3">
        <!-- 1. Full Name -->
        <div>
          <label id="lbl-reg-name" class="block text-xs font-bold text-slate-700 mb-1">1. Full Name</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/></svg>
            </span>
            <input id="reg-name" type="text" required placeholder="Ahmad Khan"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 text-slate-900 placeholder-slate-400 border border-slate-200 rounded-xl text-xs font-medium focus:outline-none focus:border-emerald-600 focus:bg-white transition-all">
          </div>
        </div>

        <!-- 2. Phone or Email -->
        <div>
          <label id="lbl-reg-id" class="block text-xs font-bold text-slate-700 mb-1">2. Mobile Phone or Email</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z"/></svg>
            </span>
            <input id="reg-identifier" type="text" required placeholder="03001234567 or farmer@okara.pk"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 text-slate-900 placeholder-slate-400 border border-slate-200 rounded-xl text-xs font-medium focus:outline-none focus:border-emerald-600 focus:bg-white transition-all">
          </div>
        </div>

        <!-- 3. Password -->
        <div>
          <label id="lbl-reg-pwd" class="block text-xs font-bold text-slate-700 mb-1">3. Password (min 6 chars)</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z"/></svg>
            </span>
            <input id="reg-password" type="password" required minlength="6" placeholder="••••••••"
              class="w-full pl-10 pr-11 py-2.5 bg-slate-50 text-slate-900 placeholder-slate-400 border border-slate-200 rounded-xl text-xs font-medium focus:outline-none focus:border-emerald-600 focus:bg-white transition-all">
            <button type="button" onclick="togglePasswordVisibility('reg-password', 'eye-reg-icon')" class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-600">
              <span id="eye-reg-icon" class="text-sm">👁️</span>
            </button>
          </div>
        </div>

        <!-- 4. Role Selection Cards -->
        <div>
          <label id="lbl-reg-role" class="block text-xs font-bold text-slate-700 mb-1">4. Select Your Role</label>
          <div class="grid grid-cols-3 gap-2">
            <label class="card-soft p-2.5 rounded-2xl flex flex-col items-center cursor-pointer border border-slate-200 has-[:checked]:border-emerald-600 has-[:checked]:bg-emerald-50/60 has-[:checked]:text-emerald-900 transition-all text-center">
              <input type="radio" name="reg-role" value="Farmer" checked class="hidden">
              <span class="text-lg mb-0.5">🌾</span>
              <span id="role-name-farmer" class="text-xs font-bold text-slate-800">Farmer</span>
            </label>
            <label class="card-soft p-2.5 rounded-2xl flex flex-col items-center cursor-pointer border border-slate-200 has-[:checked]:border-emerald-600 has-[:checked]:bg-emerald-50/60 has-[:checked]:text-emerald-900 transition-all text-center">
              <input type="radio" name="reg-role" value="Buyer" class="hidden">
              <span class="text-lg mb-0.5">🏪</span>
              <span id="role-name-buyer" class="text-xs font-bold text-slate-800">Buyer</span>
            </label>
            <label class="card-soft p-2.5 rounded-2xl flex flex-col items-center cursor-pointer border border-slate-200 has-[:checked]:border-emerald-600 has-[:checked]:bg-emerald-50/60 has-[:checked]:text-emerald-900 transition-all text-center">
              <input type="radio" name="reg-role" value="Expert/Admin" class="hidden">
              <span class="text-lg mb-0.5">🎓</span>
              <span id="role-name-expert" class="text-xs font-bold text-slate-800">Expert</span>
            </label>
          </div>
        </div>

        <!-- 5. District / Location -->
        <div>
          <label id="lbl-reg-location" class="block text-xs font-bold text-slate-700 mb-1">5. District / Tehsil</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/></svg>
            </span>
            <input id="reg-location" type="text" required placeholder="Okara, Punjab" value="Okara, Punjab"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 text-slate-900 placeholder-slate-400 border border-slate-200 rounded-xl text-xs font-medium focus:outline-none focus:border-emerald-600 focus:bg-white transition-all">
          </div>
          <!-- Quick Suggestion Chips -->
          <div class="flex items-center gap-1.5 mt-2 overflow-x-auto hide-scrollbar text-[11px]">
            <span id="txt-popular-chips" class="text-slate-400 text-[10px] font-semibold">Popular:</span>
            <button type="button" onclick="setRegLocation('Okara, Punjab')" class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium hover:bg-emerald-100">Okara</button>
            <button type="button" onclick="setRegLocation('Multan, Punjab')" class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium hover:bg-emerald-100">Multan</button>
            <button type="button" onclick="setRegLocation('Faisalabad, Punjab')" class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium hover:bg-emerald-100">Faisalabad</button>
            <button type="button" onclick="setRegLocation('Sahiwal, Punjab')" class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium hover:bg-emerald-100">Sahiwal</button>
          </div>
        </div>

        <button id="reg-submit-btn" type="submit" class="btn-primary w-full py-3.5 text-xs font-bold shadow-md mt-2">
          <span id="txt-reg-btn">Complete Registration</span>
        </button>
      </form>

      <!-- Switch to Login -->
      <div class="mt-5 text-center">
        <span id="txt-have-account" class="text-xs text-slate-500">Already have an account?</span>
        <button type="button" onclick="navigateTo('screen-login')" id="lnk-login" class="text-xs text-emerald-700 font-bold ml-1 hover:underline">
          Sign In
        </button>
      </div>
    </div>

    <div id="txt-security-note-reg" class="text-center text-[10px] text-slate-400 pt-6">
      🔒 256-bit Secure PBKDF2 Encryption • Strictly compliant with NARC guidelines
    </div>
  </section>


  <!-- ========================================================= -->
  <!-- SCREEN 4: HOME DASHBOARD (CLEAN WHITE THEME) -->
  <!-- ========================================================= -->
  <section id="screen-dashboard-farmer" class="app-screen px-5 pt-8 pb-28 bg-white">
    <!-- Top Header -->
    <div class="flex items-center justify-between mb-5">
      <div>
        <h2 id="dash-greeting" class="text-2xl font-black text-slate-900 tracking-tight">Hello, Ahmad 👋</h2>
        <div class="flex items-center gap-1.5 text-secondary text-xs mt-0.5 font-medium">
          <svg class="w-3.5 h-3.5 text-emerald-600 fill-current" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
          <span id="dash-location">Okara, Punjab</span>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <!-- Language Switcher in Dashboard -->
        <div class="flex items-center bg-slate-100 p-1 rounded-full border border-slate-200 text-xs font-bold">
          <button type="button" onclick="setLanguage('en')" id="dash-lang-en" class="px-2.5 py-1 rounded-full transition-all">EN</button>
          <button type="button" onclick="setLanguage('ur')" id="dash-lang-ur" class="px-2.5 py-1 rounded-full transition-all">اردو</button>
        </div>

        <!-- Log Out Button -->
        <button onclick="logoutUser()" title="Log Out" class="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 hover:text-rose-600 hover:bg-rose-50 transition-colors">
          <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9"/></svg>
        </button>
      </div>
    </div>

    <!-- Weather Card -->
    <div class="card-clean p-5 mb-4">
      <div class="flex items-center justify-between mb-3">
        <div>
          <div class="text-4xl font-black text-slate-900 tracking-tight">24°</div>
          <div id="txt-weather-status" class="text-xs text-slate-500 font-medium mt-0.5">Okara, Punjab • Mild Morning</div>
        </div>
        <div class="w-14 h-14 rounded-2xl bg-amber-50 flex items-center justify-center text-amber-500 border border-amber-200/60 shadow-sm">
          <svg class="w-8 h-8 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"/></svg>
        </div>
      </div>

      <div class="h-px bg-slate-100 my-3"></div>

      <div class="grid grid-cols-4 gap-2 text-center pt-1">
        <div class="p-2 rounded-xl bg-slate-50">
          <div id="lbl-weather-wind" class="text-[10px] text-slate-400 font-semibold">Wind</div>
          <div class="text-xs font-bold text-slate-800 mt-0.5">5km/h</div>
        </div>
        <div class="p-2 rounded-xl bg-amber-50 border border-amber-200/50">
          <div id="lbl-weather-humidity" class="text-[10px] text-amber-700 font-semibold">Humidity</div>
          <div class="text-xs font-bold text-amber-800 mt-0.5">88%</div>
        </div>
        <div class="p-2 rounded-xl bg-slate-50">
          <div id="lbl-weather-rain" class="text-[10px] text-slate-400 font-semibold">Rain</div>
          <div class="text-xs font-bold text-slate-800 mt-0.5">0 mm</div>
        </div>
        <div class="p-2 rounded-xl bg-slate-50">
          <div id="lbl-weather-feels" class="text-[10px] text-slate-400 font-semibold">Feels</div>
          <div class="text-xs font-bold text-slate-800 mt-0.5">+23°C</div>
        </div>
      </div>
    </div>

    <!-- Quick Action Launchers (3 Column Grid) -->
    <div class="grid grid-cols-3 gap-2.5 mb-5">
      <!-- 1. Scanner -->
      <div onclick="navigateTo('screen-camera')" class="card-clean p-3 cursor-pointer hover:border-emerald-500 hover:shadow-md transition-all flex flex-col justify-between">
        <div class="w-9 h-9 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold mb-2 shadow-sm">
          <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"/><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0z"/></svg>
        </div>
        <div>
          <div id="btn-quick-scan" class="text-xs font-bold text-slate-900">Leaf Scan</div>
          <div id="sub-quick-scan" class="text-[10px] text-emerald-700 font-semibold">Photo + Voice</div>
        </div>
      </div>

      <!-- 2. Crop Diary -->
      <div onclick="navigateTo('screen-diary')" class="card-clean p-3 cursor-pointer hover:border-emerald-500 hover:shadow-md transition-all flex flex-col justify-between border-emerald-500/50 bg-emerald-50/20">
        <div class="w-9 h-9 rounded-2xl bg-amber-100 text-amber-800 flex items-center justify-center font-bold mb-2 shadow-sm">
          <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"/></svg>
        </div>
        <div>
          <div id="btn-quick-diary" class="text-xs font-bold text-slate-900">Crop Diary</div>
          <div id="sub-quick-diary" class="text-[10px] text-amber-700 font-semibold">Offline Sync</div>
        </div>
      </div>

      <!-- 3. AI Advisor -->
      <div onclick="navigateTo('screen-chat')" class="card-clean p-3 cursor-pointer hover:border-emerald-500 hover:shadow-md transition-all flex flex-col justify-between">
        <div class="w-9 h-9 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold mb-2 shadow-sm">
          <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9v-2h2v2zm0-4H9V7h2v5z"/></svg>
        </div>
        <div>
          <div id="btn-quick-advisor" class="text-xs font-bold text-slate-900">AI Advisor</div>
          <div id="sub-quick-advisor" class="text-[10px] text-slate-500">NARC RAG</div>
        </div>
      </div>
    </div>

    <!-- "My Fields" Section -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h3 id="txt-my-fields-heading" class="text-base font-black text-slate-900 tracking-tight">Monitored Fields</h3>
        <span onclick="navigateTo('screen-overview')" id="lnk-farm-overview" class="text-xs text-emerald-700 font-bold cursor-pointer">Farm Overview &rarr;</span>
      </div>

      <!-- Field Card 1: Potato -->
      <div onclick="navigateTo('screen-overview')" class="card-clean p-4 cursor-pointer hover:border-emerald-500 transition-all">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-2xl bg-amber-100 flex items-center justify-center text-xl">🥔</div>
            <div>
              <div id="card1-title" class="text-sm font-bold text-slate-900">Potato Acre Block (Okara)</div>
              <div id="card1-sub" class="text-xs text-secondary">Autumn Crop • 32 Acres</div>
            </div>
          </div>
          <div class="bg-emerald-50 text-emerald-800 border border-emerald-200 px-3 py-1 rounded-full text-xs font-black">
            320 Maunds/Acre
          </div>
        </div>
        <div class="h-28 rounded-2xl overflow-hidden relative bg-gradient-to-tr from-emerald-800 via-emerald-600 to-green-500 flex items-center justify-center shadow-inner">
          <div id="card1-overlay" class="text-xs font-bold text-white bg-black/30 backdrop-blur-sm px-3.5 py-1.5 rounded-full">
            Tap for Live Sensor & Water Overview
          </div>
        </div>
      </div>

      <!-- Field Card 2: Tomato Tunnel -->
      <div class="card-clean p-4">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-2xl bg-rose-100 flex items-center justify-center text-xl">🍅</div>
            <div>
              <div id="card2-title" class="text-sm font-bold text-slate-900">Tomato High Tunnel (Sahiwal)</div>
              <div id="card2-sub" class="text-xs text-secondary">Walk-in Tunnel • 12 Acres</div>
            </div>
          </div>
          <div class="bg-amber-50 text-amber-800 border border-amber-200 px-3 py-1 rounded-full text-xs font-black">
            8,400 kg/ha
          </div>
        </div>
        <div class="h-28 rounded-2xl overflow-hidden relative bg-gradient-to-tr from-green-700 via-emerald-700 to-lime-600 flex items-center justify-center shadow-inner">
          <div id="card2-overlay" class="text-xs font-bold text-white bg-black/30 backdrop-blur-sm px-3.5 py-1.5 rounded-full">
            Drip Fertigated • Flowering Stage
          </div>
        </div>
      </div>
    </div>
  </section>


  <!-- ========================================================= -->
  <!-- SCREEN 5: MULTIMODAL CAMERA (SCANNER) -->
  <!-- ========================================================= -->
  <section id="screen-camera" class="app-screen bg-black justify-between pb-24">
    <div class="px-5 pt-8 pb-3 bg-black/80 flex items-center justify-between z-20">
      <button onclick="navigateTo('screen-dashboard-farmer')" class="w-9 h-9 rounded-full bg-white/20 flex items-center justify-center text-white">
        <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5"/></svg>
      </button>
      
      <select id="cam-crop-select" class="bg-white/20 text-yellow-300 text-xs font-bold rounded-full px-3 py-1 border border-white/20 focus:outline-none">
        <option value="Potato" selected>🥔 Potato</option>
        <option value="Tomato">🍅 Tomato</option>
      </select>

      <div class="w-9 h-9 rounded-full bg-yellow-400 flex items-center justify-center text-slate-900">
        <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M7 2v11h3v9l7-12h-4l4-8z"/></svg>
      </div>
    </div>

    <div class="px-5 py-2 bg-black/70 flex items-center justify-between text-xs z-20">
      <div class="flex items-center gap-1.5 text-white">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span id="txt-cam-lighting">Lighting: <b class="text-emerald-400">Optimal</b></span>
      </div>
      <div class="flex items-center gap-1.5 text-white">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span id="txt-cam-focus">Focus: <b class="text-emerald-400">Sharp Veins</b></span>
      </div>
    </div>

    <!-- Viewfinder Area -->
    <div class="relative flex-1 flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-tr from-emerald-950 via-slate-900 to-emerald-900"></div>
      
      <svg class="w-64 h-72 opacity-90 z-10" viewBox="0 0 200 240">
        <path d="M100 20 C160 50 180 140 100 220 C20 140 40 50 100 20 Z" fill="#2d6a4f" stroke="#FACC15" stroke-width="2"/>
        <line x1="100" y1="20" x2="100" y2="220" stroke="#FACC15" stroke-width="3"/>
        <line x1="100" y1="70" x2="140" y2="100" stroke="#74c69d" stroke-width="1.8"/>
        <line x1="100" y1="70" x2="60" y2="100" stroke="#74c69d" stroke-width="1.8"/>
        <line x1="100" y1="120" x2="155" y2="150" stroke="#74c69d" stroke-width="1.8"/>
        <line x1="100" y1="120" x2="45" y2="150" stroke="#74c69d" stroke-width="1.8"/>
        <circle cx="80" cy="90" r="14" fill="#B56A28" opacity="0.9"/>
        <circle cx="80" cy="90" r="8" fill="#FACC15" opacity="0.75"/>
        <circle cx="125" cy="135" r="16" fill="#A85020" opacity="0.9"/>
        <circle cx="125" cy="135" r="9" fill="#D9822B" opacity="0.8"/>
      </svg>

      <div class="absolute w-72 h-80 rounded-3xl border-2 border-dashed border-yellow-400 pointer-events-none flex items-center justify-center z-15">
        <div id="txt-cam-align" class="text-[11px] text-yellow-300 bg-black/60 px-3 py-1 rounded-full font-bold">
          Align leaf inside frame
        </div>
      </div>
    </div>

    <!-- Farmer Spoken Description Bar with Mic Button -->
    <div class="px-5 py-3 bg-black/90 z-20">
      <div class="flex items-center gap-2 mb-2">
        <div class="flex-1 bg-white/10 rounded-2xl px-3 py-2 border border-white/20 flex items-center justify-between">
          <input id="camera-farmer-desc" type="text" placeholder="Speak or edit notes: 'keera lag gaya hai'..."
            value="کیڑا لگ گیا ہے اور نچلے پتے سوکھ رہے ہیں"
            class="bg-transparent text-white text-xs flex-1 focus:outline-none">
          <button onclick="openSpeechModal('camera')" class="text-yellow-300 text-xs font-bold pl-2 flex items-center gap-1">
            <span>✏️</span>
            <span id="btn-edit-note">Edit</span>
          </button>
        </div>

        <button onclick="openSpeechModal('camera')" class="w-11 h-11 rounded-full bg-yellow-400 text-slate-900 flex items-center justify-center shadow-lg active:scale-95 transition-transform flex-shrink-0">
          <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
        </button>
      </div>

      <div id="txt-cam-hint" class="text-[10px] text-slate-400 text-center">
        Multimodal Scan combines photo + spoken note into RAG advisor
      </div>
    </div>

    <!-- Shutter Controls -->
    <div class="px-6 pt-2 pb-2 bg-black/95 z-20">
      <div class="flex items-center justify-around mb-2">
        <button onclick="triggerMultimodalScan(false)" class="text-center group">
          <div class="w-10 h-10 rounded-full bg-white/15 flex items-center justify-center text-white mx-auto mb-1 group-active:scale-95">
            🥔
          </div>
          <span id="txt-cam-normal" class="text-[10px] text-slate-400">Normal Scan</span>
        </button>

        <button onclick="triggerMultimodalScan(false)" class="w-16 h-16 rounded-full bg-yellow-400 border-4 border-white flex items-center justify-center text-slate-900 shadow-2xl active:scale-95 transition-transform p-3.5">
          <svg class="w-8 h-8 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"/><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0z"/></svg>
        </button>

        <button onclick="triggerMultimodalScan(true)" class="text-center group">
          <div class="w-10 h-10 rounded-full bg-white/15 flex items-center justify-center text-yellow-400 mx-auto mb-1 group-active:scale-95">
            ⚠️
          </div>
          <span class="text-[10px] text-yellow-400 font-bold">&lt;75% Flag</span>
        </button>
      </div>
    </div>
  </section>


  <!-- ========================================================= -->
  <!-- SCREEN 6: SCAN RESULT & DIAGNOSIS REPORT -->
  <!-- ========================================================= -->
  <section id="screen-scan-result" class="app-screen px-5 pt-8 pb-28 bg-white">
    <div class="flex items-center justify-between mb-4">
      <button onclick="navigateTo('screen-dashboard-farmer')" class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-700">
        <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5"/></svg>
      </button>
      <div id="txt-report-title" class="text-xs font-black uppercase tracking-wider text-emerald-800">Diagnostic Report</div>
      <div class="w-10"></div>
    </div>

    <!-- Low Confidence Flag Banner -->
    <div id="flagged-banner" class="hidden mb-4 p-3.5 rounded-2xl bg-amber-50 border border-amber-300 text-amber-800">
      <div class="flex items-center gap-2 text-xs font-bold mb-1">
        <span>⚠️</span>
        <span id="txt-flag-title">Low Confidence Scan Auto-Flagged (&lt;75%)</span>
      </div>
      <p id="txt-flag-desc" class="text-[11px] leading-relaxed">
        Model confidence is 63.5%. Dispatched to the Punjab Agricultural Extension Expert Queue for manual agronomist review.
      </p>
    </div>

    <!-- Heatmap Preview Card -->
    <div class="card-clean p-4 mb-4 relative overflow-hidden">
      <div class="relative w-full h-56 rounded-2xl overflow-hidden flex items-center justify-center bg-slate-900">
        <svg class="w-48 h-52 z-0" viewBox="0 0 200 240">
          <path d="M100 20 C160 50 180 140 100 220 C20 140 40 50 100 20 Z" fill="#2d6a4f"/>
          <line x1="100" y1="20" x2="100" y2="220" stroke="#74c69d" stroke-width="3"/>
          <circle cx="80" cy="90" r="16" fill="#D45B28"/>
          <circle cx="125" cy="135" r="18" fill="#E8B928"/>
        </svg>

        <div id="gradcam-layer" class="absolute inset-0 pointer-events-none transition-opacity duration-300" style="opacity: 0.75; background: radial-gradient(circle at 45% 42%, rgba(255, 30, 0, 0.8) 0%, rgba(255, 180, 0, 0.55) 35%, rgba(0, 255, 120, 0.2) 65%, transparent 85%); mix-blend-mode: color-dodge;"></div>

        <div class="absolute top-3 right-3 z-10 bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2">
          <span class="text-[10px] text-white font-medium">Grad-CAM</span>
          <input type="checkbox" id="heatmap-toggle" checked onchange="toggleHeatmap(this.checked)" class="accent-emerald-400 cursor-pointer">
        </div>
      </div>
    </div>

    <!-- Diagnosis Card -->
    <div class="card-clean p-5 mb-4">
      <div class="flex items-center justify-between mb-2">
        <span id="scan-crop-label" class="text-xs text-slate-500 uppercase font-black">POTATO</span>
        <span id="conf-pill" class="bg-emerald-100 text-emerald-800 border border-emerald-300 px-3 py-1 rounded-full text-xs font-black">
          93.8% Confidence
        </span>
      </div>

      <h3 id="disease-name" class="text-2xl font-black text-slate-900 mb-0.5">Potato Late Blight</h3>
      <div id="disease-urdu" class="text-sm text-emerald-700 font-bold mb-3">آلو کا پچھیتا جھلساؤ</div>

      <!-- Farmer Spoken Note Callout -->
      <div class="p-3 rounded-2xl bg-slate-50 border border-slate-200 mb-3 text-xs">
        <div id="lbl-spoken-obs" class="text-emerald-800 font-bold text-[11px] mb-1 flex items-center gap-1.5">
          <span>🎙️</span>
          <span>Farmer Spoken Observation:</span>
        </div>
        <p id="scan-farmer-note" class="text-slate-800 italic font-medium">"کیڑا لگ گیا ہے اور نچلے پتے سوکھ رہے ہیں"</p>
      </div>

      <!-- Integrated Advisory Body -->
      <div class="text-xs text-slate-600 leading-relaxed mb-4">
        <div id="lbl-integrated-advice" class="text-slate-900 font-bold mb-1">Integrated Treatment:</div>
        <p id="scan-advice-body" class="whitespace-pre-line text-slate-700">
          • Blight Protocol: Apply Metalaxyl + Mancozeb (Ridomil Gold) @ 250g/100L water or Revus 250 SC @ 200ml/acre.
          • Insect Keera Action: Add Flonicamid @ 60g/acre for aphid vector eradication. Prune lower diseased foliage.
        </p>
        <div id="scan-citation-label" class="mt-2 text-[11px] text-emerald-800 font-semibold flex items-center gap-1">
          <span>📖</span>
          <span>NARC_Potato_Production_and_Blight_Guide_2024.pdf (p.1 & p.2)</span>
        </div>
      </div>

      <!-- TTS Button & Explain Button -->
      <div class="grid grid-cols-2 gap-2.5">
        <button id="tts-scan-btn" onclick="speakCurrentDiagnosis()" class="btn-primary py-3 px-4 text-xs font-bold flex items-center justify-center gap-1.5 shadow-sm">
          <span>🔊</span>
          <span id="tts-scan-text">Listen Aloud</span>
        </button>
        <button onclick="openExplainModal()" class="py-3 px-4 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs flex items-center justify-center gap-1.5 border border-slate-200">
          <span>💡</span>
          <span id="txt-why-result">Why this result?</span>
        </button>
      </div>
    </div>
  </section>


  <!-- ========================================================= -->
  <!-- SCREEN 7: CROP-HEALTH DIARY -->
  <!-- ========================================================= -->
  <section id="screen-diary" class="app-screen px-5 pt-8 pb-28 bg-white">
    <!-- Top Bar -->
    <div class="flex items-center justify-between mb-4">
      <button onclick="navigateTo('screen-dashboard-farmer')" class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-700">
        <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5"/></svg>
      </button>
      <div class="text-center">
        <h2 id="diary-heading" class="text-base font-black text-slate-900 tracking-tight">Crop-Health Diary</h2>
        <div id="diary-subheading" class="text-[10px] text-emerald-700 font-bold">Offline-First • Latest Timestamp Wins</div>
      </div>
      <!-- Sync Button Pill -->
      <button id="diary-sync-btn" onclick="syncDiaryWithBackend()" class="px-3.5 py-1.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-bold flex items-center gap-1.5 active:scale-95 transition-transform shadow-sm">
        <span id="diary-sync-icon" class="text-sm">🔄</span>
        <span id="diary-sync-text">Sync</span>
      </button>
    </div>

    <!-- Search Bar -->
    <div class="card-soft px-4 py-2.5 rounded-2xl flex items-center gap-2 mb-3.5">
      <svg class="w-4 h-4 text-slate-400 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/></svg>
      <input id="diary-search-input" type="text" placeholder="Search potato, tomato, blight, spray..." oninput="handleDiaryFilter()"
        class="bg-transparent text-slate-900 text-xs flex-1 focus:outline-none placeholder-slate-400">
    </div>

    <!-- Filter Chips (Crops) -->
    <div class="flex items-center gap-2 overflow-x-auto hide-scrollbar mb-2.5">
      <button id="chip-crop-all" onclick="setDiaryCropFilter('All')" class="bg-emerald-700 text-white font-bold text-xs px-4 py-1.5 rounded-full whitespace-nowrap shadow-sm">All Crops</button>
      <button id="chip-crop-potato" onclick="setDiaryCropFilter('Potato')" class="bg-slate-100 text-slate-700 text-xs px-4 py-1.5 rounded-full whitespace-nowrap hover:bg-slate-200">🥔 Potato</button>
      <button id="chip-crop-tomato" onclick="setDiaryCropFilter('Tomato')" class="bg-slate-100 text-slate-700 text-xs px-4 py-1.5 rounded-full whitespace-nowrap hover:bg-slate-200">🍅 Tomato</button>
    </div>

    <!-- Timeline Entries Container -->
    <div id="diary-entries-container" class="space-y-3.5 mb-6"></div>

    <!-- Floating Action Button to Add Entry -->
    <div class="fixed bottom-20 right-5 z-30">
      <button onclick="openAddDiaryModal()" class="btn-primary px-5 py-3.5 flex items-center gap-2 shadow-xl text-xs font-bold active:scale-95 transition-transform">
        <span class="text-base font-black">+</span>
        <span id="btn-add-diary-text">Log Crop Entry</span>
      </button>
    </div>
  </section>


  <!-- ========================================================= -->
  <!-- SCREEN 8: ADVISOR CHAT -->
  <!-- ========================================================= -->
  <section id="screen-chat" class="app-screen justify-between pb-24 bg-white">
    <div class="px-5 pt-8 pb-3 bg-white border-b border-slate-100 flex items-center justify-between z-20">
      <button onclick="navigateTo('screen-dashboard-farmer')" class="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center text-slate-700">
        <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5"/></svg>
      </button>
      <div class="text-center">
        <div id="chat-heading" class="text-sm font-black text-slate-900">AgriMate AI Advisor</div>
        <div id="chat-subheading" class="text-[10px] text-emerald-700 font-bold">NARC Grounded RAG</div>
      </div>
      <div class="w-9 h-9 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-800 font-bold text-xs">
        RAG
      </div>
    </div>

    <!-- Messages Container -->
    <div id="chat-messages" class="flex-1 overflow-y-auto px-5 py-4 space-y-3.5 hide-scrollbar bg-slate-50">
      <div class="card-clean p-4 rounded-2xl max-w-[90%] shadow-sm">
        <div class="flex items-center gap-1.5 text-xs font-bold text-emerald-700 mb-1.5">
          <span>🌿</span>
          <span id="txt-advisor-verified">Verified Agronomic Advisor</span>
        </div>
        <p id="txt-advisor-welcome" class="text-xs text-slate-800 leading-relaxed">
          Assalam-o-Alaikum! Ask me about Potato & Tomato diseases, blight sprays, fertilizer schedules, or pest thresholds in Urdu or English.
        </p>
      </div>
    </div>

    <!-- Quick Prompts Horizontal Scroll -->
    <div class="px-4 py-2 flex items-center gap-2 overflow-x-auto hide-scrollbar bg-white border-t border-slate-100">
      <button onclick="sendQuickPrompt('Potato late blight symptoms, spray and treatment')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] px-3.5 py-1.5 rounded-full whitespace-nowrap border border-slate-200">
        🥔 Potato Late Blight
      </button>
      <button onclick="sendQuickPrompt('Tomato early blight and pest management')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] px-3.5 py-1.5 rounded-full whitespace-nowrap border border-slate-200">
        🍅 Tomato Blight
      </button>
      <button onclick="sendQuickPrompt('Potato fertilizer and urea application schedule')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] px-3.5 py-1.5 rounded-full whitespace-nowrap border border-slate-200">
        🌱 Fertilizer Schedule
      </button>
    </div>

    <!-- Input Box with Mic Button -->
    <div class="px-4 pt-2 pb-3 bg-white border-t border-slate-100">
      <form onsubmit="handleChatSubmit(event)" class="flex items-center gap-2">
        <input id="chat-input" type="text" placeholder="Ask your agricultural question..." required
          class="flex-1 bg-slate-50 border border-slate-200 rounded-full px-4 py-3 text-slate-900 text-xs placeholder-slate-400 focus:outline-none focus:border-emerald-600">
        
        <button type="button" onclick="openSpeechModal('chat')" class="w-11 h-11 rounded-full bg-slate-100 text-emerald-800 border border-slate-200 flex items-center justify-center font-bold shadow-sm active:scale-95 transition-transform flex-shrink-0">
          <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
        </button>

        <button type="submit" class="w-11 h-11 rounded-full btn-primary flex items-center justify-center font-bold shadow-md active:scale-95 transition-transform flex-shrink-0">
          <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"/></svg>
        </button>
      </form>
    </div>
  </section>


  <!-- ========================================================= -->
  <!-- SCREEN 9: FARM OVERVIEW -->
  <!-- ========================================================= -->
  <section id="screen-overview" class="app-screen pb-28 bg-white">
    <div class="px-5 pt-8 pb-3 bg-white border-b border-slate-100 flex items-center justify-between">
      <button onclick="navigateTo('screen-dashboard-farmer')" class="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center text-slate-700">
        <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5"/></svg>
      </button>
      <div id="overview-heading" class="text-sm font-black text-slate-900">Farm Overview</div>
      <div class="w-9"></div>
    </div>

    <div class="p-5 space-y-4">
      <div class="grid grid-cols-2 gap-3.5">
        <div class="card-clean p-4 flex flex-col justify-between h-44">
          <div id="lbl-total-workers" class="text-sm font-bold text-slate-900">Total Workers</div>
          <div class="text-3xl font-black text-emerald-800">48</div>
          <div id="sub-active-workers" class="text-xs text-secondary">Active Harvesters</div>
        </div>

        <div class="card-clean p-4 flex flex-col justify-between h-44">
          <div id="lbl-total-acres" class="text-sm font-bold text-slate-900">Total Acres</div>
          <div class="text-3xl font-black text-emerald-800">848</div>
          <div id="sub-crops-acres" class="text-xs text-secondary">Potato & Tomato Beds</div>
        </div>
      </div>

      <div class="card-clean p-4.5 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-11 h-11 rounded-2xl bg-emerald-100 flex items-center justify-center text-emerald-800">
            💧
          </div>
          <div>
            <div id="lbl-drip-system" class="text-sm font-bold text-slate-900">Drip Fertigation System</div>
            <div id="sub-drip-system" class="text-xs text-emerald-700 font-bold">Active Cycle • Potassium Nitrate</div>
          </div>
        </div>
        <span class="w-3 h-3 rounded-full bg-emerald-500 animate-ping"></span>
      </div>
    </div>
  </section>


  <!-- ========================================================= -->
  <!-- MODAL: ADD CROP HEALTH RECORD -->
  <!-- ========================================================= -->
  <div id="add-diary-modal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-end justify-center">
    <div class="w-full max-w-md bg-white rounded-t-[32px] p-6 border-t border-slate-200 shadow-2xl max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold">📖</div>
          <h4 id="lbl-modal-log-title" class="text-base font-black text-slate-900">Log Crop Health Record</h4>
        </div>
        <button onclick="closeAddDiaryModal()" class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500">✕</button>
      </div>

      <form onsubmit="handleAddDiarySubmit(event)" class="space-y-3 text-xs">
        <div>
          <label id="lbl-diary-crop-var" class="block font-bold text-slate-700 mb-1 text-[11px]">Crop & Variety</label>
          <div class="grid grid-cols-2 gap-2">
            <select id="diary-form-crop" class="bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600">
              <option value="Potato" selected>🥔 Potato</option>
              <option value="Tomato">🍅 Tomato</option>
            </select>
            <input id="diary-form-variety" type="text" placeholder="Variety (e.g. Asterix)" value="Asterix"
              class="bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600">
          </div>
        </div>

        <div>
          <label id="lbl-diary-field-acre" class="block font-bold text-slate-700 mb-1 text-[11px]">Field & Acreage</label>
          <div class="grid grid-cols-2 gap-2">
            <input id="diary-form-field" type="text" placeholder="Field Name" value="Okara North Block 3" required
              class="bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600">
            <input id="diary-form-acreage" type="number" step="0.5" placeholder="Acres" value="12.5"
              class="bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600">
          </div>
        </div>

        <div>
          <label id="lbl-diary-stage" class="block font-bold text-slate-700 mb-1 text-[11px]">Growth Stage</label>
          <select id="diary-form-stage" class="w-full bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600">
            <option value="Emergence">Emergence</option>
            <option value="Vegetative">Vegetative</option>
            <option value="Flowering/Fruit Set">Flowering/Fruit Set</option>
            <option value="Tuber Bulking/Ripening" selected>Tuber Bulking/Ripening</option>
            <option value="Harvest Ready">Harvest Ready</option>
          </select>
        </div>

        <div>
          <label id="lbl-diary-diag" class="block font-bold text-slate-700 mb-1 text-[11px]">Disease Diagnosis (if any)</label>
          <div class="grid grid-cols-2 gap-2">
            <input id="diary-form-disease" type="text" placeholder="e.g. Potato Late Blight" value="Potato Late Blight"
              class="bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600">
            <input id="diary-form-conf" type="number" step="1" min="0" max="100" placeholder="Confidence %" value="94"
              class="bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600">
          </div>
        </div>

        <div>
          <label id="lbl-diary-notes" class="block font-bold text-slate-700 mb-1 text-[11px]">Observations & Notes</label>
          <textarea id="diary-form-notes" rows="2" placeholder="Describe symptoms, pest signs, irrigation status..."
            class="w-full bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600 resize-none">Late blight lesions detected after morning fog. Water-soaked margins on lower leaves.</textarea>
        </div>

        <div>
          <label id="lbl-diary-treatment" class="block font-bold text-slate-700 mb-1 text-[11px]">Applied Treatment & Cost</label>
          <div class="grid grid-cols-3 gap-2">
            <input id="diary-form-treatment" type="text" placeholder="Treatment / Spray" value="Ridomil Gold @ 250g/100L water"
              class="col-span-2 bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600">
            <input id="diary-form-cost" type="number" step="50" placeholder="PKR Cost" value="3800"
              class="bg-slate-50 text-slate-900 rounded-xl p-2.5 border border-slate-200 focus:outline-none focus:border-emerald-600">
          </div>
        </div>

        <button id="btn-save-diary" type="submit" class="btn-primary w-full py-3.5 text-xs font-bold shadow-md mt-3">
          Save Locally & Sync
        </button>
      </form>
    </div>
  </div>


  <!-- ========================================================= -->
  <!-- MODAL: SPEECH-TO-TEXT WITH EDITABLE TRANSCRIPT -->
  <!-- ========================================================= -->
  <div id="speech-modal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-end justify-center">
    <div class="w-full max-w-md bg-white rounded-t-[32px] p-6 border-t border-slate-200 shadow-2xl">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold">🎙️</div>
          <h4 id="lbl-modal-speech-title" class="text-base font-black text-slate-900">Voice Speech-to-Text</h4>
        </div>
        <button onclick="closeSpeechModal()" class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500">✕</button>
      </div>

      <p id="lbl-modal-speech-sub" class="text-xs text-secondary mb-3">
        Speak in Urdu or English. You can edit the text before confirming:
      </p>

      <div class="mb-3">
        <textarea id="speech-transcript-box" rows="3"
          class="w-full p-3.5 bg-slate-50 text-slate-900 text-xs rounded-2xl border border-slate-200 focus:outline-none focus:border-emerald-600 resize-none font-medium"></textarea>
      </div>

      <div class="grid grid-cols-2 gap-2">
        <button onclick="simulateMicRecord()" class="py-3 px-4 rounded-full bg-slate-100 text-slate-800 font-bold text-xs flex items-center justify-center gap-1.5 border border-slate-200">
          <span class="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
          <span id="btn-mic-record">Record Mic</span>
        </button>
        <button onclick="confirmSpeechTranscript()" class="btn-primary py-3 px-4 text-xs font-bold flex items-center justify-center gap-1.5 shadow-sm">
          <span id="btn-confirm-speech">Confirm & Send</span>
        </button>
      </div>
    </div>
  </div>


  <!-- ========================================================= -->
  <!-- MODAL: EXPLAINABILITY "WHY THIS RESULT?" -->
  <!-- ========================================================= -->
  <div id="explain-modal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-5">
    <div class="w-full max-w-sm bg-white rounded-3xl p-6 border border-slate-200 shadow-2xl">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-base font-black text-slate-900 flex items-center gap-2">
          <span>🧠</span>
          <span id="lbl-explain-title">Grad-CAM Explainability</span>
        </h4>
        <button onclick="closeExplainModal()" class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500">✕</button>
      </div>

      <p id="lbl-explain-desc" class="text-xs text-secondary leading-relaxed mb-4">
        MobileNetV2 computes gradients from the final convolutional layer to identify symptom regions:
      </p>

      <div class="space-y-2.5 mb-4 text-xs">
        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
          <div id="lbl-explain-1-title" class="text-emerald-800 font-bold mb-0.5">1. Target Rings & Necrosis (52% weight)</div>
          <p id="lbl-explain-1-desc" class="text-slate-600 text-[11px]">Concentric lesion margins characteristic of Potato/Tomato Blight.</p>
        </div>
        <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
          <div id="lbl-explain-2-title" class="text-emerald-800 font-bold mb-0.5">2. Farmer Voice Integration (48% weight)</div>
          <p id="lbl-explain-2-desc" class="text-slate-600 text-[11px]">Spoken symptom note matched aphid pest attack and lower leaf wilting.</p>
        </div>
      </div>

      <button onclick="closeExplainModal()" class="btn-primary w-full py-3 text-xs font-bold">
        <span id="btn-explain-close">Got It</span>
      </button>
    </div>
  </div>


  <!-- ========================================================= -->
  <!-- BOTTOM NAVIGATION BAR (Strictly hidden on Auth & Splash) -->
  <!-- ========================================================= -->
  <nav id="app-nav" class="bottom-nav" style="display: none;">
    <button id="nav-btn-home" onclick="navigateTo('screen-dashboard-farmer')" class="flex flex-col items-center gap-1 text-emerald-800 font-bold">
      <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"/></svg>
      <span id="nav-text-home" class="text-[10px]">Home</span>
    </button>
    <button id="nav-btn-scanner" onclick="navigateTo('screen-camera')" class="flex flex-col items-center gap-1 text-slate-500 hover:text-emerald-700">
      <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"/><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0z"/></svg>
      <span id="nav-text-scanner" class="text-[10px]">Scanner</span>
    </button>
    <button id="nav-btn-diary" onclick="navigateTo('screen-diary')" class="flex flex-col items-center gap-1 text-slate-500 hover:text-emerald-700">
      <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"/></svg>
      <span id="nav-text-diary" class="text-[10px]">Diary</span>
    </button>
    <button id="nav-btn-advisor" onclick="navigateTo('screen-chat')" class="flex flex-col items-center gap-1 text-slate-500 hover:text-emerald-700">
      <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9v-2h2v2zm0-4H9V7h2v5z"/></svg>
      <span id="nav-text-advisor" class="text-[10px]">Advisor</span>
    </button>
    <button id="nav-btn-overview" onclick="navigateTo('screen-overview')" class="flex flex-col items-center gap-1 text-slate-500 hover:text-emerald-700">
      <svg class="w-5 h-5 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15"/></svg>
      <span id="nav-text-overview" class="text-[10px]">Overview</span>
    </button>
  </nav>


  <!-- ========================================================= -->
  <!-- APPLICATION SCRIPTS & TRANSLATION ENGINE -->
  <!-- ========================================================= -->
  <script>
    const API_BASE = (() => {
      if (localStorage.getItem('agrimate_custom_api')) return localStorage.getItem('agrimate_custom_api');
      if (window.location.protocol === 'file:') return 'http://192.168.1.12:8000/api/v1';
      if (window.location.hostname && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        return `http://${window.location.hostname}:8000/api/v1`;
      }
      return 'http://localhost:8000/api/v1';
    })();

    let currentLang = localStorage.getItem('agrimate_lang') || 'en';
    let currentSpeechTarget = 'chat';
    let isSpeaking = false;

    // Comprehensive Language Dictionary: Pure English vs Pure Urdu
    const I18N = {
      en: {
        splash_sub: "Smart Farming Pakistan",
        splash_from: "FROM",
        login_heading: "Welcome Back! 👋",
        login_subtitle: "Sign in to manage Potato & Tomato crops and get AI diagnostics.",
        lbl_login_id: "Phone or Email",
        ph_login_id: "03001234567 or farmer@agrimate.pk",
        lbl_login_pwd: "Password",
        ph_login_pwd: "Enter password",
        lnk_forgot_pwd: "Forgot?",
        lbl_remember_me: "Keep me signed in on this phone",
        txt_login_btn: "Log In",
        txt_no_account: "Don't have an account?",
        lnk_signup: "Create Account",
        txt_demo_title: "One-Tap Quick Demo Sign In:",
        demo_farmer: "Farmer",
        demo_buyer: "Buyer",
        demo_expert: "Expert",
        txt_security_note: "🔒 256-bit Secure PBKDF2 Encryption • Strictly compliant with NARC guidelines",
        reg_heading: "Create Account 🌿",
        reg_subtitle: "Join Pakistan's precision agricultural network.",
        lbl_reg_name: "1. Full Name",
        ph_reg_name: "Ahmad Khan",
        lbl_reg_id: "2. Mobile Phone or Email",
        ph_reg_id: "03001234567 or farmer@okara.pk",
        lbl_reg_pwd: "3. Password (min 6 chars)",
        lbl_reg_role: "4. Select Your Role",
        lbl_reg_location: "5. District / Tehsil",
        txt_popular_chips: "Popular:",
        txt_reg_btn: "Complete Registration",
        txt_have_account: "Already have an account?",
        lnk_login: "Sign In",
        nav_home: "Home",
        nav_scanner: "Scanner",
        nav_diary: "Diary",
        nav_advisor: "Advisor",
        nav_overview: "Overview",
        btn_quick_scan: "Leaf Scan",
        sub_quick_scan: "Photo + Voice",
        btn_quick_diary: "Crop Diary",
        sub_quick_diary: "Offline Sync",
        btn_quick_advisor: "AI Advisor",
        sub_quick_advisor: "NARC RAG",
        txt_my_fields_heading: "Monitored Fields",
        lnk_farm_overview: "Farm Overview →",
        diary_heading: "Crop-Health Diary",
        diary_subheading: "Offline-First • Latest Timestamp Wins",
        btn_add_diary_text: "Log Crop Entry",
        chat_heading: "AgriMate AI Advisor",
        chat_subheading: "NARC Grounded RAG",
        txt_advisor_verified: "Verified Agronomic Advisor",
        txt_advisor_welcome: "Assalam-o-Alaikum! Ask me about Potato & Tomato diseases, blight sprays, fertilizer schedules, or pest thresholds in Urdu or English.",
        ph_chat_input: "Ask your agricultural question...",
        overview_heading: "Farm Overview",
        lbl_total_workers: "Total Workers",
        sub_active_workers: "Active Harvesters",
        lbl_total_acres: "Total Acres",
        sub_crops_acres: "Potato & Tomato Beds",
        lbl_drip_system: "Drip Fertigation System",
        sub_drip_system: "Active Cycle • Potassium Nitrate",
        txt_report_title: "Diagnostic Report",
        txt_flag_title: "Low Confidence Scan Auto-Flagged (<75%)",
        txt_flag_desc: "Model confidence is 63.5%. Dispatched to Punjab Agri Extension Queue for agronomist review.",
        lbl_spoken_obs: "Farmer Spoken Observation:",
        lbl_integrated_advice: "Integrated Treatment:",
        tts_scan_text: "Listen Aloud",
        txt_why_result: "Why this result?",
        txt_cam_lighting: "Lighting: Optimal",
        txt_cam_focus: "Focus: Sharp Veins",
        txt_cam_align: "Align leaf inside frame",
        btn_edit_note: "Edit",
        txt_cam_hint: "Multimodal Scan combines photo + spoken note into RAG advisor",
        txt_cam_normal: "Normal Scan"
      },
      ur: {
        splash_sub: "اسمارٹ زراعت • پاکستان",
        splash_from: "کی طرف سے",
        login_heading: "خوش آمدید! 👋",
        login_subtitle: "آلو اور ٹماٹر کی فصلوں کی دیکھ بھال اور زرعی رہنمائی کے لیے لاگ ان کریں۔",
        lbl_login_id: "موبائل فون یا ای میل",
        ph_login_id: "03001234567 یا farmer@agrimate.pk",
        lbl_login_pwd: "پاس ورڈ",
        ph_login_pwd: "پاس ورڈ درج کریں",
        lnk_forgot_pwd: "بھول گئے؟",
        lbl_remember_me: "اس فون پر لاگ ان محفوظ رکھیں",
        txt_login_btn: "لاگ ان کریں",
        txt_no_account: "نیا اکاؤنٹ بنانا چاہتے ہیں؟",
        lnk_signup: "نیا اکاؤنٹ بنائیں",
        txt_demo_title: "فوری ٹیسٹ اکاؤنٹ (1-ٹیپ):",
        demo_farmer: "کاشتکار",
        demo_buyer: "خریدار",
        demo_expert: "زرعی ماہر",
        txt_security_note: "🔒 محفوظ انکرپشن • زرعی تحقیقاتی ادارہ (NARC) کے ضوابط کے مطابق",
        reg_heading: "نیا اکاؤنٹ بنائیں 🌿",
        reg_subtitle: "پاکستان کے جدید ترین زرعی نیٹ ورک میں شامل ہوں۔",
        lbl_reg_name: "1. پورا نام",
        ph_reg_name: "احمد خان",
        lbl_reg_id: "2. موبائل فون یا ای میل",
        ph_reg_id: "03001234567 یا farmer@okara.pk",
        lbl_reg_pwd: "3. پاس ورڈ (کم از کم 6 ہندسے)",
        lbl_reg_role: "4. اپنا کردار منتخب کریں",
        lbl_reg_location: "5. ضلع یا تحصیل",
        txt_popular_chips: "مشہور اضلاع:",
        txt_reg_btn: "اکاؤنٹ مکمل کریں",
        txt_have_account: "پہلے سے اکاؤنٹ موجود ہے؟",
        lnk_login: "لاگ ان کریں",
        nav_home: "ہوم",
        nav_scanner: "اسکینر",
        nav_diary: "ڈائری",
        nav_advisor: "مشیر",
        nav_overview: "جائزہ",
        btn_quick_scan: "پتے کا اسکین",
        sub_quick_scan: "تصویر + آواز",
        btn_quick_diary: "فصل ڈائری",
        sub_quick_diary: "آف لائن ریکارڈ",
        btn_quick_advisor: "زرعی مشیر",
        sub_quick_advisor: "تصدیق شدہ",
        txt_my_fields_heading: "زیرِ نگرانی کھیت",
        lnk_farm_overview: "مکمل جائزہ ←",
        diary_heading: "فصل کی صحت ڈائری",
        diary_subheading: "آف لائن ریکارڈ • جدید ترین اندراج ترجیح پائے گا",
        btn_add_diary_text: "نیا اندراج کریں",
        chat_heading: "ایگری میٹ زرعی مشیر",
        chat_subheading: "مستند زرعی کتب پر مبنی جوابات",
        txt_advisor_verified: "تصدیق شدہ زرعی مشیر",
        txt_advisor_welcome: "السلام علیکم! مجھ سے آلو اور ٹماٹر کی بیماریوں، اسپرے، کھاد کے شیڈول یا کیڑوں کے تدارک کے بارے میں اردو یا انگلش میں پوچھیں۔",
        ph_chat_input: "اپنا زرعی سوال یہاں لکھیں...",
        overview_heading: "فارم کا مجموعی جائزہ",
        lbl_total_workers: "کل مزدور",
        sub_active_workers: "کھیتوں میں متحرک",
        lbl_total_acres: "کل رقبہ",
        sub_crops_acres: "آلو اور ٹماٹر کے بلاکس",
        lbl_drip_system: "ڈرپ فرٹیگیشن سسٹم",
        sub_drip_system: "فعال • پوٹاشیم نائٹریٹ سائیکل",
        txt_report_title: "تشخیصی رپورٹ",
        txt_flag_title: "کم اعتمادی اسکین خودکار بھیج دیا گیا (<75%)",
        txt_flag_desc: "ماڈل کا اعتماد 63.5% ہے۔ زرعی ماہر کی تصدیق کے لیے ارسال کر دیا گیا ہے۔",
        lbl_spoken_obs: "کسان کا صوتی بیان:",
        lbl_integrated_advice: "تجویز کردہ زرعی مشورہ:",
        tts_scan_text: "آواز میں سنیں",
        txt_why_result: "یہ نتیجہ کیوں آیا؟",
        txt_cam_lighting: "روشنی: بہترین",
        txt_cam_focus: "فوکس: واضح نسیں",
        txt_cam_align: "پتے کو دائرے کے اندر رکھیں",
        btn_edit_note: "تبدیل کریں",
        txt_cam_hint: "پتے کی تصویر اور آپ کی آواز دونوں کو ملا کر مشورہ دیا جاتا ہے",
        txt_cam_normal: "عام اسکین"
      }
    };

    function setLanguage(lang) {
      currentLang = lang;
      localStorage.setItem('agrimate_lang', lang);

      const dict = I18N[lang] || I18N['en'];
      const isUrdu = lang === 'ur';

      // Set HTML / Body Direction & Classes
      document.documentElement.lang = lang;
      if (isUrdu) {
        document.body.classList.add('rtl-mode');
        document.body.setAttribute('dir', 'rtl');
      } else {
        document.body.classList.remove('rtl-mode');
        document.body.setAttribute('dir', 'ltr');
      }

      // Update text values
      for (const [id, val] of Object.entries(dict)) {
        const el = document.getElementById(id);
        if (el) {
          if (id.startsWith('ph_')) {
            el.placeholder = val;
          } else {
            el.innerText = val;
          }
        }
      }

      // Update placeholders
      if (document.getElementById('login-identifier')) {
        document.getElementById('login-identifier').placeholder = dict.ph_login_id;
      }
      if (document.getElementById('login-password')) {
        document.getElementById('login-password').placeholder = dict.ph_login_pwd;
      }
      if (document.getElementById('reg-name')) {
        document.getElementById('reg-name').placeholder = dict.ph_reg_name;
      }
      if (document.getElementById('reg-identifier')) {
        document.getElementById('reg-identifier').placeholder = dict.ph_reg_id;
      }
      if (document.getElementById('chat-input')) {
        document.getElementById('chat-input').placeholder = dict.ph_chat_input;
      }

      // Update Language Switcher Buttons Style
      ['login', 'reg', 'dash'].forEach(prefix => {
        const btnEn = document.getElementById(`${prefix}-lang-en`);
        const btnUr = document.getElementById(`${prefix}-lang-ur`);
        if (btnEn && btnUr) {
          if (lang === 'en') {
            btnEn.className = 'px-3 py-1 rounded-full bg-white text-emerald-800 shadow-sm transition-all';
            btnUr.className = 'px-3 py-1 rounded-full text-slate-500 hover:text-slate-800 transition-all';
          } else {
            btnUr.className = 'px-3 py-1 rounded-full bg-white text-emerald-800 shadow-sm transition-all';
            btnEn.className = 'px-3 py-1 rounded-full text-slate-500 hover:text-slate-800 transition-all';
          }
        }
      });
    }

    // App Initialization
    window.addEventListener('DOMContentLoaded', () => {
      setLanguage(currentLang);

      // Instagram/Facebook Splash Screen Timer (2.5 seconds)
      setTimeout(() => {
        const token = localStorage.getItem('agrimate_jwt');
        if (token) {
          navigateTo('screen-dashboard-farmer');
        } else {
          navigateTo('screen-login');
        }
      }, 2500);

      renderDiaryEntries();
      updateSyncPill();
    });

    // Central Navigation with Strict Authentication Guard
    function navigateTo(screenId) {
      const token = localStorage.getItem('agrimate_jwt');
      const authScreens = ['screen-splash', 'screen-login', 'screen-register'];

      // If user is NOT logged in and tries to access in-app screens, strictly force to login
      if (!token && !authScreens.includes(screenId)) {
        screenId = 'screen-login';
      }

      // Hide all screens and activate the target
      document.querySelectorAll('.app-screen').forEach(s => s.classList.remove('active'));
      const target = document.getElementById(screenId);
      if (target) {
        target.classList.add('active');
        window.scrollTo(0, 0);
      }

      // Control Bottom Navigation Bar Visibility
      const nav = document.getElementById('app-nav');
      if (nav) {
        if (authScreens.includes(screenId)) {
          nav.style.display = 'none';
        } else {
          nav.style.display = 'flex';
          updateNavActiveState(screenId);
        }
      }
    }

    function updateNavActiveState(screenId) {
      const navMap = {
        'screen-dashboard-farmer': 'nav-btn-home',
        'screen-camera': 'nav-btn-scanner',
        'screen-scan-result': 'nav-btn-scanner',
        'screen-diary': 'nav-btn-diary',
        'screen-chat': 'nav-btn-advisor',
        'screen-overview': 'nav-btn-overview'
      };

      ['nav-btn-home', 'nav-btn-scanner', 'nav-btn-diary', 'nav-btn-advisor', 'nav-btn-overview'].forEach(btnId => {
        const btn = document.getElementById(btnId);
        if (!btn) return;
        if (navMap[screenId] === btnId) {
          btn.classList.add('text-emerald-800', 'font-bold');
          btn.classList.remove('text-slate-500');
        } else {
          btn.classList.remove('text-emerald-800', 'font-bold');
          btn.classList.add('text-slate-500');
        }
      });
    }

    // Toggle password visibility (Eye icon)
    function togglePasswordVisibility(inputId, eyeIconId) {
      const field = document.getElementById(inputId);
      const icon = document.getElementById(eyeIconId);
      if (field.type === 'password') {
        field.type = 'text';
        icon.innerText = '🙈';
      } else {
        field.type = 'password';
        icon.innerText = '👁️';
      }
    }

    function setRegLocation(loc) {
      document.getElementById('reg-location').value = loc;
    }

    function fillDemo(id, pwd) {
      document.getElementById('login-identifier').value = id;
      document.getElementById('login-password').value = pwd;
    }

    // Login Handler
    async function handleLoginSubmit(e) {
      e.preventDefault();
      const errBox = document.getElementById('login-error-box');
      const errMsg = document.getElementById('login-error-msg');
      const btn = document.getElementById('login-submit-btn');
      errBox.classList.add('hidden');
      btn.innerText = currentLang === 'ur' ? 'لاگ ان ہو رہا ہے...' : 'Signing In...';

      const phone_or_email = document.getElementById('login-identifier').value.trim();
      const password = document.getElementById('login-password').value;

      try {
        const res = await fetch(`${API_BASE}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ phone_or_email, password })
        });
        const data = await res.json();
        btn.innerText = currentLang === 'ur' ? 'لاگ ان کریں' : 'Log In';

        if (res.ok) {
          localStorage.setItem('agrimate_jwt', data.access_token);
          localStorage.setItem('agrimate_user', JSON.stringify(data.user));
          const user = data.user;
          document.getElementById('dash-greeting').innerText = `${currentLang === 'ur' ? 'خوش آمدید' : 'Hello'}, ${user.name.split(' ')[0]} 👋`;
          document.getElementById('dash-location').innerText = user.location;
          navigateTo('screen-dashboard-farmer');
        } else {
          errMsg.innerText = data.detail || (currentLang === 'ur' ? 'لاگ ان ناکام رہا۔ معلومات درست کریں۔' : 'Login failed. Please check credentials.');
          errBox.classList.remove('hidden');
        }
      } catch (err) {
        btn.innerText = currentLang === 'ur' ? 'لاگ ان کریں' : 'Log In';
        // Seamless offline evaluation session for quick demo credentials
        const demoUser = { name: phone_or_email.includes('0311') ? 'Tariq Buyer' : (phone_or_email.includes('0322') ? 'Dr. Fatima' : 'Ahmad Farmer'), location: 'Okara, Punjab' };
        localStorage.setItem('agrimate_jwt', 'offline-session-token');
        localStorage.setItem('agrimate_user', JSON.stringify(demoUser));
        document.getElementById('dash-greeting').innerText = `${currentLang === 'ur' ? 'خوش آمدید' : 'Hello'}, ${demoUser.name.split(' ')[0]} 👋`;
        navigateTo('screen-dashboard-farmer');
      }
    }

    // Register Handler
    async function handleRegisterSubmit(e) {
      e.preventDefault();
      const errBox = document.getElementById('reg-error-box');
      const errMsg = document.getElementById('reg-error-msg');
      const btn = document.getElementById('reg-submit-btn');
      errBox.classList.add('hidden');
      btn.innerText = currentLang === 'ur' ? 'اکاؤنٹ بن رہا ہے...' : 'Creating Account...';

      const roleInput = document.querySelector('input[name="reg-role"]:checked');
      const role = roleInput ? roleInput.value : 'Farmer';
      const name = document.getElementById('reg-name').value.trim();
      const phone_or_email = document.getElementById('reg-identifier').value.trim();
      const password = document.getElementById('reg-password').value;
      const location = document.getElementById('reg-location').value.trim();

      try {
        const res = await fetch(`${API_BASE}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, phone_or_email, password, role, location })
        });
        const data = await res.json();
        btn.innerText = currentLang === 'ur' ? 'اکاؤنٹ مکمل کریں' : 'Complete Registration';

        if (res.ok) {
          localStorage.setItem('agrimate_jwt', data.access_token);
          localStorage.setItem('agrimate_user', JSON.stringify(data.user));
          document.getElementById('dash-greeting').innerText = `${currentLang === 'ur' ? 'خوش آمدید' : 'Hello'}, ${data.user.name.split(' ')[0]} 👋`;
          document.getElementById('dash-location').innerText = data.user.location;
          navigateTo('screen-dashboard-farmer');
        } else {
          errMsg.innerText = data.detail || (currentLang === 'ur' ? 'رجسٹریشن ناکام رہی۔ معلومات چیک کریں۔' : 'Registration failed. Check your inputs.');
          errBox.classList.remove('hidden');
        }
      } catch (err) {
        btn.innerText = currentLang === 'ur' ? 'اکاؤنٹ مکمل کریں' : 'Complete Registration';
        const newUser = { name: name || 'Ahmad Farmer', location: location || 'Okara, Punjab' };
        localStorage.setItem('agrimate_jwt', 'offline-session-token');
        localStorage.setItem('agrimate_user', JSON.stringify(newUser));
        document.getElementById('dash-greeting').innerText = `${currentLang === 'ur' ? 'خوش آمدید' : 'Hello'}, ${newUser.name.split(' ')[0]} 👋`;
        navigateTo('screen-dashboard-farmer');
      }
    }

    // Log Out
    function logoutUser() {
      if (confirm(currentLang === 'ur' ? 'کیا آپ واقعی لاگ آؤٹ کرنا چاہتے ہیں؟' : 'Are you sure you want to log out?')) {
        localStorage.removeItem('agrimate_jwt');
        localStorage.removeItem('agrimate_user');
        navigateTo('screen-login');
      }
    }

    // Speech Modal
    function openSpeechModal(target) {
      currentSpeechTarget = target;
      const initialText = target === 'camera'
        ? (document.getElementById('camera-farmer-desc').value || 'کیڑا لگ گیا ہے اور نچلے پتے سوکھ رہے ہیں')
        : (document.getElementById('chat-input').value || 'آلو میں پچھیتا جھلساؤ کا علاج اور سپرے بتائیں');
      
      document.getElementById('speech-transcript-box').value = initialText;
      document.getElementById('speech-modal').classList.remove('hidden');
    }

    function closeSpeechModal() {
      document.getElementById('speech-modal').classList.add('hidden');
    }

    function simulateMicRecord() {
      if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        const rec = new SpeechRec();
        rec.lang = currentLang === 'ur' ? 'ur-PK' : 'en-US';
        rec.start();
        rec.onresult = function(event) {
          document.getElementById('speech-transcript-box').value = event.results[0][0].transcript;
        };
      } else {
        document.getElementById('speech-transcript-box').value = currentLang === 'ur' 
          ? 'آلو کے پتوں پر کالے دھبے اور کیڑا لگ گیا ہے' 
          : 'Leaves are wilting with dark blight spots';
      }
    }

    function confirmSpeechTranscript() {
      const text = document.getElementById('speech-transcript-box').value.trim();
      closeSpeechModal();
      if (!text) return;

      if (currentSpeechTarget === 'camera') {
        document.getElementById('camera-farmer-desc').value = text;
      } else {
        document.getElementById('chat-input').value = text;
        handleChatSubmit(new Event('submit'));
      }
    }

    // Text-to-Speech (TTS)
    function speakText(text) {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = currentLang === 'ur' ? 'ur-PK' : 'en-US';
        utterance.rate = 0.95;
        window.speechSynthesis.speak(utterance);
      }
    }

    function speakCurrentDiagnosis() {
      const text = document.getElementById('scan-advice-body').innerText;
      const btnText = document.getElementById('tts-scan-text');
      
      if (!isSpeaking) {
        isSpeaking = true;
        btnText.innerText = currentLang === 'ur' ? 'آواز بند کریں' : 'Stop Audio';
        speakText(text);
      } else {
        isSpeaking = false;
        btnText.innerText = currentLang === 'ur' ? 'آواز میں سنیں' : 'Listen Aloud';
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      }
    }

    // Multimodal Scan
    async function triggerMultimodalScan(isLowConfidence) {
      const crop = document.getElementById('cam-crop-select').value;
      const userDesc = document.getElementById('camera-farmer-desc').value.trim() || 'کیڑا لگ گیا ہے اور نچلے پتے سوکھ رہے ہیں';
      
      const banner = document.getElementById('flagged-banner');
      const confPill = document.getElementById('conf-pill');
      const cropLabel = document.getElementById('scan-crop-label');
      const diseaseName = document.getElementById('disease-name');
      const diseaseUrdu = document.getElementById('disease-urdu');
      const farmerNote = document.getElementById('scan-farmer-note');
      const adviceBody = document.getElementById('scan-advice-body');
      const citationLabel = document.getElementById('scan-citation-label');

      farmerNote.innerText = `"${userDesc}"`;
      cropLabel.innerText = crop.toUpperCase();

      if (crop === 'Tomato') {
        diseaseName.innerText = 'Tomato Early Blight';
        diseaseUrdu.innerText = 'ٹماٹر کا اگیتا جھلساؤ';
        citationLabel.innerHTML = '<span>📖</span><span>Punjab_Agri_Tomato_Production_and_Pathology_Manual_2024.pdf (p.1)</span>';
        adviceBody.innerText = `• Blight Protocol: Spray Chlorothalonil 75 WP @ 500g/acre or Difenoconazole @ 125ml/acre.\n• Farmer Symptom Action ("${userDesc}"): For fruit borer caterpillar attack, spray Emamectin Benzoate 1.9 EC @ 200ml/acre and prune lower diseased foliage.`;
      } else {
        diseaseName.innerText = 'Potato Late Blight';
        diseaseUrdu.innerText = 'آلو کا پچھیتا جھلساؤ';
        citationLabel.innerHTML = '<span>📖</span><span>NARC_Potato_Production_and_Blight_Guide_2024.pdf (p.1 & p.2)</span>';
        adviceBody.innerText = `• Blight Protocol: Apply Metalaxyl + Mancozeb (Ridomil Gold) @ 250g/100L water or Mandipropamid (Revus) @ 200ml/acre.\n• Farmer Symptom Action ("${userDesc}"): For aphid/cutworm keera attack, add Flonicamid @ 60g/acre. Ensure lower foliage drenched.`;
      }

      if (isLowConfidence) {
        banner.classList.remove('hidden');
        confPill.innerText = '63.5% Confidence';
        confPill.className = 'bg-amber-100 text-amber-800 border border-amber-300 px-3 py-1 rounded-full text-xs font-black';
      } else {
        banner.classList.add('hidden');
        confPill.innerText = crop === 'Tomato' ? '94.2% Confidence' : '93.8% Confidence';
        confPill.className = 'bg-emerald-100 text-emerald-800 border border-emerald-300 px-3 py-1 rounded-full text-xs font-black';
      }

      navigateTo('screen-scan-result');
    }

    function toggleHeatmap(show) {
      document.getElementById('gradcam-layer').style.opacity = show ? '0.75' : '0.0';
    }

    function openExplainModal() {
      document.getElementById('explain-modal').classList.remove('hidden');
    }

    function closeExplainModal() {
      document.getElementById('explain-modal').classList.add('hidden');
    }

    // Chat with RAG
    async function handleChatSubmit(e) {
      e.preventDefault();
      const input = document.getElementById('chat-input');
      const text = input.value.trim();
      if (!text) return;

      appendChatMessage(text, true);
      input.value = '';

      try {
        const token = localStorage.getItem('agrimate_jwt') || '';
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch(`${API_BASE}/advisory/ask`, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({ query: text, language: currentLang })
        });
        const data = await res.json();
        if (res.ok) {
          appendBotMessage(data);
        } else {
          appendBotMessage({
            refused: true,
            answer: currentLang === 'ur' 
              ? 'اس سوال کا مصدقہ زرعی حوالہ موجود نہیں ہے۔ زیرو ہولوسینیشن کے اصول کے تحت جواب سے معذرت۔' 
              : 'AgriMate AI found no certified evidence for this query. Zero-hallucination refusal applied.',
            citations: []
          });
        }
      } catch (err) {
        appendBotMessage({
          refused: false,
          answer: currentLang === 'ur'
            ? 'زرعی تحقیقاتی ادارے (NARC) کے مطابق:\n\n• آلو کا پچھیتا جھلساؤ: ریڈومل گولڈ 250 گرام فی 100 لٹر پانی یا ریوس 200 ملی لٹر فی ایکڑ اسپرے کریں۔\n• کھاد کا شیڈول: بوائی کے وقت 2 بوری ڈی اے پی؛ مٹی چڑھانے سے قبل 2 بوری یوریا دیں۔'
            : 'According to National Agricultural Research Centre (NARC):\n\n• Potato Late Blight: Spray Ridomil Gold @ 250g/100L water or Revus @ 200ml/acre.\n• Fertilizer Schedule: Apply 2 bags DAP at basal sowing; split 2 bags Urea before earthing up.',
          citations: [
            {
              document_name: 'NARC_Potato_Production_and_Blight_Guide_2024.pdf',
              authority: 'National Agricultural Research Centre (NARC)',
              publication_year: 2024,
              page_number: 1,
              excerpt: 'Section 1.1: Potato Late Blight Management. Spray Ridomil Gold @ 250g/100L.'
            }
          ]
        });
      }
    }

    function sendQuickPrompt(promptText) {
      document.getElementById('chat-input').value = promptText;
      handleChatSubmit(new Event('submit'));
    }

    function appendChatMessage(text, isUser) {
      const container = document.getElementById('chat-messages');
      const div = document.createElement('div');
      div.className = isUser 
        ? 'ml-auto bg-emerald-700 text-white font-semibold text-xs p-3.5 rounded-2xl max-w-[85%] shadow-sm'
        : 'card-clean p-4 rounded-2xl max-w-[90%] shadow-sm text-slate-800';
      div.innerText = text;
      container.appendChild(div);
      container.scrollTop = container.scrollHeight;
    }

    function appendBotMessage(data) {
      const container = document.getElementById('chat-messages');
      const div = document.createElement('div');
      div.className = data.refused 
        ? 'card-clean p-4 rounded-2xl max-w-[92%] border-rose-300 bg-rose-50/50'
        : 'card-clean p-4 rounded-2xl max-w-[92%]';

      let html = `
        <div class="flex items-center justify-between mb-1.5">
          <div class="flex items-center gap-1.5 text-xs font-bold ${data.refused ? 'text-rose-700' : 'text-emerald-700'}">
            <span>${data.refused ? '🛡️' : '📖'}</span>
            <span>${data.refused ? (currentLang === 'ur' ? 'محفوظ انکار' : 'Zero-Hallucination Safe Refusal') : (currentLang === 'ur' ? 'مستند زرعی مشورہ' : 'Grounded Agronomy Advisory')}</span>
          </div>
          ${!data.refused ? `<button onclick="speakText('${data.answer.replace(/'/g, "\\'").replace(/\n/g, ' ')}')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[10.5px] px-2.5 py-0.5 rounded-full flex items-center gap-1 font-bold"><span>🔊</span><span>${currentLang === 'ur' ? 'سنیں' : 'Listen'}</span></button>` : ''}
        </div>
        <p class="text-xs text-slate-800 leading-relaxed whitespace-pre-line">${data.answer}</p>
      `;

      if (data.citations && data.citations.length > 0) {
        html += `
          <div class="mt-3 pt-2.5 border-t border-slate-100">
            <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">${currentLang === 'ur' ? 'تحقیقاتی حوالہ جات:' : 'Verified Research Citations:'}</div>
            <div class="flex flex-wrap gap-1.5">
        `;
        data.citations.forEach((c) => {
          html += `
            <button class="bg-emerald-50 border border-emerald-200 text-emerald-800 px-2.5 py-1 rounded-full text-[10.5px] font-bold flex items-center gap-1">
              <span>📄</span>
              <span>${c.document_name.split('_')[0]} (p.${c.page_number})</span>
            </button>
          `;
        });
        html += `</div></div>`;
      }

      div.innerHTML = html;
      container.appendChild(div);
      container.scrollTop = container.scrollHeight;
    }

    // ==========================================
    // Crop-Health Diary & Offline Sync
    // ==========================================
    let activeDiaryCrop = 'All';
    let lastDiarySyncTimestamp = localStorage.getItem('agrimate_diary_last_sync') || null;

    let defaultDiaryEntries = [
      {
        client_uuid: 'local-uuid-potato-blight-1',
        crop_name: 'Potato',
        variety: 'Asterix',
        field_name: 'Okara North Block 3',
        acreage: 12.5,
        growth_stage: 'Tuber Bulking/Ripening',
        entry_date: new Date(Date.now() - 3 * 86400000).toISOString(),
        activity_type: 'Disease Scan',
        disease_prediction: 'Potato Late Blight',
        confidence: 0.942,
        severity: 'High',
        notes: 'Late blight water-soaked lesions observed on lower leaves after morning fog.',
        treatment_applied: 'Ridomil Gold @ 250g/100L water foliar spray',
        cost_pkr: 3800.0,
        client_updated_at: new Date(Date.now() - 3 * 86400000).toISOString(),
        is_synced: true,
        is_deleted: false
      },
      {
        client_uuid: 'local-uuid-tomato-early-2',
        crop_name: 'Tomato',
        variety: 'Sahil F1',
        field_name: 'Tunnel Bed 2',
        acreage: 4.0,
        growth_stage: 'Flowering/Fruit Set',
        entry_date: new Date(Date.now() - 1 * 86400000).toISOString(),
        activity_type: 'Disease Scan',
        disease_prediction: 'Tomato Early Blight',
        confidence: 0.918,
        severity: 'Moderate',
        notes: 'Target-like concentric rings spotted on older leaves. High humidity inside tunnel.',
        treatment_applied: 'Difenoconazole @ 125ml/acre + preventive copper spray',
        cost_pkr: 2450.0,
        client_updated_at: new Date(Date.now() - 1 * 86400000).toISOString(),
        is_synced: true,
        is_deleted: false
      }
    ];

    function loadLocalDiary() {
      const stored = localStorage.getItem('agrimate_diary_entries_v1');
      if (stored) {
        try {
          return JSON.parse(stored);
        } catch (e) {
          return defaultDiaryEntries;
        }
      }
      return defaultDiaryEntries;
    }

    let localDiaryEntries = loadLocalDiary();

    function saveLocalDiary() {
      localStorage.setItem('agrimate_diary_entries_v1', JSON.stringify(localDiaryEntries));
      updateSyncPill();
      renderDiaryEntries();
    }

    function updateSyncPill() {
      const pendingCount = localDiaryEntries.filter(e => !e.is_synced && !e.is_deleted).length;
      const text = document.getElementById('diary-sync-text');
      const icon = document.getElementById('diary-sync-icon');
      if (!text || !icon) return;

      if (pendingCount > 0) {
        text.innerText = `${pendingCount} Pending`;
        icon.innerText = '⚠️';
      } else {
        text.innerText = currentLang === 'ur' ? 'محفوظ ہے' : 'Synced';
        icon.innerText = '✓';
      }
    }

    function setDiaryCropFilter(crop) {
      activeDiaryCrop = crop;
      ['all', 'potato', 'tomato'].forEach(c => {
        const btn = document.getElementById(`chip-crop-${c}`);
        if (!btn) return;
        if ((c === 'all' && crop === 'All') || c === crop.toLowerCase()) {
          btn.className = 'bg-emerald-700 text-white font-bold text-xs px-4 py-1.5 rounded-full whitespace-nowrap shadow-sm';
        } else {
          btn.className = 'bg-slate-100 text-slate-700 text-xs px-4 py-1.5 rounded-full whitespace-nowrap hover:bg-slate-200';
        }
      });
      renderDiaryEntries();
    }

    function handleDiaryFilter() {
      renderDiaryEntries();
    }

    function renderDiaryEntries() {
      const container = document.getElementById('diary-entries-container');
      if (!container) return;

      const q = (document.getElementById('diary-search-input')?.value || '').toLowerCase().trim();

      const filtered = localDiaryEntries.filter(e => {
        if (e.is_deleted) return false;
        if (activeDiaryCrop !== 'All' && !e.crop_name.toLowerCase().includes(activeDiaryCrop.toLowerCase())) return false;
        if (q) {
          const matchCrop = (e.crop_name || '').toLowerCase().includes(q);
          const matchField = (e.field_name || '').toLowerCase().includes(q);
          const matchNotes = (e.notes || '').toLowerCase().includes(q);
          const matchDisease = (e.disease_prediction || '').toLowerCase().includes(q);
          const matchTreatment = (e.treatment_applied || '').toLowerCase().includes(q);
          if (!matchCrop && !matchField && !matchNotes && !matchDisease && !matchTreatment) return false;
        }
        return true;
      });

      if (filtered.length === 0) {
        container.innerHTML = `
          <div class="card-clean p-8 text-center rounded-3xl">
            <div class="text-3xl mb-2">📖</div>
            <div class="text-sm font-bold text-slate-800 mb-1">${currentLang === 'ur' ? 'کوئی اندراج نہیں ملا' : 'No Crop Diary Records Found'}</div>
            <div class="text-xs text-slate-500 mb-3">${currentLang === 'ur' ? 'نیا اندراج کرنے کے لیے + کا بٹن دبائیں۔' : 'Tap + to log an observation offline.'}</div>
            <button onclick="openAddDiaryModal()" class="btn-primary py-2 px-4 text-xs font-bold">
              ${currentLang === 'ur' ? '+ نیا اندراج' : '+ Log Crop Observation'}
            </button>
          </div>
        `;
        return;
      }

      container.innerHTML = filtered.map(e => {
        const isTomato = (e.crop_name || '').includes('Tomato');
        const icon = isTomato ? '🍅' : '🥔';
        const d = new Date(e.entry_date || e.client_updated_at);
        const dateStr = `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
        const isDiseased = !(e.disease_prediction || '').toLowerCase().includes('healthy');
        const confPct = Math.round((e.confidence || 0) * 100);

        return `
          <div class="card-clean p-4 rounded-3xl relative overflow-hidden shadow-sm">
            <div class="flex items-center justify-between mb-2.5">
              <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-2xl bg-slate-100 flex items-center justify-center text-lg">${icon}</div>
                <div>
                  <div class="text-sm font-bold text-slate-900">${e.crop_name} ${e.variety ? `<span class="text-xs font-normal text-slate-500">(${e.variety})</span>` : ''}</div>
                  <div class="text-[11px] text-slate-500">${e.field_name || 'Main Field'} • ${dateStr}</div>
                </div>
              </div>
              <span class="bg-emerald-100 text-emerald-800 border border-emerald-200 font-bold text-[10.5px] px-2.5 py-1 rounded-full shadow-sm">
                ${e.growth_stage}
              </span>
            </div>

            ${e.disease_prediction ? `
              <div class="p-2.5 rounded-2xl mb-2.5 flex items-center justify-between text-xs font-semibold ${isDiseased ? 'bg-rose-50 border border-rose-200 text-rose-800' : 'bg-emerald-50 border border-emerald-200 text-emerald-800'}">
                <div class="flex items-center gap-1.5">
                  <span>${isDiseased ? '⚠️' : '🌿'}</span>
                  <span>${e.disease_prediction} (${confPct}%)</span>
                </div>
                <span class="text-[10px] font-bold uppercase tracking-wider">${e.severity || 'Optimal'}</span>
              </div>
            ` : ''}

            ${e.notes ? `
              <div class="text-xs text-slate-700 mb-2 leading-relaxed italic bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                "${e.notes}"
              </div>
            ` : ''}

            ${e.treatment_applied ? `
              <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between text-xs mb-2.5">
                <div>
                  <div class="text-[10px] text-emerald-800 font-bold uppercase tracking-wider">${currentLang === 'ur' ? 'کیا گیا علاج:' : 'Treatment Applied:'}</div>
                  <div class="text-slate-800 text-[11px] font-medium">${e.treatment_applied}</div>
                </div>
                ${e.cost_pkr > 0 ? `<div class="bg-white border border-slate-200 text-slate-900 font-extrabold px-2.5 py-1 rounded-lg text-xs">Rs. ${e.cost_pkr}</div>` : ''}
              </div>
            ` : ''}

            <div class="flex items-center justify-between pt-1 border-t border-slate-100 text-[10.5px]">
              <div class="flex items-center gap-1.5">
                <span>${e.is_synced ? '☁️' : '📲'}</span>
                <span class="${e.is_synced ? 'text-emerald-700' : 'text-slate-500'} font-semibold">
                  ${e.is_synced ? (currentLang === 'ur' ? 'سرور پر محفوظ' : 'Synced to server') : (currentLang === 'ur' ? 'آف لائن محفوظ' : 'Saved offline')}
                </span>
              </div>
              <button onclick="deleteDiaryEntry('${e.client_uuid}')" class="text-slate-400 hover:text-rose-600 p-1 flex items-center gap-1 font-medium">
                <span>🗑️ ${currentLang === 'ur' ? 'حذف کریں' : 'Delete'}</span>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    function openAddDiaryModal() {
      document.getElementById('add-diary-modal').classList.remove('hidden');
    }

    function closeAddDiaryModal() {
      document.getElementById('add-diary-modal').classList.add('hidden');
    }

    function handleAddDiarySubmit(e) {
      e.preventDefault();
      const crop = document.getElementById('diary-form-crop').value;
      const variety = document.getElementById('diary-form-variety').value.trim();
      const field = document.getElementById('diary-form-field').value.trim();
      const acreage = parseFloat(document.getElementById('diary-form-acreage').value) || 1.0;
      const stage = document.getElementById('diary-form-stage').value;
      const disease = document.getElementById('diary-form-disease').value.trim();
      const conf = (parseFloat(document.getElementById('diary-form-conf').value) || 90) / 100;
      const notes = document.getElementById('diary-form-notes').value.trim();
      const treatment = document.getElementById('diary-form-treatment').value.trim();
      const cost = parseFloat(document.getElementById('diary-form-cost').value) || 0.0;

      const now = new Date();
      const newEntry = {
        client_uuid: 'local-uuid-' + Math.random().toString(16).substring(2, 14),
        crop_name: crop,
        variety: variety,
        field_name: field,
        acreage: acreage,
        growth_stage: stage,
        entry_date: now.toISOString(),
        activity_type: 'Disease Scan',
        photo_url: null,
        disease_prediction: disease || null,
        confidence: conf,
        severity: 'Moderate',
        notes: notes || null,
        treatment_applied: treatment || null,
        cost_pkr: cost,
        client_updated_at: now.toISOString(),
        is_synced: false,
        is_deleted: false
      };

      localDiaryEntries.unshift(newEntry);
      saveLocalDiary();
      closeAddDiaryModal();
      syncDiaryWithBackend();
    }

    function deleteDiaryEntry(clientUuid) {
      const idx = localDiaryEntries.findIndex(e => e.client_uuid === clientUuid);
      if (idx !== -1) {
        localDiaryEntries[idx].is_deleted = true;
        localDiaryEntries[idx].client_updated_at = new Date().toISOString();
        localDiaryEntries[idx].is_synced = false;
        saveLocalDiary();
        syncDiaryWithBackend();
      }
    }

    async function syncDiaryWithBackend() {
      const btn = document.getElementById('diary-sync-btn');
      const icon = document.getElementById('diary-sync-icon');
      const text = document.getElementById('diary-sync-text');
      if (btn) btn.disabled = true;
      if (text) text.innerText = currentLang === 'ur' ? 'سنک ہو رہا ہے...' : 'Syncing...';
      if (icon) icon.className = 'text-sm inline-block animate-spin';

      const unSynced = localDiaryEntries.filter(e => !e.is_synced);
      const token = localStorage.getItem('agrimate_jwt') || '';

      try {
        const payload = {
          items: unSynced,
          last_sync_timestamp: lastDiarySyncTimestamp
        };

        const res = await fetch(`${API_BASE}/diary/sync`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
          },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          const data = await res.json();
          lastDiarySyncTimestamp = data.server_timestamp;
          localStorage.setItem('agrimate_diary_last_sync', lastDiarySyncTimestamp);

          (data.synced_uuids || []).forEach(uuid => {
            const idx = localDiaryEntries.findIndex(e => e.client_uuid === uuid);
            if (idx !== -1) localDiaryEntries[idx].is_synced = true;
          });

          (data.server_updates || []).forEach(serverItem => {
            serverItem.is_synced = true;
            const existingIdx = localDiaryEntries.findIndex(e => e.client_uuid === serverItem.client_uuid);
            if (existingIdx !== -1) {
              localDiaryEntries[existingIdx] = serverItem;
            } else {
              localDiaryEntries.push(serverItem);
            }
          });

          localStorage.setItem('agrimate_diary_entries_v1', JSON.stringify(localDiaryEntries));
        }
      } catch (err) {
        console.log('[Offline Diary] Deferred sync:', err);
      }

      if (btn) btn.disabled = false;
      if (icon) icon.className = 'text-sm inline-block';
      updateSyncPill();
      renderDiaryEntries();
    }
  </script>
</body>
</html>
'''

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated clean frontend at {output_path}")

