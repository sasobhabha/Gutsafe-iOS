import SwiftUI

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
