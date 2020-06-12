import os
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil

class DownloadUtils:
    def __init__(self):
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.au = AssemblyUtil(self.callback_url)
        self.gfu = GenomeFileUtil(self.callback_url)
        pass

    def get_gff(self, genome_ref, output_dir):
        gff_filename = os.path.join(output_dir + "/snp_eff/data/kbase_v1", "gene.gff")
        file = self.gfu.genome_to_gff({'genome_ref': genome_ref, 'filename':gff_filename})
        return file['file_path']

    def get_assembly(self, assembly_ref, output_dir):
        assembly_filename = os.path.join(output_dir + "/snp_eff/data/kbase_v1", "sequences.fa")
        file = self.au.get_assembly_as_fasta({
          'ref': assembly_ref, 'filename':assembly_filename
        })
        return file['path']
