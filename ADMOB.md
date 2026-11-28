# Switching from test ads to real ads

1. AdMob → Apps → Add app → Android → (not yet on Play) → name "Keep Seeing Numbers".
2. Copy the App ID (ca-app-pub-XXXX~YYYY) into android/app/src/main/res/values/strings.xml (admob_app_id).
3. AdMob → the app → Ad units → Rewarded → name "Unlock reading". Copy the unit ID (ca-app-pub-XXXX/ZZZZ).
4. In www/index.html, before app.js, add: <script>window.KSN_REWARDED_ID="ca-app-pub-XXXX/ZZZZ"</script>
   (with it set, test mode turns off automatically).
