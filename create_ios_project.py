import os
import urllib.request
from pathlib import Path

# Setup directories
workspace = Path("/Users/shashwathmanjunath/Desktop/Gutsafe")
ios_dir = workspace / "GutsafeIOS"
ios_app_dir = ios_dir / "GutsafeIOS"
ios_views_dir = ios_app_dir / "Views"
assets_dir = ios_app_dir / "Assets.xcassets"
icon_set_dir = assets_dir / "AppIcon.appiconset"
xcodeproj_dir = ios_dir / "GutsafeIOS.xcodeproj"
workspace_dir = xcodeproj_dir / "project.xcworkspace"

for d in [ios_dir, ios_app_dir, ios_views_dir, assets_dir, icon_set_dir, xcodeproj_dir, workspace_dir]:
    d.mkdir(parents=True, exist_ok=True)

print("Created directory structure...")

# Write swift files
color_theme = """import SwiftUI

extension Color {
    static let themeBg = Color(hex: "0A0F0D")
    static let themeCard = Color(hex: "141C18")
    static let themeElevated = Color(hex: "1A241F")
    static let themeBorder = Color(hex: "243028")
    static let themeBorderSubtle = Color(hex: "1E2A23")
    static let themeText = Color(hex: "F0F5F2")
    static let themeSecondary = Color(hex: "9AAB9F")
    static let themeAccent = Color(hex: "4ADE80")
    static let themeAccentSoft = Color(hex: "22C55E")
    static let themeAccentMuted = Color(hex: "4ADE80").opacity(0.12)
    static let themeWarn = Color(hex: "FBBF24")
    static let themeWarnMuted = Color(hex: "FBBF24").opacity(0.12)
    static let themeDanger = Color(hex: "F87171")
    static let themeDangerMuted = Color(hex: "F87171").opacity(0.12)
}

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8 * 17) & 0xFF, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, (int >> 16) & 0xFF, (int >> 8) & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = ((int >> 24) & 0xFF, (int >> 16) & 0xFF, (int >> 8) & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}
"""

models_swift = """import Foundation

struct ProductResponse: Codable, Identifiable {
    var id: String { barcode }
    let barcode: String
    let sources: [String]
    let productName: String?
    let brands: String?
    let category: String?
    let imageUrl: String?
    let ingredientsText: String?
    let ingredientsBySource: [String: String]?
    let warning: String?
    let score: GutHealthScore?

    enum CodingKeys: String, CodingKey {
        case barcode
        case sources
        case productName = "product_name"
        case brands
        case category
        case imageUrl = "image_url"
        case ingredientsText = "ingredients_text"
        case ingredientsBySource = "ingredients_by_source"
        case warning
        case score
    }
}

struct GutHealthScore: Codable {
    let wellbeingIndex: Double?
    let modelWellbeingIndex: Double?
    let additiveFlags: [String: Int]?
    let literatureAggregatedEffects: [String: Double]?
    let lexiconKeywordHits: [String]?
    let lexiconContribution: [String: Double]?
    let microbiomeStressIndex: Double?

    enum CodingKeys: String, CodingKey {
        case wellbeingIndex = "wellbeing_index_0_100"
        case modelWellbeingIndex = "model_wellbeing_index_0_100"
        case additiveFlags = "additive_flags"
        case literatureAggregatedEffects = "literature_aggregated_effects"
        case lexiconKeywordHits = "lexicon_keyword_hits"
        case lexiconContribution = "lexicon_contribution"
        case microbiomeStressIndex = "microbiome_stress_index_0_1"
    }
}
"""

api_client = """import Foundation

class APIClient: ObservableObject {
    @Published var apiBaseUrl: String {
        didSet {
            UserDefaults.standard.set(apiBaseUrl, forKey: "gutsafe_api_base_url")
        }
    }

    init() {
        let defaultUrl = "https://gutsafe.educhange.app"
        let oldDefaultUrl = "https://gutsafe-backend.manjunath-shankar.workers.dev"
        let savedUrl = UserDefaults.standard.string(forKey: "gutsafe_api_base_url")
        
        let needsMigration = savedUrl == nil || 
                             savedUrl == oldDefaultUrl || 
                             savedUrl?.contains("manjunath-shankar") == true || 
                             savedUrl?.contains("workers.dev") == true
                             
        if needsMigration {
            self.apiBaseUrl = defaultUrl
            UserDefaults.standard.set(defaultUrl, forKey: "gutsafe_api_base_url")
        } else {
            self.apiBaseUrl = savedUrl!
        }
    }

    func fetchProduct(barcode: String) async throws -> ProductResponse {
        var cleanUrl = apiBaseUrl.trimmingCharacters(in: .whitespacesAndNewlines)
        if !cleanUrl.hasPrefix("http://") && !cleanUrl.hasPrefix("https://") {
            cleanUrl = "http://" + cleanUrl
        }
        // Remove trailing slashes
        cleanUrl = cleanUrl.replacingOccurrences(of: "/+$", with: "", options: .regularExpression)
        
        guard let url = URL(string: "\\(cleanUrl)/api/scan/\\(barcode)") else {
            throw URLError(.badURL)
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.timeoutInterval = 15
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw URLError(.badServerResponse)
        }

        if httpResponse.statusCode == 404 {
            throw NSError(domain: "GutSafe", code: 404, userInfo: [NSLocalizedDescriptionKey: "Product not found."])
        } else if httpResponse.statusCode != 200 {
            if let errorObj = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                if let detail = errorObj["detail"] as? String {
                    throw NSError(domain: "GutSafe", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: detail])
                } else if let detailObj = errorObj["detail"] as? [String: Any],
                          let detailMsg = detailObj["message"] as? String {
                    throw NSError(domain: "GutSafe", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: detailMsg])
                }
            }
            throw NSError(domain: "GutSafe", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: "Server returned error status \\(httpResponse.statusCode)"])
        }

        let decoder = JSONDecoder()
        return try decoder.decode(ProductResponse.self, from: data)
    }
    
    func testConnection() async -> Bool {
        var cleanUrl = apiBaseUrl.trimmingCharacters(in: .whitespacesAndNewlines)
        if !cleanUrl.hasPrefix("http://") && !cleanUrl.hasPrefix("https://") {
            cleanUrl = "http://" + cleanUrl
        }
        cleanUrl = cleanUrl.replacingOccurrences(of: "/+$", with: "", options: .regularExpression)
        
        guard let url = URL(string: "\\(cleanUrl)/api/health") else {
            return false
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.timeoutInterval = 5
        
        do {
            let (_, response) = try await URLSession.shared.data(for: request)
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                return true
            }
        } catch {
            print("Connection test failed: \\(error.localizedDescription)")
        }
        return false
    }
}
"""

camera_scanner = """import SwiftUI
import AVFoundation

struct CameraScannerView: UIViewControllerRepresentable {
    @Binding var scannedCode: String?
    @Binding var isScanning: Bool
    var onError: (String) -> Void

    func makeUIViewController(context: Context) -> CameraScannerViewController {
        let controller = CameraScannerViewController()
        controller.delegate = context.coordinator
        return controller
    }

    func updateUIViewController(_ uiViewController: CameraScannerViewController, context: Context) {
        if isScanning {
            uiViewController.startScanning()
        } else {
            uiViewController.stopScanning()
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, AVCaptureMetadataOutputObjectsDelegate {
        var parent: CameraScannerView

        init(_ parent: CameraScannerView) {
            self.parent = parent
        }

        func metadataOutput(_ output: AVCaptureMetadataOutput, didOutput metadataObjects: [AVMetadataObject], from connection: AVCaptureConnection) {
            guard parent.isScanning else { return }
            if let metadataObject = metadataObjects.first {
                guard let readableObject = metadataObject as? AVMetadataMachineReadableCodeObject else { return }
                guard let stringValue = readableObject.stringValue else { return }
                
                // Successful read! Provide audio/haptic feedback
                AudioServicesPlaySystemSound(SystemSoundID(kSystemSoundID_Vibrate))
                
                DispatchQueue.main.async {
                    self.parent.scannedCode = stringValue
                    self.parent.isScanning = false
                }
            }
        }
    }
}

class CameraScannerViewController: UIViewController {
    var delegate: AVCaptureMetadataOutputObjectsDelegate?
    var captureSession: AVCaptureSession?
    var previewLayer: AVCaptureVideoPreviewLayer?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .black
        setupCaptureSession()
    }
    
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        previewLayer?.frame = view.layer.bounds
    }
    
    func setupCaptureSession() {
        let session = AVCaptureSession()
        self.captureSession = session
        
        guard let videoCaptureDevice = AVCaptureDevice.default(for: .video) else {
            // Simulator or device without camera
            showErrorLabel("Camera not available on simulator.\\nUse manual entry or simulator mock button.")
            return
        }
        
        let videoInput: AVCaptureDeviceInput
        
        do {
            videoInput = try AVCaptureDeviceInput(device: videoCaptureDevice)
        } catch {
            showErrorLabel("Could not access camera: \\(error.localizedDescription)")
            return
        }
        
        if (session.canAddInput(videoInput)) {
            session.addInput(videoInput)
        } else {
            showErrorLabel("Could not setup camera input")
            return
        }
        
        let metadataOutput = AVCaptureMetadataOutput()
        
        if (session.canAddOutput(metadataOutput)) {
            session.addOutput(metadataOutput)
            
            metadataOutput.setMetadataObjectsDelegate(delegate, queue: DispatchQueue.main)
            metadataOutput.metadataObjectTypes = [.ean13, .ean8, .pdf417, .qr, .code128, .code39, .code93, .upce]
        } else {
            showErrorLabel("Could not setup scanning output")
            return
        }
        
        let preview = AVCaptureVideoPreviewLayer(session: session)
        preview.frame = view.layer.bounds
        preview.videoGravity = .resizeAspectFill
        view.layer.addSublayer(preview)
        self.previewLayer = preview
    }
    
    func startScanning() {
        guard let session = captureSession, !session.isRunning else { return }
        DispatchQueue.global(qos: .userInitiated).async {
            session.startRunning()
        }
    }
    
    func stopScanning() {
        guard let session = captureSession, session.isRunning else { return }
        session.stopRunning()
    }
    
    private func showErrorLabel(_ message: String) {
        let label = UILabel()
        label.text = message
        label.textColor = .white
        label.numberOfLines = 0
        label.textAlignment = .center
        label.font = .systemFont(ofSize: 14, weight: .medium)
        label.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)
        
        NSLayoutConstraint.activate([
            label.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            label.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            label.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        stopScanning()
    }
}
"""

barcode_scanner_view = """import SwiftUI

struct BarcodeScannerView: View {
    @EnvironmentObject var apiClient: APIClient
    @State private var barcodeInput: String = ""
    @State private var isCameraScanning: Bool = false
    @State private var scannedCode: String? = nil
    
    @State private var isLoading: Bool = false
    @State private var errorMessage: String? = nil
    @State private var successMessage: String? = nil
    @State private var analysisResult: ProductResponse? = nil
    
    var body: some View {
        NavigationView {
            ZStack {
                Color.themeBg.ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 24) {
                        // Header
                        VStack(spacing: 8) {
                            HStack(spacing: 12) {
                                Image(systemName: "shield.chevron.fill")
                                    .font(.system(size: 32))
                                    .foregroundColor(.themeBg)
                                    .padding(8)
                                    .background(
                                        LinearGradient(
                                            colors: [.themeAccent, .themeAccentSoft],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .cornerRadius(12)
                                
                                Text("GutSafe AI")
                                    .font(.custom("PlayfairDisplay-Bold", size: 30))
                                    .fontWeight(.bold)
                                    .foregroundColor(.themeText)
                            }
                            
                            Text("Scan food barcodes to analyze ingredients and discover how they may affect your gut health.")
                                .font(.system(size: 14))
                                .foregroundColor(.themeSecondary)
                                .multilineTextAlignment(.center)
                                .padding(.horizontal)
                        }
                        .padding(.top, 16)
                        
                        // Input Card
                        VStack(alignment: .leading, spacing: 16) {
                            HStack(spacing: 12) {
                                Image(systemName: "barcode.viewfinder")
                                    .font(.title2)
                                    .foregroundColor(.themeAccent)
                                    .frame(width: 40, height: 40)
                                    .background(Color.themeAccentMuted)
                                    .cornerRadius(10)
                                
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("Enter Barcode")
                                        .font(.headline)
                                        .foregroundColor(.themeText)
                                    Text("Type or paste a product barcode")
                                        .font(.caption)
                                        .foregroundColor(.themeSecondary)
                                }
                            }
                            
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Product Barcode (UPC/EAN)")
                                    .font(.caption)
                                    .fontWeight(.semibold)
                                    .foregroundColor(.themeSecondary)
                                
                                HStack {
                                    TextField("e.g. 078742315805", text: $barcodeInput)
                                        .keyboardType(.numberPad)
                                        .padding(.horizontal, 16)
                                        .padding(.vertical, 12)
                                        .background(Color.themeBg)
                                        .cornerRadius(10)
                                        .foregroundColor(.themeText)
                                        .overlay(
                                            RoundedRectangle(cornerRadius: 10)
                                                .stroke(Color.themeBorder, lineWidth: 1)
                                        )
                                    
                                    Button(action: {
                                        performLookup(barcode: barcodeInput)
                                    }) {
                                        Image(systemName: "magnifyingglass")
                                            .foregroundColor(.themeBg)
                                            .padding(14)
                                            .background(
                                                LinearGradient(
                                                    colors: [.themeAccent, .themeAccentSoft],
                                                    startPoint: .topLeading,
                                                    endPoint: .bottomTrailing
                                                )
                                            )
                                            .cornerRadius(10)
                                    }
                                    .disabled(barcodeInput.trimmingCharacters(in: .whitespaces).isEmpty || isLoading)
                                }
                            }
                        }
                        .padding(20)
                        .background(Color.themeCard)
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color.themeBorder, lineWidth: 1)
                        )
                        .padding(.horizontal)
                        
                        // Camera Card
                        VStack(alignment: .leading, spacing: 16) {
                            HStack(spacing: 12) {
                                Image(systemName: "camera.fill")
                                    .font(.title2)
                                    .foregroundColor(.themeAccent)
                                    .frame(width: 40, height: 40)
                                    .background(Color.themeAccentMuted)
                                    .cornerRadius(10)
                                
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("Scan with Camera")
                                        .font(.headline)
                                        .foregroundColor(.themeText)
                                    Text("Use your device camera to scan")
                                        .font(.caption)
                                        .foregroundColor(.themeSecondary)
                                }
                            }
                            
                            ZStack {
                                if isCameraScanning {
                                    CameraScannerView(
                                        scannedCode: $scannedCode,
                                        isScanning: $isCameraScanning,
                                        onError: { err in
                                            errorMessage = err
                                            isCameraScanning = false
                                        }
                                    )
                                    .frame(height: 220)
                                    .cornerRadius(12)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 12)
                                            .stroke(Color.themeAccent, lineWidth: 2)
                                    )
                                    .transition(.opacity)
                                    
                                    // Scanning Reticle
                                    VStack {
                                        Spacer()
                                        Rectangle()
                                            .fill(Color.themeAccent)
                                            .frame(height: 2)
                                            .shadow(color: .themeAccent, radius: 4)
                                        Spacer()
                                    }
                                } else {
                                    VStack(spacing: 12) {
                                        Image(systemName: "camera.viewfinder")
                                            .font(.system(size: 48))
                                            .foregroundColor(.themeSecondary.opacity(0.6))
                                        
                                        Text("Camera Feed Inactive")
                                            .font(.subheadline)
                                            .foregroundColor(.themeSecondary)
                                    }
                                    .frame(height: 220)
                                    .frame(maxWidth: .infinity)
                                    .background(Color.themeBg)
                                    .cornerRadius(12)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 12)
                                            .stroke(Color.themeBorder, lineWidth: 1)
                                    )
                                }
                            }
                            .animation(.easeInOut, value: isCameraScanning)
                            
                            HStack(spacing: 12) {
                                Button(action: {
                                    isCameraScanning = true
                                    errorMessage = nil
                                    successMessage = nil
                                }) {
                                    HStack {
                                        Image(systemName: "play.fill")
                                        Text("Start Camera")
                                    }
                                    .fontWeight(.semibold)
                                    .foregroundColor(.themeBg)
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 12)
                                    .background(
                                        LinearGradient(
                                            colors: [.themeAccent, .themeAccentSoft],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .cornerRadius(10)
                                }
                                .disabled(isCameraScanning)
                                
                                Button(action: {
                                    isCameraScanning = false
                                }) {
                                    HStack {
                                        Image(systemName: "stop.fill")
                                        Text("Stop")
                                    }
                                    .fontWeight(.semibold)
                                    .foregroundColor(.themeText)
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 12)
                                    .background(Color.themeElevated)
                                    .cornerRadius(10)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 10)
                                            .stroke(Color.themeBorder, lineWidth: 1)
                                    )
                                }
                                .disabled(!isCameraScanning)
                            }
                            
                            // Mock Button for Simulator testing
                            #if targetEnvironment(simulator)
                            Button(action: {
                                // Mock barcode scanning with a real barcode (e.g. Coca-Cola)
                                let mockBarcodes = ["049000025010", "078742315805", "012000000133"]
                                let chosen = mockBarcodes.randomElement() ?? "049000025010"
                                barcodeInput = chosen
                                performLookup(barcode: chosen)
                            }) {
                                Text("Simulator Mock: Scan Barcode")
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .foregroundColor(.themeAccent)
                                    .padding(.vertical, 8)
                                    .frame(maxWidth: .infinity)
                                    .background(Color.themeAccentMuted)
                                    .cornerRadius(8)
                            }
                            #endif
                            
                            Text("Position the barcode within the frame. Works best with good lighting.")
                                .font(.system(size: 11))
                                .foregroundColor(.themeSecondary)
                                .lineLimit(nil)
                        }
                        .padding(20)
                        .background(Color.themeCard)
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color.themeBorder, lineWidth: 1)
                        )
                        .padding(.horizontal)
                        
                        // Status Messages
                        if isLoading {
                            HStack(spacing: 12) {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .themeAccent))
                                Text("Analyzing product...")
                                    .foregroundColor(.themeAccent)
                                    .font(.subheadline)
                            }
                            .padding(.vertical, 8)
                            .frame(maxWidth: .infinity)
                            .background(Color.themeAccentMuted)
                            .cornerRadius(10)
                            .padding(.horizontal)
                        } else if let err = errorMessage {
                            HStack(spacing: 8) {
                                Image(systemName: "exclamationmark.triangle.fill")
                                    .foregroundColor(.themeDanger)
                                Text(err)
                                    .foregroundColor(.themeDanger)
                                    .font(.subheadline)
                            }
                            .padding(.vertical, 10)
                            .padding(.horizontal, 16)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.themeDangerMuted)
                            .cornerRadius(10)
                            .padding(.horizontal)
                        } else if let ok = successMessage {
                            HStack(spacing: 8) {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(.themeAccent)
                                Text(ok)
                                    .foregroundColor(.themeAccent)
                                    .font(.subheadline)
                            }
                            .padding(.vertical, 10)
                            .padding(.horizontal, 16)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.themeAccentMuted)
                            .cornerRadius(10)
                            .padding(.horizontal)
                        }
                        
                        // Product Result View
                        if let result = analysisResult {
                            ProductResultView(result: result)
                                .padding(.horizontal)
                        }
                        
                        Spacer(minLength: 40)
                    }
                }
            }
            .navigationBarHidden(true)
            .onChange(of: scannedCode) { newCode in
                if let code = newCode {
                    barcodeInput = code
                    performLookup(barcode: code)
                    scannedCode = nil
                }
            }
        }
    }
    
    private func performLookup(barcode: String) {
        let cleanCode = barcode.trimmingCharacters(in: .whitespacesAndNewlines)
        guard cleanCode.count >= 8 else {
            errorMessage = "Please enter at least 8 digits."
            successMessage = nil
            analysisResult = nil
            return
        }
        
        isLoading = true
        errorMessage = nil
        successMessage = nil
        
        Task {
            do {
                let product = try await apiClient.fetchProduct(barcode: cleanCode)
                await MainActor.run {
                    self.analysisResult = product
                    self.successMessage = "Analysis complete!"
                    self.isLoading = false
                }
            } catch {
                await MainActor.run {
                    self.errorMessage = error.localizedDescription
                    self.analysisResult = nil
                    self.isLoading = false
                }
            }
        }
    }
}
"""

product_result_view = """import SwiftUI

struct ProductResultView: View {
    let result: ProductResponse
    
    @State private var showDetails: Bool = false
    @State private var showIngredients: Bool = false
    @State private var showSources: Bool = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            // Results Header
            HStack(spacing: 8) {
                Image(systemName: "checkmark.seal.fill")
                    .font(.title2)
                    .foregroundColor(.themeAccent)
                Text("Analysis Complete")
                    .font(.custom("PlayfairDisplay-Bold", size: 20))
                    .fontWeight(.bold)
                    .foregroundColor(.themeText)
            }
            .padding(.bottom, 8)
            
            // Warning box
            if let warning = result.warning, !warning.isEmpty {
                HStack(alignment: .top, spacing: 10) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .foregroundColor(.themeWarn)
                        .padding(.top, 2)
                    Text(warning)
                        .font(.system(size: 13))
                        .foregroundColor(.themeWarn)
                }
                .padding(12)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color.themeWarnMuted)
                .cornerRadius(10)
                .overlay(
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(Color.themeWarn.opacity(0.3), lineWidth: 1)
                )
            }
            
            // Product info & score layout
            HStack(alignment: .top, spacing: 16) {
                // Image & Info
                HStack(alignment: .top, spacing: 12) {
                    if let imgUrlStr = result.imageUrl, let imgUrl = URL(string: imgUrlStr) {
                        AsyncImage(url: imgUrl) { phase in
                            switch phase {
                            case .success(let image):
                                image.resizable()
                                     .aspectRatio(contentMode: .fit)
                            default:
                                Image(systemName: "cart.fill")
                                     .foregroundColor(.themeSecondary)
                            }
                        }
                        .frame(width: 80, height: 80)
                        .padding(6)
                        .background(Color.white)
                        .cornerRadius(10)
                    }
                    
                    VStack(alignment: .leading, spacing: 4) {
                        Text(result.productName ?? "Unknown Product")
                            .font(.headline)
                            .foregroundColor(.themeText)
                            .lineLimit(2)
                        
                        Text(result.brands ?? "")
                            .font(.subheadline)
                            .foregroundColor(.themeSecondary)
                            .lineLimit(1)
                        
                        VStack(alignment: .leading, spacing: 2) {
                            Text("Barcode: \\(result.barcode)")
                            
                            if !result.sources.isEmpty {
                                Text("Sources: " + result.sources.map { $0.replacingOccurrences(of: "_", with: " ").capitalized }.joined(separator: ", "))
                            }
                            
                            if let cat = result.category, !cat.isEmpty {
                                Text("Category: \\(cat)")
                            }
                        }
                        .font(.system(size: 11))
                        .foregroundColor(.themeSecondary)
                    }
                }
                
                Spacer()
                
                // Score Ring
                VStack(spacing: 6) {
                    let wellbeingScore = result.score?.wellbeingIndex ?? 0.0
                    
                    ScoreRingView(score: wellbeingScore)
                        .frame(width: 80, height: 80)
                    
                    Text("Gut Health Score\\n(0-100)")
                        .font(.system(size: 9))
                        .foregroundColor(.themeSecondary)
                        .multilineTextAlignment(.center)
                        .lineSpacing(2)
                }
            }
            
            // Additive Analysis
            VStack(alignment: .leading, spacing: 8) {
                Text("Additive Analysis")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundColor(.themeSecondary)
                    .tracking(1)
                
                let detectedAdditives = result.score?.additiveFlags?.filter { $0.value == 1 }.map { $0.key } ?? []
                
                if detectedAdditives.isEmpty {
                    Text("None detected")
                        .font(.system(size: 12))
                        .foregroundColor(.themeSecondary)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .background(Color.themeElevated)
                        .cornerRadius(15)
                } else {
                    FlowLayout(spacing: 6) {
                        ForEach(detectedAdditives.sorted(), id: \\.self) { add in
                            Text(add.replacingOccurrences(of: "_", with: " "))
                                .font(.system(size: 11, weight: .semibold))
                                .foregroundColor(.themeDanger)
                                .padding(.horizontal, 10)
                                .padding(.vertical, 6)
                                .background(Color.themeDangerMuted)
                                .cornerRadius(15)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 15)
                                        .stroke(Color.themeDanger.opacity(0.35), lineWidth: 1)
                                )
                        }
                    }
                }
            }
            
            // Expandable details (Reveal Analysis Details)
            VStack(alignment: .leading, spacing: 0) {
                Button(action: { showDetails.toggle() }) {
                    HStack {
                        Text("Reveal Analysis Details")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(.themeText)
                        Spacer()
                        Image(systemName: showDetails ? "chevron.up" : "chevron.down")
                            .font(.system(size: 12, weight: .bold))
                            .foregroundColor(.themeSecondary)
                    }
                    .padding()
                    .background(Color.themeElevated)
                }
                
                if showDetails {
                    VStack(alignment: .leading, spacing: 16) {
                        // Additional Concerns (Lexicon Keyword Hits in yellow)
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Additional Concerns")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.themeSecondary)
                                .tracking(1)
                            
                            let hits = result.score?.lexiconKeywordHits ?? []
                            let hasNegLex = result.score?.lexiconContribution?.values.contains { $0 < -0.001 } ?? false
                            
                            if hasNegLex && !hits.isEmpty {
                                FlowLayout(spacing: 6) {
                                    ForEach(hits, id: \\.self) { kw in
                                        Text(kw)
                                            .font(.system(size: 11, weight: .semibold))
                                            .foregroundColor(.themeWarn)
                                            .padding(.horizontal, 10)
                                            .padding(.vertical, 6)
                                            .background(Color.themeWarnMuted)
                                            .cornerRadius(15)
                                            .overlay(
                                                RoundedRectangle(cornerRadius: 15)
                                                    .stroke(Color.themeWarn.opacity(0.5), lineWidth: 1)
                                            )
                                    }
                                }
                            } else {
                                Text("None")
                                    .font(.system(size: 12))
                                    .foregroundColor(.themeSecondary)
                                    .padding(.horizontal, 12)
                                    .padding(.vertical, 6)
                                    .background(Color.themeBg)
                                    .cornerRadius(15)
                            }
                        }
                        
                        // Microbiome Impact
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Microbiome Impact")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.themeSecondary)
                                .tracking(1)
                            
                            let lit = result.score?.literatureAggregatedEffects ?? [:]
                            
                            VStack(spacing: 6) {
                                MicrobiomeRow(label: "Bifidobacterium", key: "bifido_delta", value: lit["bifido_delta"])
                                MicrobiomeRow(label: "Lactobacillus", key: "lacto_delta", value: lit["lacto_delta"])
                                MicrobiomeRow(label: "Akkermansia", key: "akkermansia_delta", value: lit["akkermansia_delta"])
                                MicrobiomeRow(label: "Microbiome Diversity", key: "diversity_delta", value: lit["diversity_delta"])
                                MicrobiomeRow(label: "Short-Chain Fatty Acids", key: "scfa_delta", value: lit["scfa_delta"])
                            }
                        }
                    }
                    .padding()
                    .background(Color.themeBg)
                    .transition(.opacity)
                }
            }
            .cornerRadius(10)
            .overlay(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(Color.themeBorder, lineWidth: 2)
            )
            
            // Full Ingredients list
            VStack(alignment: .leading, spacing: 0) {
                Button(action: { showIngredients.toggle() }) {
                    HStack {
                        Text("View Full Ingredients List")
                            .font(.system(size: 13, weight: .medium))
                            .foregroundColor(.themeSecondary)
                        Spacer()
                        Image(systemName: showIngredients ? "chevron.up" : "chevron.down")
                            .font(.system(size: 12))
                            .foregroundColor(.themeSecondary)
                    }
                    .padding()
                    .background(Color.themeElevated)
                }
                
                if showIngredients {
                    Text(result.ingredientsText ?? "No ingredients listed")
                        .font(.system(size: 12, design: .monospaced))
                        .foregroundColor(.themeText)
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(Color.themeBg)
                }
            }
            .cornerRadius(10)
            .overlay(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(Color.themeBorder, lineWidth: 1)
            )
            
            // Ingredients by Data source
            if let bySrc = result.ingredientsBySource, bySrc.count > 1 {
                VStack(alignment: .leading, spacing: 0) {
                    Button(action: { showSources.toggle() }) {
                        HStack {
                            Text("Ingredients by Data Source")
                                .font(.system(size: 13, weight: .medium))
                                .foregroundColor(.themeSecondary)
                            Spacer()
                            Image(systemName: showSources ? "chevron.up" : "chevron.down")
                                .font(.system(size: 12))
                                .foregroundColor(.themeSecondary)
                        }
                        .padding()
                        .background(Color.themeElevated)
                    }
                    
                    if showSources {
                        VStack(alignment: .leading, spacing: 12) {
                            ForEach(bySrc.keys.sorted(), id: \\.self) { key in
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(key.replacingOccurrences(of: "_", with: " ").capitalized)
                                        .font(.system(size: 11, weight: .bold))
                                        .foregroundColor(.themeAccent)
                                    Text(bySrc[key] ?? "")
                                        .font(.system(size: 11, design: .monospaced))
                                        .foregroundColor(.themeText)
                                }
                            }
                        }
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(Color.themeBg)
                    }
                }
                .cornerRadius(10)
                .overlay(
                    RoundedRectangle(cornerRadius: 10)
                        .stroke(Color.themeBorder, lineWidth: 1)
                )
            }
        }
        .padding(20)
        .background(Color.themeCard)
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.themeBorder, lineWidth: 1)
        )
    }
}

struct ScoreRingView: View {
    let score: Double
    
    var ringColor: Color {
        if score >= 90 {
            return .themeAccent
        } else if score >= 76 {
            return .themeWarn
        } else if score >= 61 {
            return Color(hex: "F97316") // Orange
        } else {
            return .themeDanger
        }
    }
    
    var body: some View {
        ZStack {
            Circle()
                .stroke(Color.themeBorder, lineWidth: 6)
            
            Circle()
                .trim(from: 0.0, to: CGFloat(min(max(score, 0), 100) / 100.0))
                .stroke(
                    ringColor,
                    style: StrokeStyle(lineWidth: 6, lineCap: .round)
                )
                .rotationEffect(Angle(degrees: -90))
                .animation(.linear(duration: 0.6), value: score)
            
            Text(String(format: "%.0f", score))
                .font(.custom("PlayfairDisplay-Bold", size: 24))
                .fontWeight(.bold)
                .foregroundColor(.themeText)
        }
    }
}

struct MicrobiomeRow: View {
    let label: String
    let key: String
    let value: Double?
    
    var textColor: Color {
        guard let val = value else { return .themeAccent }
        if val < 0 {
            if val <= -1 {
                return .themeDanger
            } else if val <= -0.5 {
                return Color(hex: "F97316")
            } else {
                return .themeWarn
            }
        }
        return .themeAccent
    }
    
    var formattedVal: String {
        guard let val = value else { return "0.00" }
        return String(format: "%+.2f", val)
    }
    
    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(textColor)
                .font(.system(size: 13, weight: .medium))
            Spacer()
            Text(formattedVal)
                .foregroundColor(textColor)
                .font(.system(size: 13, design: .monospaced))
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(Color.themeBg)
        .cornerRadius(8)
        .overlay(
            RoundedRectangle(cornerRadius: 8)
                .stroke(Color.themeBorderSubtle, lineWidth: 1)
        )
    }
}

// Simple FlowLayout helper for SwiftUI
struct FlowLayout: Layout {
    var spacing: CGFloat = 6
    
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let width = proposal.width ?? 300
        var height: CGFloat = 0
        var currentX: CGFloat = 0
        var currentY: CGFloat = 0
        var maxRowHeight: CGFloat = 0
        
        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if currentX + size.width > width {
                currentX = 0
                currentY += maxRowHeight + spacing
                maxRowHeight = 0
            }
            currentX += size.width + spacing
            maxRowHeight = max(maxRowHeight, size.height)
        }
        height = currentY + maxRowHeight
        return CGSize(width: width, height: height)
    }
    
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let width = bounds.width
        var currentX: CGFloat = bounds.minX
        var currentY: CGFloat = bounds.minY
        var maxRowHeight: CGFloat = 0
        
        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if currentX + size.width > bounds.maxX {
                currentX = bounds.minX
                currentY += maxRowHeight + spacing
                maxRowHeight = 0
            }
            subview.place(at: CGPoint(x: currentX, y: currentY), proposal: .unspecified)
            currentX += size.width + spacing
            maxRowHeight = max(maxRowHeight, size.height)
        }
    }
}
"""

about_view = """import SwiftUI

struct AdditiveRowData: Identifiable {
    var id: String { name }
    let name: String
    let bifido: String
    let lacto: String
    let akkermansia: String
    let entero: String
    let diversity: String
    let scfa: String
    let barrier: String
}

struct AboutView: View {
    let additiveData: [AdditiveRowData] = [
        AdditiveRowData(name: "Polysorbate 80 (E433)", bifido: "-0.45", lacto: "-0.40", akkermansia: "-0.55", entero: "+0.50", diversity: "-0.55", scfa: "-0.45", barrier: "0.95"),
        AdditiveRowData(name: "CMC / Cellulose Gum (E466)", bifido: "-0.25", lacto: "-0.22", akkermansia: "-0.40", entero: "+0.20", diversity: "-0.35", scfa: "-0.35", barrier: "0.75"),
        AdditiveRowData(name: "Polysorbate 60 (E435)", bifido: "-0.30", lacto: "-0.26", akkermansia: "-0.35", entero: "+0.32", diversity: "-0.35", scfa: "-0.28", barrier: "0.70"),
        AdditiveRowData(name: "Red 40 / Allura Red (E129)", bifido: "-0.18", lacto: "-0.12", akkermansia: "-0.08", entero: "+0.25", diversity: "-0.20", scfa: "-0.15", barrier: "0.55"),
        AdditiveRowData(name: "Carrageenan (E407)", bifido: "-0.08", lacto: "-0.06", akkermansia: "-0.04", entero: "+0.08", diversity: "-0.06", scfa: "-0.05", barrier: "0.20"),
        AdditiveRowData(name: "Sucralose (E955)", bifido: "-0.15", lacto: "-0.12", akkermansia: "-0.05", entero: "+0.08", diversity: "-0.08", scfa: "-0.05", barrier: "0.20"),
        AdditiveRowData(name: "Saccharin (E954)", bifido: "-0.10", lacto: "-0.12", akkermansia: "-0.04", entero: "+0.08", diversity: "-0.08", scfa: "-0.06", barrier: "0.25"),
        AdditiveRowData(name: "Sodium Nitrite (E250)", bifido: "-0.06", lacto: "-0.05", akkermansia: "-0.06", entero: "+0.12", diversity: "-0.10", scfa: "-0.08", barrier: "0.25"),
        AdditiveRowData(name: "Titanium Dioxide (E171)", bifido: "-0.05", lacto: "-0.04", akkermansia: "-0.03", entero: "+0.05", diversity: "-0.04", scfa: "+0.02", barrier: "0.15"),
        AdditiveRowData(name: "Sodium Benzoate (E211)", bifido: "-0.06", lacto: "-0.05", akkermansia: "-0.02", entero: "-0.04", diversity: "-0.05", scfa: "-0.06", barrier: "0.14"),
        AdditiveRowData(name: "Potassium Sorbate (E202)", bifido: "-0.08", lacto: "-0.06", akkermansia: "-0.03", entero: "-0.05", diversity: "-0.06", scfa: "-0.08", barrier: "0.18"),
        AdditiveRowData(name: "Aspartame (E951)", bifido: "-0.08", lacto: "-0.10", akkermansia: "0.00", entero: "+0.05", diversity: "-0.05", scfa: "-0.03", barrier: "0.15"),
        AdditiveRowData(name: "Acesulfame K (E950)", bifido: "-0.06", lacto: "-0.08", akkermansia: "-0.02", entero: "+0.05", diversity: "-0.05", scfa: "-0.04", barrier: "0.15"),
        AdditiveRowData(name: "Tartrazine / Yellow 5 (E102)", bifido: "-0.06", lacto: "-0.04", akkermansia: "-0.03", entero: "+0.08", diversity: "-0.06", scfa: "-0.04", barrier: "0.18"),
        AdditiveRowData(name: "MSG (E621)", bifido: "-0.05", lacto: "-0.06", akkermansia: "-0.03", entero: "+0.04", diversity: "-0.04", scfa: "-0.03", barrier: "0.12"),
        AdditiveRowData(name: "Stevia / Steviol (E960)", bifido: "-0.05", lacto: "-0.06", akkermansia: "0.00", entero: "+0.02", diversity: "-0.03", scfa: "-0.02", barrier: "0.08"),
        AdditiveRowData(name: "Xanthan Gum (E415)", bifido: "-0.04", lacto: "-0.03", akkermansia: "-0.04", entero: "+0.04", diversity: "-0.04", scfa: "-0.03", barrier: "0.12"),
        AdditiveRowData(name: "Sorbitol (E420)", bifido: "-0.03", lacto: "-0.04", akkermansia: "0.00", entero: "+0.03", diversity: "-0.04", scfa: "-0.04", barrier: "0.12"),
        AdditiveRowData(name: "Maltitol (E965)", bifido: "-0.03", lacto: "-0.04", akkermansia: "0.00", entero: "+0.03", diversity: "-0.04", scfa: "-0.03", barrier: "0.10"),
        AdditiveRowData(name: "Propylene Glycol (E1520)", bifido: "-0.03", lacto: "-0.03", akkermansia: "-0.02", entero: "+0.04", diversity: "-0.03", scfa: "-0.02", barrier: "0.10"),
        AdditiveRowData(name: "Phosphoric Acid (E338)", bifido: "-0.02", lacto: "-0.02", akkermansia: "-0.01", entero: "+0.02", diversity: "-0.03", scfa: "-0.02", barrier: "0.08"),
        AdditiveRowData(name: "Xylitol (E967)", bifido: "+0.08", lacto: "-0.04", akkermansia: "+0.02", entero: "-0.02", diversity: "+0.04", scfa: "+0.06", barrier: "-0.05"),
        AdditiveRowData(name: "Citric Acid (E330)", bifido: "-0.01", lacto: "-0.01", akkermansia: "0.00", entero: "+0.01", diversity: "-0.02", scfa: "-0.01", barrier: "0.04"),
        AdditiveRowData(name: "Guar Gum (E412)", bifido: "+0.12", lacto: "+0.08", akkermansia: "+0.06", entero: "-0.06", diversity: "+0.08", scfa: "+0.15", barrier: "-0.12")
    ]

    var body: some View {
        NavigationView {
            ZStack {
                Color.themeBg.ignoresSafeArea()
                
                ScrollView {
                    VStack(alignment: .leading, spacing: 24) {
                        // Header
                        HStack(spacing: 12) {
                            Image(systemName: "info.circle.fill")
                                .font(.title)
                                .foregroundColor(.themeAccent)
                            Text("About GutSafe AI")
                                .font(.custom("PlayfairDisplay-Bold", size: 26))
                                .fontWeight(.bold)
                                .foregroundColor(.themeText)
                        }
                        .padding(.top, 16)
                        
                        // Card
                        VStack(alignment: .leading, spacing: 14) {
                            Text("GutSafe AI analyzes food products to estimate their impact on gut health based on their ingredients.")
                                .font(.system(size: 14))
                                .foregroundColor(.themeSecondary)
                            
                            Divider().background(Color.themeBorder)
                            
                            // Pipeline
                            Text("Scoring Pipeline")
                                .font(.headline)
                                .foregroundColor(.themeText)
                            
                            Text("The Gut Health Score (0–100) is produced by a 6-step pipeline:")
                                .font(.caption)
                                .foregroundColor(.themeSecondary)
                            
                            VStack(alignment: .leading, spacing: 12) {
                                StepRow(number: "1", title: "Additive detection", desc: "Checks ingredients against 24 regulated additives, mapping regex and E-numbers.")
                                StepRow(number: "2", title: "Literature delta accumulation", desc: "Flags add per-target deltas across 7 gut microbiome dimensions.")
                                StepRow(number: "3", title: "Ingredient lexicon scan", desc: "Segments ingredient text, matching against a 120-entry lexicon to reward good inputs and penalize bad ones.")
                                StepRow(number: "4", title: "Ultra-processed proxy", desc: "Adds a penalty of +0.0035 per ingredient block above 6, reflecting ultra-processed correlation.")
                                StepRow(number: "5", title: "Microbiome Stress Index", desc: "Collapses deltas into a single index based on weighted probiotic loss (26%), opportunist growth (17%), diversity loss (17%), and barrier risk (40%).")
                                StepRow(number: "6", title: "Final Score mapping", desc: "Merges lexicon effects with model predictions before computing the final 0–100 score.")
                            }
                        }
                        .padding(20)
                        .background(Color.themeCard)
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color.themeBorder, lineWidth: 1)
                        )
                        
                        // Additive Table Card
                        VStack(alignment: .leading, spacing: 14) {
                            Text("Flagged Ingredient Effects")
                                .font(.headline)
                                .foregroundColor(.themeText)
                            
                            Text("Exact per-target deltas used in scoring (positive = beneficial, negative = harmful):")
                                .font(.caption)
                                .foregroundColor(.themeSecondary)
                            
                            ScrollView(.horizontal, showsIndicators: true) {
                                VStack(alignment: .leading, spacing: 0) {
                                    // Header
                                    HStack(spacing: 0) {
                                        TableHeaderCell(text: "Additive", width: 150, alignment: .leading)
                                        TableHeaderCell(text: "Bifido", width: 60)
                                        TableHeaderCell(text: "Lacto", width: 60)
                                        TableHeaderCell(text: "Akkerm.", width: 60)
                                        TableHeaderCell(text: "Entero.", width: 60)
                                        TableHeaderCell(text: "Div.", width: 60)
                                        TableHeaderCell(text: "SCFA", width: 60)
                                        TableHeaderCell(text: "Barrier", width: 60)
                                    }
                                    .padding(.vertical, 8)
                                    .background(Color.themeElevated)
                                    
                                    ForEach(additiveData) { add in
                                        let isGood = add.name.contains("Guar Gum") || add.name.contains("Xylitol")
                                        HStack(spacing: 0) {
                                            TableCell(text: add.name, width: 150, alignment: .leading, color: isGood ? .themeAccent : .themeText)
                                            TableCell(text: add.bifido, width: 60, color: colorForDelta(add.bifido))
                                            TableCell(text: add.lacto, width: 60, color: colorForDelta(add.lacto))
                                            TableCell(text: add.akkermansia, width: 60, color: colorForDelta(add.akkermansia))
                                            TableCell(text: add.entero, width: 60, color: colorForDelta(add.entero, invert: true))
                                            TableCell(text: add.diversity, width: 60, color: colorForDelta(add.diversity))
                                            TableCell(text: add.scfa, width: 60, color: colorForDelta(add.scfa))
                                            TableCell(text: add.barrier, width: 60, color: colorForDelta(add.barrier, invert: true))
                                        }
                                        .padding(.vertical, 6)
                                        Divider().background(Color.themeBorderSubtle)
                                    }
                                }
                            }
                            .cornerRadius(8)
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(Color.themeBorder, lineWidth: 1)
                            )
                        }
                        .padding(20)
                        .background(Color.themeCard)
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color.themeBorder, lineWidth: 1)
                        )
                        
                        // Disclaimer
                        Text("This tool is for educational purposes only. It is not medical advice. Consult a healthcare professional for dietary concerns.")
                            .font(.system(size: 11))
                            .italic()
                            .foregroundColor(.themeSecondary)
                            .padding(.horizontal)
                        
                        Spacer(minLength: 40)
                    }
                    .padding(.horizontal)
                }
            }
            .navigationBarHidden(true)
        }
    }
    
    private func colorForDelta(_ valStr: String, invert: Bool = false) -> Color {
        guard let val = Double(valStr) else { return .themeText }
        if val == 0 { return .themeSecondary }
        
        let isNegativeEffect = invert ? val > 0 : val < 0
        if isNegativeEffect {
            return .themeDanger
        } else {
            return .themeAccent
        }
    }
}

struct StepRow: View {
    let number: String
    let title: String
    let desc: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Text(number)
                .font(.system(size: 12, weight: .bold))
                .foregroundColor(.themeBg)
                .frame(width: 20, height: 20)
                .background(Color.themeAccent)
                .clipShape(Circle())
                .padding(.top, 2)
            
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.system(size: 13, weight: .bold))
                    .foregroundColor(.themeText)
                Text(desc)
                    .font(.system(size: 12))
                    .foregroundColor(.themeSecondary)
            }
        }
    }
}

struct TableHeaderCell: View {
    let text: String
    let width: CGFloat
    var alignment: Alignment = .center
    
    var body: some View {
        Text(text)
            .font(.system(size: 10, weight: .bold))
            .foregroundColor(.themeSecondary)
            .frame(width: width, alignment: alignment)
            .padding(.horizontal, 4)
    }
}

struct TableCell: View {
    let text: String
    let width: CGFloat
    var alignment: Alignment = .center
    var color: Color = .themeText
    
    var body: some View {
        Text(text)
            .font(.system(size: 10, design: .monospaced))
            .foregroundColor(color)
            .frame(width: width, alignment: alignment)
            .padding(.horizontal, 4)
    }
}
"""

settings_view = """import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var apiClient: APIClient
    @State private var inputUrl: String = ""
    @State private var isTesting: Bool = false
    @State private var connectionResult: ConnectionState = .untested
    
    enum ConnectionState {
        case untested
        case success
        case failure
    }
    
    var body: some View {
        NavigationView {
            ZStack {
                Color.themeBg.ignoresSafeArea()
                
                VStack(alignment: .leading, spacing: 24) {
                    // Header
                    HStack(spacing: 12) {
                        Image(systemName: "gearshape.fill")
                            .font(.title)
                            .foregroundColor(.themeAccent)
                        Text("Settings")
                            .font(.custom("PlayfairDisplay-Bold", size: 26))
                            .fontWeight(.bold)
                            .foregroundColor(.themeText)
                    }
                    .padding(.top, 16)
                    
                    // Card
                    VStack(alignment: .leading, spacing: 16) {
                        Text("API Configuration")
                            .font(.headline)
                            .foregroundColor(.themeText)
                        
                        Text("Set the base URL of your GutSafe API server. If running locally, you can use the default localhost URL.")
                            .font(.caption)
                            .foregroundColor(.themeSecondary)
                        
                        VStack(alignment: .leading, spacing: 8) {
                            Text("API Base URL")
                                .font(.caption)
                                .fontWeight(.semibold)
                                .foregroundColor(.themeSecondary)
                            
                            TextField("https://gutsafe.educhange.app", text: $inputUrl)
                                .keyboardType(.URL)
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                                .padding(.horizontal, 16)
                                .padding(.vertical, 12)
                                .background(Color.themeBg)
                                .cornerRadius(10)
                                .foregroundColor(.themeText)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 10)
                                        .stroke(Color.themeBorder, lineWidth: 1)
                                )
                        }
                        
                        HStack(spacing: 12) {
                            Button(action: {
                                apiClient.apiBaseUrl = inputUrl
                                testConnection()
                            }) {
                                HStack {
                                    if isTesting {
                                        ProgressView()
                                            .progressViewStyle(CircularProgressViewStyle(tint: .themeBg))
                                    } else {
                                        Image(systemName: "network")
                                    }
                                    Text("Save & Test")
                                }
                                .fontWeight(.semibold)
                                .foregroundColor(.themeBg)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 12)
                                .background(
                                    LinearGradient(
                                        colors: [.themeAccent, .themeAccentSoft],
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    )
                                )
                                .cornerRadius(10)
                            }
                            .disabled(isTesting || inputUrl.trimmingCharacters(in: .whitespaces).isEmpty)
                            
                            Button(action: {
                                inputUrl = "https://gutsafe.educhange.app"
                                apiClient.apiBaseUrl = inputUrl
                                connectionResult = .untested
                            }) {
                                Text("Reset Default")
                                    .fontWeight(.semibold)
                                    .foregroundColor(.themeText)
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 12)
                                    .background(Color.themeElevated)
                                    .cornerRadius(10)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 10)
                                            .stroke(Color.themeBorder, lineWidth: 1)
                                    )
                            }
                        }
                        
                        // Status
                        if connectionResult == .success {
                            HStack {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(.themeAccent)
                                Text("Connected successfully to API!")
                                    .font(.subheadline)
                                    .foregroundColor(.themeAccent)
                            }
                            .padding(.vertical, 8)
                            .frame(maxWidth: .infinity)
                            .background(Color.themeAccentMuted)
                            .cornerRadius(8)
                        } else if connectionResult == .failure {
                            HStack {
                                Image(systemName: "exclamationmark.triangle.fill")
                                    .foregroundColor(.themeDanger)
                                Text("Could not connect to API server.")
                                    .font(.subheadline)
                                    .foregroundColor(.themeDanger)
                            }
                            .padding(.vertical, 8)
                            .frame(maxWidth: .infinity)
                            .background(Color.themeDangerMuted)
                            .cornerRadius(8)
                        }
                    }
                    .padding(20)
                    .background(Color.themeCard)
                    .cornerRadius(16)
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(Color.themeBorder, lineWidth: 1)
                    )
                    
                    Spacer()
                }
                .padding(.horizontal)
            }
            .navigationBarHidden(true)
            .onAppear {
                inputUrl = apiClient.apiBaseUrl
            }
        }
    }
    
    private func testConnection() {
        isTesting = true
        connectionResult = .untested
        
        Task {
            let success = await apiClient.testConnection()
            await MainActor.run {
                self.connectionResult = success ? .success : .failure
                self.isTesting = false
            }
        }
    }
}
"""

content_view = """import SwiftUI

struct ContentView: View {
    @StateObject private var apiClient = APIClient()
    
    init() {
        // Customize the tab bar appearance for dark theme
        let appearance = UITabBarAppearance()
        appearance.configureWithOpaqueBackground()
        appearance.backgroundColor = UIColor(Color.themeCard)
        appearance.shadowColor = UIColor(Color.themeBorder)
        
        let itemAppearance = UITabBarItemAppearance()
        itemAppearance.normal.iconColor = UIColor(Color.themeSecondary)
        itemAppearance.normal.titleTextAttributes = [.foregroundColor: UIColor(Color.themeSecondary)]
        itemAppearance.selected.iconColor = UIColor(Color.themeAccent)
        itemAppearance.selected.titleTextAttributes = [.foregroundColor: UIColor(Color.themeAccent)]
        
        appearance.stackedLayoutAppearance = itemAppearance
        appearance.inlineLayoutAppearance = itemAppearance
        appearance.compactInlineLayoutAppearance = itemAppearance
        
        UITabBar.appearance().standardAppearance = appearance
        UITabBar.appearance().scrollEdgeAppearance = appearance
    }
    
    var body: some View {
        TabView {
            BarcodeScannerView()
                .tabItem {
                    Label("Scanner", systemImage: "barcode.viewfinder")
                }
            
            AboutView()
                .tabItem {
                    Label("About", systemImage: "info.circle")
                }
            
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gearshape")
                }
        }
        .environmentObject(apiClient)
        .preferredColorScheme(.dark)
    }
}
"""

gutsafe_app = """import SwiftUI

@main
struct GutsafeApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
"""

info_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key>
	<string>$(DEVELOPMENT_LANGUAGE)</string>
	<key>CFBundleExecutable</key>
	<string>$(EXECUTABLE_NAME)</string>
	<key>CFBundleIdentifier</key>
	<string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>$(PRODUCT_NAME)</string>
	<key>CFBundlePackageType</key>
	<string>$(PRODUCT_BUNDLE_PACKAGE_TYPE)</string>
	<key>CFBundleShortVersionString</key>
	<string>1.0</string>
	<key>CFBundleVersion</key>
	<string>1</string>
	<key>LSRequiresIPhoneOS</key>
	<true/>
	<key>NSCameraUsageDescription</key>
	<string>We need access to your camera to scan food product barcodes.</string>
	<key>UIApplicationSceneManifest</key>
	<dict>
		<key>UIApplicationSupportsMultipleScenes</key>
		<false/>
	</dict>
	<key>UILaunchScreen</key>
	<dict/>
	<key>UISupportedInterfaceOrientations</key>
	<array>
		<string>UIInterfaceOrientationPortrait</string>
	</array>
</dict>
</plist>
"""

# Write standard files
files = {
    ios_app_dir / "Color+Theme.swift": color_theme,
    ios_app_dir / "Models.swift": models_swift,
    ios_app_dir / "APIClient.swift": api_client,
    ios_app_dir / "Info.plist": info_plist,
    ios_app_dir / "ContentView.swift": content_view,
    ios_app_dir / "GutsafeApp.swift": gutsafe_app,
    ios_views_dir / "CameraScannerView.swift": camera_scanner,
    ios_views_dir / "BarcodeScannerView.swift": barcode_scanner_view,
    ios_views_dir / "ProductResultView.swift": product_result_view,
    ios_views_dir / "AboutView.swift": about_view,
    ios_views_dir / "SettingsView.swift": settings_view,
}

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)
    print(f"Wrote {path.name}")

# Create Assets xcassets Assets details
with open(assets_dir / "Contents.json", "w") as f:
    f.write('''{
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}''')

# App icon mapping
with open(icon_set_dir / "Contents.json", "w") as f:
    f.write('''{
  "images" : [
    {
      "idiom" : "iphone",
      "size" : "20x20",
      "scale" : "2x",
      "filename" : "icon-20-2x.png"
    },
    {
      "idiom" : "iphone",
      "size" : "20x20",
      "scale" : "3x",
      "filename" : "icon-20-3x.png"
    },
    {
      "idiom" : "iphone",
      "size" : "29x29",
      "scale" : "2x",
      "filename" : "icon-29-2x.png"
    },
    {
      "idiom" : "iphone",
      "size" : "29x29",
      "scale" : "3x",
      "filename" : "icon-29-3x.png"
    },
    {
      "idiom" : "iphone",
      "size" : "40x40",
      "scale" : "2x",
      "filename" : "icon-40-2x.png"
    },
    {
      "idiom" : "iphone",
      "size" : "40x40",
      "scale" : "3x",
      "filename" : "icon-40-3x.png"
    },
    {
      "idiom" : "iphone",
      "size" : "60x60",
      "scale" : "2x",
      "filename" : "icon-60-2x.png"
    },
    {
      "idiom" : "iphone",
      "size" : "60x60",
      "scale" : "3x",
      "filename" : "icon-60-3x.png"
    },
    {
      "idiom" : "ios-marketing",
      "size" : "1024x1024",
      "scale" : "1x",
      "filename" : "icon-1024.png"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}''')

# Download and resize app icon
try:
    print("Downloading product logo for AppIcon...")
    logo_url = "https://i.postimg.cc/vZxxKpX1/Copilot-20260418-232604.png"
    req = urllib.request.Request(logo_url, headers={'User-Agent': 'Mozilla/5.0'})
    temp_icon = icon_set_dir / "temp_logo.png"
    
    download_ok = False
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                with open(temp_icon, "wb") as f:
                    f.write(response.read())
                download_ok = True
                print("Logo downloaded successfully.")
    except Exception as e:
        print(f"Skipping download or failed: {e}")
        
    if not download_ok:
        # Fallback tiny transparent png
        png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82'
        with open(temp_icon, "wb") as f:
            f.write(png_bytes)
        print("Created fallback temporary logo.")

    # Resize temp_logo into the target resolutions
    icon_sizes = [
        ("icon-20-2x.png", 40, 40),
        ("icon-20-3x.png", 60, 60),
        ("icon-29-2x.png", 58, 58),
        ("icon-29-3x.png", 87, 87),
        ("icon-40-2x.png", 80, 80),
        ("icon-40-3x.png", 120, 120),
        ("icon-60-2x.png", 120, 120),
        ("icon-60-3x.png", 180, 180),
        ("icon-1024.png", 1024, 1024),
    ]
    
    import subprocess
    for fname, w, h in icon_sizes:
        out_path = icon_set_dir / fname
        cmd = ["sips", "-z", str(h), str(w), str(temp_icon), "--out", str(out_path)]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    # Remove temp icon
    if temp_icon.is_file():
        temp_icon.unlink()
    print("Resized all AppIcon dimensions using sips.")
except Exception as e:
    print(f"Error generating AppIcon assets: {e}")

# Write workspace metadata
with open(workspace_dir / "contents.xcworkspacedata", "w") as f:
    f.write('''<?xml version="1.0" encoding="UTF-8"?>
<Workspace
   version = "1.0">
   <FileRef
      location = "self:GutsafeIOS.xcodeproj">
   </FileRef>
</Workspace>
''')

# Generate project.pbxproj with fixed 24-character hexadecimal UUIDs
pbxproj_content = """// !$*UTF8*$!
{
	archiveVersion = 1;
	classes = {
	};
	objectVersion = 60;
	objects = {

/* Begin PBXBuildFile section */
		E10000000000000000000001 /* Color+Theme.swift in Sources */ = {isa = PBXBuildFile; fileRef = F10000000000000000000001 /* Color+Theme.swift */; };
		E10000000000000000000002 /* Models.swift in Sources */ = {isa = PBXBuildFile; fileRef = F10000000000000000000002 /* Models.swift */; };
		E10000000000000000000003 /* APIClient.swift in Sources */ = {isa = PBXBuildFile; fileRef = F10000000000000000000003 /* APIClient.swift */; };
		E10000000000000000000004 /* ContentView.swift in Sources */ = {isa = PBXBuildFile; fileRef = F10000000000000000000004 /* ContentView.swift */; };
		E10000000000000000000005 /* GutsafeApp.swift in Sources */ = {isa = PBXBuildFile; fileRef = F10000000000000000000005 /* GutsafeApp.swift */; };
		E10000000000000000000006 /* CameraScannerView.swift in Sources */ = {isa = PBXBuildFile; fileRef = F10000000000000000000006 /* CameraScannerView.swift */; };
		E10000000000000000000007 /* BarcodeScannerView.swift in Sources */ = {isa = PBXBuildFile; fileRef = F10000000000000000000007 /* BarcodeScannerView.swift */; };
		E10000000000000000000008 /* ProductResultView.swift in Sources */ = {isa = PBXBuildFile; fileRef = F10000000000000000000008 /* ProductResultView.swift */; };
		E10000000000000000000009 /* AboutView.swift in Sources */ = {isa = PBXBuildFile; fileRef = F10000000000000000000009 /* AboutView.swift */; };
		E1000000000000000000000A /* SettingsView.swift in Sources */ = {isa = PBXBuildFile; fileRef = F1000000000000000000000A /* SettingsView.swift */; };
		E1000000000000000000000B /* Assets.xcassets in Resources */ = {isa = PBXBuildFile; fileRef = F1000000000000000000000B /* Assets.xcassets */; };
/* End PBXBuildFile section */

/* Begin PBXFileReference section */
		F10000000000000000000001 /* Color+Theme.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = "Color+Theme.swift"; sourceTree = "<group>"; };
		F10000000000000000000002 /* Models.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = Models.swift; sourceTree = "<group>"; };
		F10000000000000000000003 /* APIClient.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = APIClient.swift; sourceTree = "<group>"; };
		F10000000000000000000004 /* ContentView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ContentView.swift; sourceTree = "<group>"; };
		F10000000000000000000005 /* GutsafeApp.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = GutsafeApp.swift; sourceTree = "<group>"; };
		F10000000000000000000006 /* CameraScannerView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = Views/CameraScannerView.swift; sourceTree = "<group>"; };
		F10000000000000000000007 /* BarcodeScannerView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = Views/BarcodeScannerView.swift; sourceTree = "<group>"; };
		F10000000000000000000008 /* ProductResultView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = Views/ProductResultView.swift; sourceTree = "<group>"; };
		F10000000000000000000009 /* AboutView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = Views/AboutView.swift; sourceTree = "<group>"; };
		F1000000000000000000000A /* SettingsView.swift */ = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = Views/SettingsView.swift; sourceTree = "<group>"; };
		F1000000000000000000000B /* Assets.xcassets */ = {isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = Assets.xcassets; sourceTree = "<group>"; };
		F1000000000000000000000C /* Info.plist */ = {isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; };
		F1000000000000000000000D /* GutsafeIOS.app */ = {isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = GutsafeIOS.app; sourceTree = BUILT_PRODUCTS_DIR; };
/* End PBXFileReference section */

/* Begin PBXFrameworksBuildPhase section */
		C10000000000000000000001 /* Frameworks */ = {
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXFrameworksBuildPhase section */

/* Begin PBXGroup section */
		A10000000000000000000001 = {
			isa = PBXGroup;
			children = (
				A10000000000000000000002 /* GutsafeIOS */,
				A10000000000000000000003 /* Products */,
			);
			sourceTree = "<group>";
		};
		A10000000000000000000003 /* Products */ = {
			isa = PBXGroup;
			children = (
				F1000000000000000000000D /* GutsafeIOS.app */,
			);
			name = Products;
			sourceTree = "<group>";
		};
		A10000000000000000000002 /* GutsafeIOS */ = {
			isa = PBXGroup;
			children = (
				F10000000000000000000005 /* GutsafeApp.swift */,
				F10000000000000000000004 /* ContentView.swift */,
				F10000000000000000000001 /* Color+Theme.swift */,
				F10000000000000000000002 /* Models.swift */,
				F10000000000000000000003 /* APIClient.swift */,
				F10000000000000000000006 /* CameraScannerView.swift */,
				F10000000000000000000007 /* BarcodeScannerView.swift */,
				F10000000000000000000008 /* ProductResultView.swift */,
				F10000000000000000000009 /* AboutView.swift */,
				F1000000000000000000000A /* SettingsView.swift */,
				F1000000000000000000000B /* Assets.xcassets */,
				F1000000000000000000000C /* Info.plist */,
			);
			path = GutsafeIOS;
			sourceTree = "<group>";
		};
/* End PBXGroup section */

/* Begin PBXNativeTarget section */
		B10000000000000000000001 /* GutsafeIOS */ = {
			isa = PBXNativeTarget;
			buildConfigurationList = D10000000000000000000002 /* Build configuration list for PBXNativeTarget "GutsafeIOS" */;
			buildPhases = (
				C10000000000000000000002 /* Sources */,
				C10000000000000000000001 /* Frameworks */,
				C10000000000000000000003 /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = GutsafeIOS;
			productName = GutsafeIOS;
			productReference = F1000000000000000000000D /* GutsafeIOS.app */;
			productType = "com.apple.product-type.application";
		};
/* End PBXNativeTarget section */

/* Begin PBXProject section */
		910000000000000000000001 /* Project object */ = {
			isa = PBXProject;
			attributes = {
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 1500;
				LastUpgradeCheck = 1500;
				TargetAttributes = {
					B10000000000000000000001 = {
						CreatedOnToolsVersion = 15.0;
					};
				};
			};
			buildConfigurationList = D10000000000000000000001 /* Build configuration list for PBXProject "GutsafeIOS" */;
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = A10000000000000000000001;
			productRefGroup = A10000000000000000000003 /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				B10000000000000000000001 /* GutsafeIOS */,
			);
		};
/* End PBXProject section */

/* Begin PBXResourcesBuildPhase section */
		C10000000000000000000003 /* Resources */ = {
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				E1000000000000000000000B /* Assets.xcassets in Resources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXResourcesBuildPhase section */

/* Begin PBXSourcesBuildPhase section */
		C10000000000000000000002 /* Sources */ = {
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				E10000000000000000000001 /* Color+Theme.swift in Sources */,
				E10000000000000000000002 /* Models.swift in Sources */,
				E10000000000000000000003 /* APIClient.swift in Sources */,
				E10000000000000000000004 /* ContentView.swift in Sources */,
				E10000000000000000000005 /* GutsafeApp.swift in Sources */,
				E10000000000000000000006 /* CameraScannerView.swift in Sources */,
				E10000000000000000000007 /* BarcodeScannerView.swift in Sources */,
				E10000000000000000000008 /* ProductResultView.swift in Sources */,
				E10000000000000000000009 /* AboutView.swift in Sources */,
				E1000000000000000000000A /* SettingsView.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		};
/* End PBXSourcesBuildPhase section */

/* Begin XCBuildConfiguration section */
		E100000000000000000000C1 /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_TESTABILITY = YES;
				ENABLE_USER_SCRIPT_SANDBOXING = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_OPTIMIZATION_LEVEL = 0;
				GCC_PREPROCESSOR_DEFINITIONS = (
					"DEBUG=1",
					"$(inherited)",
				);
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 16.0;
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				MTL_FAST_MATH = YES;
				ONLY_ACTIVE_ARCH = YES;
				SDKROOT = iphoneos;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
			};
			name = Debug;
		};
		E100000000000000000000C2 /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				COPY_PHASE_STRIP = YES;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_USER_SCRIPT_SANDBOXING = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				IPHONEOS_DEPLOYMENT_TARGET = 16.0;
				MTL_ENABLE_DEBUG_INFO = NO;
				MTL_FAST_MATH = YES;
				SDKROOT = iphoneos;
				SWIFT_COMPILATION_MODE = wholemodule;
				SWIFT_OPTIMIZATION_LEVEL = "-O";
				VALIDATE_PRODUCT = YES;
			};
			name = Release;
		};
		T100000000000000000000C1 /* Debug */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = GutsafeIOS/Info.plist;
				INFOPLIST_KEY_CFBundleDisplayName = "GutSafe AI";
				INFOPLIST_KEY_NSCameraUsageDescription = "We need access to your camera to scan food product barcodes.";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.gutsafe.ai;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			};
			name = Debug;
		};
		T100000000000000000000C2 /* Release */ = {
			isa = XCBuildConfiguration;
			buildSettings = {
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				DEVELOPMENT_TEAM = "";
				GENERATE_INFOPLIST_FILE = YES;
				INFOPLIST_FILE = GutsafeIOS/Info.plist;
				INFOPLIST_KEY_CFBundleDisplayName = "GutSafe AI";
				INFOPLIST_KEY_NSCameraUsageDescription = "We need access to your camera to scan food product barcodes.";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = com.gutsafe.ai;
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			};
			name = Release;
		};
/* End XCBuildConfiguration section */

/* Begin XCConfigurationList section */
		D10000000000000000000002 /* Build configuration list for PBXNativeTarget "GutsafeIOS" */ = {
			isa = XCConfigurationList;
			buildConfigurations = (
				T100000000000000000000C1 /* Debug */,
				T100000000000000000000C2 /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
		D10000000000000000000001 /* Build configuration list for PBXProject "GutsafeIOS" */ = {
			isa = XCConfigurationList;
			buildConfigurations = (
				E100000000000000000000C1 /* Debug */,
				E100000000000000000000C2 /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		};
/* End XCConfigurationList section */
	};
	rootObject = 910000000000000000000001 /* Project object */;
}
"""

with open(xcodeproj_dir / "project.pbxproj", "w") as f:
    f.write(pbxproj_content)
print("Generated xcodeproj folder with project.pbxproj successfully!")
print("Project setup complete!")
