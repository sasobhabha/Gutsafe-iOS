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

struct LiteratureItem: Identifiable {
    var id = UUID()
    let text: String
    let url: String
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
                        
                        // Intro Card
                        VStack(alignment: .leading, spacing: 14) {
                            Text("GutSafe AI analyzes food products to estimate their impact on gut health based on their ingredients.")
                                .font(.system(size: 14))
                                .foregroundColor(.themeSecondary)
                            
                            Divider().background(Color.themeBorder)
                            
                            // Pipeline
                            Text("Scoring Pipeline")
                                .font(.headline)
                                .foregroundColor(.themeText)
                            
                            Text("The Gut Health Score (0–100) is produced by a 6-step pipeline run on every product's ingredient list:")
                                .font(.caption)
                                .foregroundColor(.themeSecondary)
                            
                            VStack(alignment: .leading, spacing: 12) {
                                StepRow(number: "1", title: "Additive detection", desc: "The ingredient text is scanned for 24 regulated additives using regex patterns and EU E-number synonyms. Each detected additive sets a binary flag (0 or 1).")
                                StepRow(number: "2", title: "Literature delta accumulation", desc: "Every flagged additive contributes its curated per-target deltas (see table below) to a running sum across all 7 microbiome dimensions. Multiple additives stack additively.")
                                StepRow(number: "3", title: "Ingredient lexicon scan", desc: "The text is split by comma into segments. Each segment is matched against a 120-entry lexicon (longest match wins). One contribution per segment is added to the running sum — this captures beneficial ingredients (whole grains, legumes, fermented foods) as well as harmful ones not on the additive list.")
                                StepRow(number: "4", title: "Ultra-processed proxy", desc: "If the ingredient list has more than 6 comma-separated segments, a small penalty of +0.0035 × (n − 6) is added to Gut Barrier Risk, capped at +0.14. This reflects the general association between ingredient-list length and ultra-processing.")
                                StepRowWithList(number: "5", title: "Microbiome Stress Index", desc: "The 7 merged deltas are collapsed into a single stress score (0–∞) using weighted components:", items: [
                                    "Beneficial loss (weight 0.26): sum of absolute negative deltas for Bifidobacterium, Lactobacillus, and Akkermansia",
                                    "Opportunist growth (weight 0.17): positive delta of Enterobacteriaceae (clamped ≥ 0)",
                                    "Ecosystem loss (weight 0.17): sum of absolute negative deltas for Diversity and SCFA",
                                    "Barrier risk (weight 0.40): raw barrier risk value, clamped to [0, 1.2]"
                                ])
                                StepRow(number: "6", title: "Final score", desc: "The ML model (PyTorch MLP, hidden layers [64, 32]) trained on 199 real products provides a secondary predicted-effects estimate which is merged with the lexicon before final scoring.")
                            }
                        }
                        .padding(20)
                        .background(Color.themeCard)
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color.themeBorder, lineWidth: 1)
                        )

                        // Microbiome Dimensions Card
                        VStack(alignment: .leading, spacing: 14) {
                            Text("Microbiome Dimensions")
                                .font(.headline)
                                .foregroundColor(.themeText)
                            
                            Text("All 7 target dimensions and their role in the score:")
                                .font(.caption)
                                .foregroundColor(.themeSecondary)
                            
                            VStack(alignment: .leading, spacing: 8) {
                                BulletRow(title: "Bifidobacterium Δ", desc: "Negative values reduce a keystone probiotic genus linked to immune regulation, IgA production, and pathogen exclusion.")
                                BulletRow(title: "Lactobacillus Δ", desc: "Negative values reduce lactic-acid bacteria that maintain colonic pH, compete with pathogens, and enhance nutrient bioavailability.")
                                BulletRow(title: "Akkermansia Δ", desc: "Negative values reduce the mucin-layer coloniser whose abundance correlates with intact gut barrier and metabolic health.")
                                BulletRow(title: "Enterobacteriaceae Δ", desc: "Positive values increase a family that contains opportunistic pathogens (E. coli, Klebsiella). Drives the opportunist weight.")
                                BulletRow(title: "Diversity Δ", desc: "Negative values reduce overall ecosystem richness (Shannon index proxy). Low diversity is a consistent marker of dysbiosis.")
                                BulletRow(title: "SCFA Δ", desc: "Negative values reduce short-chain fatty acid production (butyrate, propionate, acetate), which fuel colonocytes and regulate inflammation.")
                                BulletRow(title: "Gut Barrier Risk", desc: "Positive values indicate increased intestinal permeability risk (\"leaky gut\"), which drives the highest-weighted component (0.40) of the stress score.")
                            }
                            
                            Text("Colors in the Microbiome Impact panel indicate severity of negative effect: green (no impact), yellow (Δ > −0.5), orange (Δ > −1.0), red (Δ ≤ −1.0).")
                                .font(.system(size: 12))
                                .foregroundColor(.themeSecondary)
                                .padding(.top, 4)
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
                            
                            Text("Exact per-target deltas used in Step 2, sourced from peer-reviewed literature:")
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
                            
                            Text("Δ values represent estimated relative abundance / risk unit changes aggregated from published animal and human studies. Values are signed: negative = harmful, positive = beneficial. Barrier Risk: positive = higher permeability risk.")
                                .font(.system(size: 11))
                                .foregroundColor(.themeSecondary)
                                .padding(.top, 4)
                        }
                        .padding(20)
                        .background(Color.themeCard)
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color.themeBorder, lineWidth: 1)
                        )

                        // Data Sources Card
                        VStack(alignment: .leading, spacing: 14) {
                            Text("Product Data Sources")
                                .font(.headline)
                                .foregroundColor(.themeText)
                            
                            Text("Product ingredient and label data is fetched live from:")
                                .font(.caption)
                                .foregroundColor(.themeSecondary)
                            
                            VStack(alignment: .leading, spacing: 8) {
                                LinkRow(title: "Open Food Facts", desc: "global crowdsourced food product database", url: "https://world.openfoodfacts.org/")
                                LinkRow(title: "USDA FoodData Central", desc: "branded foods database from the USDA National Agricultural Library", url: "https://fdc.nal.usda.gov/")
                                LinkRow(title: "SmartLabel / Label Insight", desc: "CPG brand digital label disclosure data", url: "https://www.smartlabel.org/")
                            }
                        }
                        .padding(20)
                        .background(Color.themeCard)
                        .cornerRadius(16)
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(Color.themeBorder, lineWidth: 1)
                        )

                        // Scientific Literature Card
                        VStack(alignment: .leading, spacing: 14) {
                            Text("Scientific Literature")
                                .font(.headline)
                                .foregroundColor(.themeText)
                            
                            Text("Ingredient microbiome effects are derived from the following peer-reviewed studies, organized by topic:")
                                .font(.caption)
                                .foregroundColor(.themeSecondary)
                            
                            LiteratureSection(title: "General Microbiome & Diet", items: [
                                LiteratureItem(text: "Clemente et al. *The impact of the gut microbiota on human health: an integrative view.* Cell, 2012.", url: "https://doi.org/10.1016/j.cell.2012.01.035"),
                                LiteratureItem(text: "Sonnenburg & Bäckhed. *Diet–microbiota interactions in health are controlled by intestinal nitrogen source constraints.* Nature, 2016.", url: "https://doi.org/10.1038/nature18849"),
                                LiteratureItem(text: "Zinöcker & Lindseth. *The Western Diet–Microbiome-Host Interaction and Its Role in Metabolic Disease.* Nutrients, 2018.", url: "https://doi.org/10.3390/nu10030365"),
                                LiteratureItem(text: "Wastyk et al. *Gut-microbiota-targeted diets modulate human immune status.* Cell, 2021.", url: "https://doi.org/10.1016/j.cell.2021.06.019")
                            ])

                            LiteratureSection(title: "Dietary Fiber, Prebiotics & SCFA", items: [
                                LiteratureItem(text: "Slavin. *Fiber and Prebiotics: Mechanisms and Health Benefits.* Nutrients, 2013.", url: "https://doi.org/10.3390/nu5041417"),
                                LiteratureItem(text: "Kovatcheva-Datchary et al. *Dietary Fiber-Induced Improvement in Glucose Metabolism Is Associated with Increased Abundance of Prevotella.* Cell Metabolism, 2015.", url: "https://doi.org/10.1016/j.cmet.2015.10.001"),
                                LiteratureItem(text: "Desai et al. *A Dietary Fiber-Deprived Gut Microbiota Degrades the Colonic Mucus Barrier and Enhances Pathogen Susceptibility.* Cell, 2016.", url: "https://doi.org/10.1016/j.cell.2016.10.043"),
                                LiteratureItem(text: "Baxter et al. *Dynamics of Human Gut Microbiota and Short-Chain Fatty Acids in Response to Dietary Interventions with Three Fermentable Fibers.* mBio, 2019.", url: "https://doi.org/10.1128/mBio.02566-18"),
                                LiteratureItem(text: "Dahl et al. *A dietary fiber supplement improves gut microbiota diversity.* ISME J, 2023.", url: "https://doi.org/10.1038/s41396-022-01355-3")
                            ])

                            LiteratureSection(title: "Artificial Sweeteners", items: [
                                LiteratureItem(text: "Suez et al. *Artificial sweeteners induce glucose intolerance by altering the gut microbiota.* Nature, 2014.", url: "https://doi.org/10.1038/nature13793"),
                                LiteratureItem(text: "Bian et al. *Gut Microbiome Response to Sucralose and Its Potential Role in Inducing Liver Inflammation in Mice.* Front. Physiol., 2017.", url: "https://doi.org/10.3389/fphys.2017.00487"),
                                LiteratureItem(text: "Ruiz-Ojeda et al. *Effects of Sweeteners on the Gut Microbiota: A Review of Experimental Studies and Clinical Trials.* Adv. Nutr., 2019.", url: "https://doi.org/10.1093/advances/nmy037")
                            ])

                            LiteratureSection(title: "Emulsifiers & Food Additives", items: [
                                LiteratureItem(text: "Chassaing et al. *Dietary emulsifiers impact the mouse gut microbiota promoting colitis and metabolic syndrome.* Nature, 2015.", url: "https://doi.org/10.1038/nature14232"),
                                LiteratureItem(text: "Bhattacharyya & Tobacman. *Molecular signature of kappa-carrageenan mimics chondroitin-4-sulfate and dermatan sulfate and enables interaction with arylsulfatase B.* J. Nutr. Biochem., 2012.", url: "https://doi.org/10.1016/j.jnutbio.2011.05.012"),
                                LiteratureItem(text: "Bettini et al. *Food-grade TiO2 impairs intestinal and systemic immune homeostasis, initiates preneoplastic lesions and promotes aberrant crypt development in the rat colon.* Sci. Rep., 2017.", url: "https://doi.org/10.1038/srep40373"),
                                LiteratureItem(text: "Niaz et al. *Extensive use of monosodium glutamate: A threat to public health?* EXCLI J., 2018.", url: "https://doi.org/10.17179/excli2018-1092")
                            ])

                            LiteratureSection(title: "Food Colorants", items: [
                                LiteratureItem(text: "He et al. *Food colorants metabolized by commensal bacteria promote colitis in mice with dysregulated expression of interleukin-23.* Cell Metabolism, 2021.", url: "https://doi.org/10.1016/j.cmet.2021.04.015"),
                                LiteratureItem(text: "Kwon et al. *Chronic exposure to synthetic food colorant Allura Red AC promotes susceptibility to experimental colitis via intestinal serotonin in mice.* Nat. Commun., 2022.", url: "https://doi.org/10.1038/s41467-022-35309-y")
                            ])

                            LiteratureSection(title: "Preservatives", items: [
                                LiteratureItem(text: "Nagpal et al. *Distinct Gut Microbiota Signatures in Mice Treated with Commonly Used Food Preservatives.* Microorganisms, 2021.", url: "https://doi.org/10.3390/microorganisms9112311"),
                                LiteratureItem(text: "Li et al. *Systematic evaluation of antimicrobial food preservatives on glucose metabolism and gut microbiota in healthy mice.* npj Science of Food, 2022.", url: "https://doi.org/10.1038/s41538-022-00158-y"),
                                LiteratureItem(text: "Xiao et al. *Effects of potassium sorbate on systemic inflammation and gut microbiota in normal mice.* Food Chem. Toxicol., 2024.", url: "https://doi.org/10.1016/j.fct.2024.114443")
                            ])

                            LiteratureSection(title: "Polyols & Sugar Alcohols", items: [
                                LiteratureItem(text: "Mäkinen. *Sugar Alcohol Sweeteners as Alternatives to Sugar with Special Consideration of Xylitol.* Med. Princ. Pract., 2011.", url: "https://doi.org/10.1159/000324534"),
                                LiteratureItem(text: "Uebanso et al. *Effects of Consuming Xylitol on Gut Microbiota and Lipid Metabolism in Mice.* Nutrients, 2017.", url: "https://doi.org/10.3390/nu9070756")
                            ])
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

                        // Footer
                        VStack(alignment: .leading, spacing: 4) {
                            Text("For educational purposes only. Not intended as medical advice.")
                                .font(.system(size: 11))
                                .italic()
                                .foregroundColor(.themeSecondary)
                            Text("Data sourced from Open Food Facts and other public nutrition databases.")
                                .font(.system(size: 11))
                                .foregroundColor(.themeSecondary)
                        }
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

// Subviews below
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

struct StepRowWithList: View {
    let number: String
    let title: String
    let desc: String
    let items: [String]
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Text(number)
                .font(.system(size: 12, weight: .bold))
                .foregroundColor(.themeBg)
                .frame(width: 20, height: 20)
                .background(Color.themeAccent)
                .clipShape(Circle())
                .padding(.top, 2)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.system(size: 13, weight: .bold))
                    .foregroundColor(.themeText)
                Text(desc)
                    .font(.system(size: 12))
                    .foregroundColor(.themeSecondary)
                
                VStack(alignment: .leading, spacing: 2) {
                    ForEach(items, id: \.self) { item in
                        HStack(alignment: .top, spacing: 6) {
                            Text("•")
                                .font(.system(size: 12))
                                .foregroundColor(.themeSecondary)
                            Text(item)
                                .font(.system(size: 12))
                                .foregroundColor(.themeSecondary)
                        }
                    }
                }
                .padding(.leading, 8)
            }
        }
    }
}

struct BulletRow: View {
    let title: String
    let desc: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 8) {
            Text("•")
                .font(.system(size: 14))
                .foregroundColor(.themeText)
            
            Text("**\(title)** — \(desc)")
                .font(.system(size: 13))
                .foregroundColor(.themeSecondary)
        }
    }
}

struct LinkRow: View {
    let title: String
    let desc: String
    let url: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 8) {
            Text("•")
                .font(.system(size: 14))
                .foregroundColor(.themeText)
            
            Text("[\(title)](\(url)) — \(desc)")
                .font(.system(size: 13))
                .foregroundColor(.themeSecondary)
                .tint(.themeAccent)
        }
    }
}

struct LiteratureSection: View {
    let title: String
    let items: [LiteratureItem]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.system(size: 13, weight: .bold))
                .foregroundColor(.themeText)
                .padding(.top, 4)
            
            ForEach(Array(items.enumerated()), id: \.element.id) { index, item in
                HStack(alignment: .top, spacing: 8) {
                    Text("\(index + 1).")
                        .font(.system(size: 12))
                        .foregroundColor(.themeSecondary)
                        .frame(width: 16, alignment: .trailing)
                    
                    Text("\(item.text) [\(item.url)](\(item.url))")
                        .font(.system(size: 12))
                        .foregroundColor(.themeSecondary)
                        .tint(.themeAccent)
                }
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
