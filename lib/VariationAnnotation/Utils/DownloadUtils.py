import os
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil

class DownloadUtils:
    def init(self):
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.assembly_util = AssemblyUtil(self.callback_url)
        self.gfu = GenomeFileUtil(self.callback_url)
        pass

    def get_gff(genome_ref):
        file = self.gfu.genome_to_gff({'genome_ref': genome_ref})
        return file['path']

    def get_assembly(assembly_ref):
        file = self.assembly_util.get_assembly_as_fasta({
               'ref': assembly_workspace_reference
        })
        return file['path']
