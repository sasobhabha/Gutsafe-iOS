import Foundation

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
        
        guard let url = URL(string: "\(cleanUrl)/api/scan/\(barcode)") else {
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
            throw NSError(domain: "GutSafe", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: "Server returned error status \(httpResponse.statusCode)"])
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
        
        guard let url = URL(string: "\(cleanUrl)/api/health") else {
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
            print("Connection test failed: \(error.localizedDescription)")
        }
        return false
    }
}
