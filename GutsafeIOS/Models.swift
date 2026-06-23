import Foundation

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
