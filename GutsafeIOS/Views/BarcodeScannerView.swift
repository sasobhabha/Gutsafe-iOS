import SwiftUI

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
