import SwiftUI

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
