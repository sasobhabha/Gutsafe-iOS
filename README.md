# GutSafe AI iOS App

A native iOS/iPadOS application built in SwiftUI that scans food product barcodes, analyzes ingredients, and displays gut health metrics. It mirrors the exact visual aesthetic, color palette, and scoring logic of the GutSafe AI web application.

## Screen Mockups & Features

- **Live Camera Barcode Scanner**: Captures EAN/UPC/EAN-8/UPC-E barcodes using your device camera, providing audio and haptic feedback.
- **Manual Input**: A developer-friendly input section for manual barcode lookups.
- **API Configuration**: Defaults to `https://gutsafe.educhange.app` for seamless live product lookup.
- **Analysis Dashboard**:
  - **Gut Health Score Ring**: Animated, color-coded gauge (Green, Yellow, Orange, Red) representing scores (0–100).
  - **Warnings Banner**: Important advisories/allergens retrieved from data sources.
  - **Additive Badges**: Red chips showing detected harmful emulsifiers and sweeteners.
  - **Additional Concerns**: Yellow chips showing lexicon keyword matches (e.g., ultra-processed proxies).
  - **Microbiome Impact Matrix**: Visual indicators of changes (relative abundance Δ) for Bifidobacterium, Lactobacillus, Akkermansia, ecosystem diversity, and short-chain fatty acids (SCFA).
  - **Expandable Ingredients Lists**: Detailed ingredient listings raw and partitioned by databases (Open Food Facts, USDA, SmartLabel).
- **Interactive Methodology Guide**: Explains the 6-step scoring pipeline and lists the full reference table of additives and peer-reviewed literature.

## Project Structure

```
GutsafeIOS/
├── GutsafeIOS.xcodeproj/      # Xcode project metadata
├── GutsafeIOS/
│   ├── GutsafeApp.swift       # Application Entry Point
│   ├── ContentView.swift      # Main Tab navigation interface
│   ├── Color+Theme.swift      # Custom theme colors (GutSafe Dark theme)
│   ├── Models.swift           # Decodable models matching the FastAPI responses
│   ├── APIClient.swift        # Network requests and connection testing client
│   ├── Info.plist             # App settings (requires NSCameraUsageDescription)
│   ├── Assets.xcassets/       # Universal AppIcon (generated in multi-resolution)
│   └── Views/
│       ├── CameraScannerView.swift     # AVFoundation-based camera controller
│       ├── BarcodeScannerView.swift    # Core scanning dashboard and input UI
│       ├── ProductResultView.swift     # Product details and scoring presentation
│       ├── AboutView.swift             # scoring pipeline and additives reference
│       └── SettingsView.swift          # API Server configuration UI
```

## Setup & Running

### 1. Prerequisites
- macOS running Xcode 15 or later (Xcode 27.0 beta is active on this system)
- An active backend server. You can run the GutSafe API locally:
  ```bash
  python3 src/api_server.py
  ```
  The local server runs at `http://127.0.0.1:8000`.

### 2. Running in Simulator
1. Open Xcode.
2. Select **File > Open** and choose the `GutsafeIOS.xcodeproj` folder located inside the `GutsafeIOS` project folder.
3. Select an iOS Simulator device (e.g., iPhone 17) from the scheme selector.
4. Press `Cmd + R` or click the **Play** button to compile and run.
5. In the simulator, you can use the **Simulator Mock: Scan Barcode** button to simulate scanning real barcodes (like Coca-Cola) since the simulator does not support physical camera feeds.
6. By default, the app communicates with the live backend at `https://gutsafe.educhange.app`. If you want to run against a local backend instead, run `python3 src/api_server.py` and modify `apiBaseUrl` in `APIClient.swift` to `http://localhost:8000`.

### 3. Running on a Physical iOS Device
1. Connect your iPhone/iPad to your Mac.
2. Select your device from the scheme selector.
3. Go to the project's **Signing & Capabilities** tab in Xcode.
4. Select your Apple Developer account Team.
5. Press `Cmd + R` to run.
6. The app will request Camera permissions on first startup. Scan a product barcode to test!

## Core UI Palette
- **Deep Slate Background**: `#0A0F0D`
- **Card Fill**: `#141C18`
- **Accent Emerald Green**: `#4ADE80`
- **Secondary Sage Green**: `#9AAB9F`
- **Danger Soft Red**: `#F87171`
- **Warning Yellow**: `#FBBF24`
