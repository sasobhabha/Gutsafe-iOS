import SwiftUI

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
