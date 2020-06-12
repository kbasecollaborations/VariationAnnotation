/*
A KBase module: VariationAnnotation
*/

module VariationAnnotation {

    /*
        variation_ref: Reference to Variation object
        out_variation_name: Name by which the output object will be saved
    */
    typedef structure {
        string variation_ref;
        string gff_ref;
        int canon;
        int no_downstream;
        int no_intergenic;
        int no_intron;
        int no_upstream;
        int no_utr;
        string out_variation_name;
    } input_params;

    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This method extracts VCF from variation object,
        runs SNPEFF workflow (http://snpeff.sourceforge.net/SnpEff_manual.html)
        and annotate and predict the effects of genetic variants
        (such as amino acid changes)
    */
    funcdef annotate_variants(input_params params) returns (ReportResults output) authentication required;

};
