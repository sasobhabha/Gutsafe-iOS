import SwiftUI

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
