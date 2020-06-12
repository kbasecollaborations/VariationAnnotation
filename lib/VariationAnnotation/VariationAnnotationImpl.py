# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import uuid
import os
import shutil
from installed_clients.VariationUtilClient import VariationUtil
from installed_clients.KBaseReportClient import KBaseReport
from VariationAnnotation.Utils.SnpEffUtils import SnpEffUtils
from VariationAnnotation.Utils.DownloadUtils import DownloadUtils
from installed_clients.WorkspaceClient import Workspace as Workspace

#END_HEADER


class VariationAnnotation:
    '''
    Module Name:
    VariationAnnotation

    Module Description:
    A KBase module: VariationAnnotation
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/man4ish/VariationAnnotation.git"
    GIT_COMMIT_HASH = "233ab11cd942b99c960f7b83aaee2b3800685bb4"

    #BEGIN_CLASS_HEADER
    def build_genome_index(self, genome_ref):
        #Downloads gff, fasta and puts it in the right directory
        # and returns the genome_index name that can be used by snpeff.jar
        #TODO: READ GENOME TAXONOMY from genome_ref and
        # TODO: Get genome taxonomy/classification from user so that There
        # is no confusion.
        pass
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.VU = VariationUtil(self.callback_url)
        self.SU = SnpEffUtils()
        self.DU = DownloadUtils()
        self.config = config
        #self.snpeff=<path_to_snpeff>
        #END_CONSTRUCTOR
        pass


    def annotate_variants(self, ctx, params):
        """
        This method extracts VCF from variation object,
        runs SNPEFF workflow (http://snpeff.sourceforge.net/SnpEff_manual.html)
        and annotate and predict the effects of genetic variants
        (such as amino acid changes)
        :param params: instance of type "input_params" (variation_ref:
           Reference to Variation object out_variation_name: Name by which
           the output object will be saved) -> structure: parameter
           "variation_ref" of String, parameter "out_variation_name" of String
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN annotate_variants
        # Validate the parameters
        # Extract vcf from variation using VariationUtil
    #    output_dir = os.path.join(self.scratch, str(uuid.uuid4()))
    #    os.mkdir(output_dir)
    #    #filename = os.path.join(output_dir, "variation.vcf.gz")

    #    print(filename)
    #    vcf_path = self.VU.get_variation_as_vcf({
    #        'variation_ref': params['variation_ref'],
    #        'filename':filename
    #    })
        vcf_path = "/kb/module/work/variation.vcf.gz"
        print (vcf_path)
        # TODO: Need to think through how to get this from the USERS
        # because variation_ref may or may not have a genome_ref field filled in
        # our spec.json may require some work
        # There is a chance that user may provide wrong genome as input if we don't deal with this properly
        # params['genome_ref']


        # Download gff and assembly based on geome_ref

        #gff_path = .....
        #assembly_path ...


        workspace = params['workspace_name']
        self.ws_url = self.config['workspace-url']
        self.ws = Workspace(self.ws_url, token=ctx['token'])



        filename = "/kb/module/work/variation.vcf"
        output_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        os.mkdir(output_dir)

        shutil.copytree("/kb/module/deps/snp_eff", output_dir + "/snp_eff")

        variation_ref= params['variation_ref']
        variation_obj = self.ws.get_objects2({'objects': [{'ref':variation_ref}]})['data'][0]

        assembly_ref= variation_obj['data']['assembly_ref']
        assembly_path = self.DU.get_assembly(assembly_ref, output_dir)

        gff_ref = params['gff_ref']
        gff_path = self.DU.get_gff(gff_ref, output_dir)

        vcf_path = self.VU.get_variation_as_vcf({
                'variation_ref': params['variation_ref'],
                'filename':filename
            })

        genome_index_name = self.SU.build_genome(gff_path, assembly_path, output_dir)
        annotated_vcf_path = self.SU.annotate_variants(genome_index_name, vcf_path['path'], params, output_dir)

        #self.VU.   #upload file to shock

        # TODO: Add parameters for snpeff in parameters
        # Parse the snpeff parameters from params and build snpeff command
        # TODO: We are hardcoding this for now

        #
        output = {
            "x":vcf_path
        }
        #END annotate_variants

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method annotate_variants return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
