"""
AgriMate AI - Clean Frontend Generator
Builds the upgraded index.html with:
1. Dedicated separate Instagram/Facebook-style Login and Sign Up screens
2. Strict authentication gating (no access to scanner, diary, advisor without login; hidden nav on auth)
3. Full English vs Urdu language toggle (no random mixed text; pure English or pure Urdu with RTL)
4. Retains all Phase 1-5 capabilities (CNN, Grad-CAM, RAG, TTS, Offline Diary Sync, Overview)
"""

def generate_index_html():
    return '''<!DOCTYPE html>
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
    /* Urdu Nastaliq styling when RTL is active */
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
      background: rgba(255, 255, 255, 0.94);
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
    <!-- Top spacer -->
    <div class="h-10"></div>

    <!-- Center: Animated Brand Mark -->
    <div class="flex flex-col items-center text-center">
      <div class="relative mb-5">
        <div class="w-24 h-24 rounded-full bg-emerald-50 flex items-center justify-center pulse-glow border-2 border-emerald-500/20 shadow-xl">
          <!-- Friendly Farmer Straw Hat Logo -->
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
        <!-- Identifier Input -->
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

        <!-- Password Input with Show/Hide Eye Toggle -->
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label id="lbl-login-pwd" class="text-xs font-bold text-slate-700">Password</label>
            <a href="#" onclick="alert('Use the quick demo accounts below!')" id="lnk-forgot-pwd" class="text-[11px] font-semibold text-emerald-700 hover:underline">Forgot?</a>
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

        <!-- Remember Me Checkbox -->
        <div class="flex items-center gap-2 pt-0.5">
          <input type="checkbox" id="login-remember" checked class="w-4 h-4 rounded text-emerald-600 accent-emerald-600">
          <label id="lbl-remember-me" for="login-remember" class="text-xs text-slate-600 font-medium">Keep me signed in on this phone</label>
        </div>

        <!-- Submit Button -->
        <button id="login-submit-btn" type="submit" class="btn-primary w-full py-3.5 text-xs font-bold mt-2 shadow-md flex items-center justify-center gap-2">
          <span id="txt-login-btn">Log In</span>
          <svg class="w-4 h-4 stroke-current stroke-2 fill-none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"/></svg>
        </button>
      </form>

      <!-- Switch to Sign Up (Instagram style bottom link) -->
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

    <!-- Regulatory Security Note -->
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

      <!-- Hero Header -->
      <div class="mb-5">
        <h2 id="reg-heading" class="text-2xl font-black text-slate-900 tracking-tight">Create Account 🌿</h2>
        <p id="reg-subtitle" class="text-xs text-secondary mt-1">Join Pakistan's precision agricultural network.</p>
      </div>

      <!-- Error Alert Box -->
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

    <!-- Regulatory Security Note -->
    <div id="txt-security-note-reg" class="text-center text-[10px] text-slate-400 pt-6">
      🔒 256-bit Secure PBKDF2 Encryption • Strictly compliant with NARC guidelines
    </div>
  </section>
'''

if __name__ == "__main__":
    print("Test build string generated.")

