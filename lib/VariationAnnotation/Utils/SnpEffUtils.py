import shutil

class SnpEffUtils:
    def init():
        pass

    def run_cmd(self, cmd):
       try:
          process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
          stdout, stderr = process.communicate()
          if stdout:
              print ("ret> ", process.returncode)
              print ("OK> output ", stdout)
          if stderr:
              print ("ret> ", process.returncode)
              print ("Error> error ", stderr.strip())

       except OSError as e:
          print ("OSError > ", e.errno)
          print ("OSError > ", e.strerror)
          print ("OSError > ", e.filename)

    def build_genome(self, gff_path, assembly_path, output_dir):
        shutil.copytree("/kb/module/deps/snp_eff", output_dir)   #Todo copy latest jar file
        stutil.copyfile(gff_path, os.path.join(output_dir,"snp_eff/data/kbase_v1"))
        stutil.copyfile(assembly_path, os.path.join(output_dir,"snp_eff/data/kbase_v1"))

        build_cmd = "java -jar " + os.path.join(output_dir, "snp_eff/snpEff.jar") + " build -gff3 -v kbase_v1"
        self.run_cmd(build_cmd)
        return "kbase_v1"


    def annotate_variants(self, vcf_path, params):
        snp_eff_cmd = ["/kb/module/deployment/bin/snpEff/snpEff.jar"]
        snp_eff_cmd.append("-v")
        snp_eff_cmd.append("-canon")
        snp_eff_cmd.append("-no-intergenic")
        snp_eff_cmd.append("-no-downstream")
        snp_eff_cmd.append("-no-intron")
        snp_eff_cmd.append("-no-upstream")
        input_vcf_path = vcf_path.replace(".gz","")
        snp_eff_cmd.append(input_vcf_path)

        out_path = vcf_path.replace(".vcf", ".ANN.vcf")
        #genome_index_name = self.build_genome(params['genome_ref'])
        genome_index_name = "kbase_v1"     #hardcoded for testing
        snp_eff_cmd.append(genome_index_name)
        snp_eff_cmd.extend(["|bgzip", "-c " ])
        snp_eff_cmd.extend([">",out_path])

        snp_eff_command = " ".join(snp_eff_cmd)
        exit(snp_eff_command)
        self.run_cmd(snp_eff_command)

        return out_path
