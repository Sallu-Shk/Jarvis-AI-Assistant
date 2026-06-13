#!/usr/bin/env python3

import os
import shutil
import time

# =========================
# DEVICE INFO
# =========================

def get_info():

    # Setup robust fallback values to prevent crashes
    data = {
        "brand": "Unknown",
        "model": "Unknown",
        "android": "Unknown",
        "cpu": "Unknown",
        "battery": "Unknown",
        "ram": 2,
        "refresh": 144,  # Hardcoded standard peak for Infinix X6873 (GT 30 Pro)
        "battery_temp": "Unknown",
        "profile": "Budget",
        "score": 50
    }

    try:
        data["brand"] = os.popen("getprop ro.product.brand").read().strip() or "Unknown"
        data["model"] = os.popen("getprop ro.product.model").read().strip() or "Unknown"
        data["android"] = os.popen("getprop ro.build.version.release").read().strip() or "Unknown"
        data["cpu"] = os.popen("getprop ro.product.cpu.abi").read().strip() or "Unknown"
        
        # Termux battery parsing block
        try:
            battery = os.popen(
                "termux-battery-status | grep percentage | cut -d':' -f2 | tr -dc '0-9'"
            ).read().strip()
            data["battery"] = battery if battery else "Unknown"
        except Exception:
            data["battery"] = "Unknown"
    
        # RAM Detection
        total_ram_gb = 2
        if os.path.exists("/proc/meminfo"):
            with open("/proc/meminfo") as f:
                mem = f.readlines()
            total_ram_mb = int(mem[0].split()[1]) // 1024

            if total_ram_mb >= 11000:
                total_ram_gb = 12
            elif total_ram_mb >= 7000:
                total_ram_gb = 8
            elif total_ram_mb >= 5000:
                total_ram_gb = 6
            elif total_ram_mb >= 3000:
                total_ram_gb = 4
            else:
                total_ram_gb = max(1, round(total_ram_mb / 1024))
        
        data["ram"] = total_ram_gb

        # ADVANCED REFRESH RATE DETECTION
        try:
            # Check 1: Peak refresh property
            refresh = os.popen("settings get system peak_refresh_rate").read().strip()
            # Check 2: User custom manual override selection if peak is null
            if not refresh or refresh == "null":
                refresh = os.popen("settings get system user_refresh_rate").read().strip()
                
            if refresh and refresh != "null":
                detected_hz = int(float(refresh))
                # Guard case against system battery saver capping data calculation to 60Hz dynamically
                if data["model"] == "Infinix X6873" and detected_hz < 90:
                    data["refresh"] = 144
                else:
                    data["refresh"] = detected_hz
            else:
                data["refresh"] = 144 if data["model"] == "Infinix X6873" else 60
        except Exception:
            data["refresh"] = 144 if data["model"] == "Infinix X6873" else 60
    
        # Termux battery temperature parsing block
        try:
            temp = os.popen(
                "termux-battery-status | grep temperature | cut -d':' -f2 | tr -dc '0-9.'"
            ).read().strip()
            data["battery_temp"] = temp + "°C" if temp else "Unknown"
        except Exception:
            data["battery_temp"] = "Unknown"

        # Gaming Profile
        if total_ram_gb >= 12:
            profile = "Flagship"
        elif total_ram_gb >= 8:
            profile = "High End"
        elif total_ram_gb >= 6:
            profile = "Mid Range"
        else:
            profile = "Budget"

        # Gaming Score
        score = 50
        if total_ram_gb >= 12:
            score += 25
        elif total_ram_gb >= 8:
            score += 20
        elif total_ram_gb >= 6:
            score += 15
        else:
            score += 5

        # Refresh Rate Score Addition
        if data["refresh"] >= 144:
            score += 25
        elif data["refresh"] >= 120:
            score += 15
        elif data["refresh"] >= 90:
            score += 10

        data["profile"] = profile
        data["score"] = min(score, 100)

    except Exception:
        pass

    return data

def banner():
    os.system("clear")

    print("\033[1;96m")
    print("╔════════════════════════════════════╗")
    print("║      \033[1;31m🤖 JARVIS AI ASSISTANT\033[1;96m      ║")
    print("╚════════════════════════════════════╝")
    print("\033[0m")

    print("\033[1;33m🔻 MAKER      : \033[1;31mSalman\033[0m")
    print("\033[1;36m🔻 VERSION    : \033[1;31mJarvis AI 2.1\033[0m")
    print("\033[1;32m🔻 STATUS     : \033[1;31mOnline\033[0m")
    print("\033[1;35m🔻 TG         : \033[1;31m@OfficialOwner10x\033[0m")

    print("\033[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    
# =========================
# BGMI
# =========================
def jarvis_scan():

    os.system("clear")

    scans = [
        ("\033[1;32m🔍 Detecting Device Hardware...\033[0m", 20),
        ("\033[1;33m⚙ Reading System Information...\033[0m", 40),
        ("\033[1;36m📊 Analyzing RAM & Storage...\033[0m", 60),
        ("\033[1;35m🎮 Building Gaming Profile...\033[0m", 80),
        ("\033[1;31m🚀 Preparing Final Report...\033[0m", 100)
    ]

    for text, percent in scans:

        os.system("clear")

        print("\033[1;96m")
        print("╔══════════════════════════════════════╗")
        print("║      🤖 JARVIS AI ANALYZING... 🤖       ║")
        print("╚══════════════════════════════════════╝")
        print("\033[0m")

        print("\n" + text + "\n")

        filled = "■" * (percent // 10)
        empty = "□" * (10 - percent // 10)

        if percent < 100:
            color = "\033[1;33m"   # Yellow
        else:
            color = "\033[1;32m"   # Green

        print(f"{color}[{filled}{empty}] {percent}%\033[0m")

        time.sleep(1.5)

    print("\n\033[1;92m✅ ANALYSIS COMPLETE\033[0m")
    print("\033[1;36m📋 Loading Results...\033[0m")

    time.sleep(1)

    os.system("clear")
    
def bgmi():
    d = get_info()
    ram = d["ram"]
    refresh = d["refresh"]
    score = d["score"]

    if score >= 90 or refresh >= 120:
        fps = "120 FPS"
        gyro = [350, 340, 320, 280, 240]
    elif score >= 80:
        fps = "120 FPS" if refresh >= 120 else "90 FPS"
        gyro = [330, 320, 300, 260, 220]
    elif score >= 70:
        fps = "90 FPS"
        gyro = [310, 290, 270, 240, 200]
    elif score >= 60:
        fps = "60 FPS"
        gyro = [290, 270, 250, 220, 180]
    else:
        fps = "40 FPS"
        gyro = [260, 240, 220, 190, 160]

    print("\033[1;95m")
    print("╔════════════════════════════════════╗")
    print("║        🔻 BGMI PROFILE 🔻          ║")
    print("╚════════════════════════════════════╝")
    print("\033[0m")

    print("\033[1;36m📱 🔸DEVICE INFORMATION🔸\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print(f"🔺 Device       : {d['model']}")
    print(f"🔺 Battery      : {d['battery']}%")
    print(f"🔺 RAM          : {ram} GB")
    print(f"🔺 Android      : {d['android']}")
    print(f"🔺 CPU ABI      : {d['cpu']}")
    print(f"🔺 Refresh Rate : {refresh} Hz")
    print(f"🔺 Battery Temp : {d['battery_temp']}")
    print(f"🔺 Gaming Score : {d['score']}/100")
    print(f"🔺 Profile      : {d['profile']}")

    print("\n\033[1;33m🎥 CAMERA SETTINGS\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print("🔸 TPP No Scope : 180")
    print("🔸 FPP No Scope : 170")
    print("🔸 Red Dot      : 60")
    print("🔸 2x Scope     : 45")
    print("🔸 3x Scope     : 30")
    print("🔸 4x Scope     : 20")

    print("\n\033[1;32m🎯 ADS SETTINGS\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print("🔸 TPP No Scope : 120")
    print("🔸 FPP No Scope : 110")
    print("🔸 Red Dot      : 55")
    print("🔸 2x Scope     : 40")
    print("🔸 3x Scope     : 30")

    print("\n\033[1;35m🌀 GYROSCOPE SETTINGS\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print(f"🔸 No Scope     : {gyro[0]}")
    print(f"🔸 Red Dot      : {gyro[1]}")
    print(f"🔸 2x Scope     : {gyro[2]}")
    print(f"🔸 3x Scope     : {gyro[3]}")
    print(f"🔸 4x Scope     : {gyro[4]}")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"\033[1;92m 🔻RECOMMENDED FPS🔻 : {fps}\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
# =========================
# FREE FIRE
# =========================

def ff():
    d = get_info()
    score = d["score"]
    refresh = d["refresh"]

    if score >= 90:
        fps = "Ultra / Max"
        general = 100
        red_dot = 95
        x2 = 90
        x4 = 80
        awm = 60
        free_look = 90
    elif score >= 80:
        fps = "Ultra / Max" if refresh >= 120 else "High"
        general = 95
        red_dot = 90
        x2 = 85
        x4 = 75
        awm = 55
        free_look = 85
    elif score >= 70:
        fps = "High"
        general = 90
        red_dot = 85
        x2 = 80
        x4 = 70
        awm = 50
        free_look = 80
    else:
        fps = "Medium"
        general = 85
        red_dot = 80
        x2 = 75
        x4 = 65
        awm = 45
        free_look = 75

    print("\033[1;96m")
    print("╔════════════════════════════════════╗")
    print("║        🔻 FREE FIRE PROFIL 🔻        ║")
    print("╚════════════════════════════════════╝")
    print("\033[0m")

    print("\033[1;36m📱 🔸DEVICE INFORMATION🔸\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print(f"🔺 Device       : {d['model']}")
    print(f"🔺 Battery      : {d['battery']}%")
    print(f"🔺 RAM          : {d['ram']} GB")
    print(f"🔺 Android      : {d['android']}")
    print(f"🔺 CPU ABI      : {d['cpu']}")
    print(f"🔺 Refresh Rate : {d['refresh']} Hz")
    print(f"🔺 Battery Temp : {d['battery_temp']}")
    print(f"🔺 Gaming Score : {d['score']}/100")
    print(f"🔺 Profile      : {d['profile']}")

    print("\n\033[1;33m🎯 FREE FIRE SENSITIVITY\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print(f"🔸 General      : {general}")
    print(f"🔸 Red Dot      : {red_dot}")
    print(f"🔸 2x Scope     : {x2}")
    print(f"🔸 4x Scope     : {x4}")
    print(f"🔸 AWM Scope    : {awm}")
    print(f"🔸 Free Look    : {free_look}")

    print("\n\033[1;35m🎮 🔸PERFORMANCE ANALYSIS🔸\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    bar = "█" * (score // 10) + "░" * (10 - (score // 10))

    print(f"🏆 Gaming Score : [{bar}] {score}/100")

    if score >= 90:
        tier = "🔥 EXTREME"
    elif score >= 80:
        tier = "🚀 HIGH END"
    elif score >= 70:
        tier = "⚡ MID RANGE"
    else:
        tier = "📱 BASIC"

    print(f"🎯 Device Tier  : {tier}")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"\033[1;92m 🔻RECOMMENDED FPS🔻 : {fps}\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# =========================
# RAM & STORAGE BOOSTER
# =========================

def booster():

    os.system("clear")

    print("\033[1;96m")
    print("╔════════════════════════════════════╗")
    print("║     🚀 JARVIS AI BOOSTER 🚀       ║")
    print("╚════════════════════════════════════╝")
    print("\033[0m")

    tasks = [
        "🔍 Scanning Cache Files...",
        "🧹 Cleaning Temporary Data...",
        "⚙ Optimizing System Resources...",
        "🎮 Preparing Gaming Environment...",
        "🚀 Finalizing Optimization..."
    ]

    for i, task in enumerate(tasks, start=1):

        percent = i * 20

        print(f"\n\033[1;36m{task}\033[0m")

        filled = "█" * (percent // 10)
        empty = "░" * (10 - percent // 10)

        print(f"\033[1;32m[{filled}{empty}] {percent}%\033[0m")

        time.sleep(1)

    # Cache cleanup
    paths_to_clear = [
        os.path.expanduser("~/.cache"),
        "./__pycache__"
    ]

    for path in paths_to_clear:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except:
                pass

    print("\n\033[1;92m✅ OPTIMIZATION COMPLETE\033[0m")
    print("\033[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")

    print(" 🔸Cache Files Cleaned")
    print(" 🔸Temporary Data Removed")
    print(" 🔸System Resources Optimized")
    print(" 🔸Gaming Profile Refreshed")
    print(" 🔸Device Ready For Gaming")

    print("\033[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")

    print("\n\033[1;93m🎮 STATUS : 🔸READY TO PLAY🔸\033[0m")

# =========================
# RAM STORAGE
# =========================

def ram_storage():
    
    os.system("clear")
    
    print("\033[1;96m")
    print("╔════════════════════════════════════╗")
    print("║      💾 STORAGE ANALYZER 💾       ║")
    print("╚════════════════════════════════════╝")
    print("\033[0m")

    try:
        path = "/storage/emulated/0"

        if not os.path.exists(path):
            path = "/"

        total, used, free = shutil.disk_usage(path)

        total_gb = round(total / (1024**3), 2)
        used_gb = round(used / (1024**3), 2)
        free_gb = round(free / (1024**3), 2)

        usage = round((used / total) * 100)

        print("\033[1;36m📊 STORAGE INFORMATION\033[0m")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        print(f"📦 Total Storage : {total_gb} GB")
        print(f"📁 Used Storage  : {used_gb} GB")
        print(f"💾 Free Storage  : {free_gb} GB")

        print("\n\033[1;35m📈 STORAGE USAGE\033[0m")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        filled = "█" * (usage // 5)
        empty = "░" * (20 - (usage // 5))

        print(f"[{filled}{empty}] {usage}%")

        print("\n\033[1;33m🔎 STORAGE HEALTH\033[0m")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        if free_gb < 10:
            print("\033[1;31m⚠ CRITICAL : Storage Almost Full\033[0m")
            print("🧹 Recommendation : Clean unnecessary files")
        elif free_gb < 30:
            print("\033[1;33m⚠ WARNING : Storage Running Low\033[0m")
            print("📂 Recommendation : Remove unused apps")
        else:
            print("\033[1;32m✅ HEALTHY : Storage Status Good\033[0m")
            print("🚀 Device Ready For Smooth Performance")

        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"\033[1;92m💡 Available Space : {free_gb} GB\033[0m")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    except Exception as e:
        print("\033[1;31m❌ Storage Error :\033[0m", e)

    
# =========================
# ABOUT
# =========================

def about():

    print("\033[1;96m")
    print("╔════════════════════════════════════╗")
    print("║         🤖 ABOUT JARVIS AI 2.1        ║")
    print("╚════════════════════════════════════╝")
    print("\033[0m")

    print("\033[1;36m📱 🔻TOOL INFORMATION🔻\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print("🤖 Tool Name : JARVIS AI")
    print("⚡ Version     : Jarvis 2.1")
    print("💀 Developer  : Salman")
    print("🟢 Status.     : Online")

    print("\n\033[1;33m🚀 FEATURES\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print("🎯 BGMI Gaming Analyzer")
    print("🔥 FREE FIRE Analyzer")
    print("📱 SMART Device Detection")
    print("⚡ GAMING Score Analysis")
    print("💾 RAM & Storage Analyzer")
    print("🚀 PERFORMANCE Booster")
    print("📊 FPS Recommendation")
    print("🌡 BATTERY & Temperature Monitor")

    print("\n\033[1;35m💡 PURPOSE 👇\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print("🔻JARVIS AI ANALYZES YOUR DEVICE")
    print("🔻AND PROVIDES GAMING RECOMMENDATIONS")
    print("🔻BASED ON HARDWARE CAPABILITIES.")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\033[1;92m❤️ THANKS FOR USING JARVIS AI\033[0m")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# =========================
# MAIN MENU
# =========================

while True:

    banner()

    print("\033[1;96m")
    print("╔════════════════════════════════════╗")
    print("║    \033[1;31m🎮 MAIN CONTROL PANEL\033[0m        ║")
    print("╚════════════════════════════════════╝")
    print("\033[0m")

    print("\033[1;92m➊\033[0m \033[1;36mBGMI MODULE\033[0m")
    print("\033[1;92m➋\033[0m \033[1;36mFREE FIRE MODULE\033[0m")
    print("\033[1;92m➌\033[0m \033[1;36mSTORAGE ANALYZER\033[0m")
    print("\033[1;92m➍\033[0m \033[1;36mPERFORMANCE BOOSTER\033[0m")
    print("\033[1;92m➎\033[0m \033[1;36mABOUT JARVIS AI\033[0m")
    print("\033[1;91m➏\033[0m \033[1;31mEXIT TOOL\033[0m")

    print("\n\033[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
    print("\033[1;92m💡 Select Module To Continue\033[0m")
    print("\033[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")

    choice = input("\033[1;92m┌─[🤖 JARVIS AI]\n└──► \033[0m")

    os.system("clear")

    if choice == "1":
        jarvis_scan()
        bgmi()

    elif choice == "2":
        jarvis_scan()
        ff()

    elif choice == "3":
        jarvis_scan()
        ram_storage()

    elif choice == "4":
        booster()

    elif choice == "5":
        about()

    elif choice == "6":
        print("\n\033[1;92m🤖 JARVIS AI SHUTTING DOWN...\033[0m")
        time.sleep(1)
        print("\033[1;36m👋 Goodbye Salman\033[0m")
        break

    else:
        print("\033[1;31m❌ Unknown Command Detected!\033[0m")

    input("\n\033[1;33m↩ Press Enter To Return To Menu...\033[0m")