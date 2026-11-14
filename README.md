# Apna AI

Android AI chat app powered by Gemini 2.5 Flash.

## Build APK

The GitHub Actions workflow builds a debug APK whenever code is pushed. Open the **Actions** tab, select **Build Android APK**, and download `Apna-AI-debug-apk` from the completed workflow run's Artifacts section.

## API key

On first launch, enter your Gemini API key in the app. It is stored only on the device using browser local storage; it is not committed to this repository. Do not share your key in chat or commit it to GitHub.

**Security note:** This starter calls Gemini directly from the Android app. A key stored on a client device can potentially be extracted. Before public release or multi-user deployment, move Gemini requests behind a secure backend and add authentication, rate limits, and privacy controls.
