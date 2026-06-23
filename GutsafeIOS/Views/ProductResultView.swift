import SwiftUI

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
                            Text("Barcode: \(result.barcode)")
                            
                            if !result.sources.isEmpty {
                                Text("Sources: " + result.sources.map { $0.replacingOccurrences(of: "_", with: " ").capitalized }.joined(separator: ", "))
                            }
                            
                            if let cat = result.category, !cat.isEmpty {
                                Text("Category: \(cat)")
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
                    
                    Text("Gut Health Score\n(0-100)")
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
                        ForEach(detectedAdditives.sorted(), id: \.self) { add in
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
                                    ForEach(hits, id: \.self) { kw in
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
                            ForEach(bySrc.keys.sorted(), id: \.self) { key in
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
