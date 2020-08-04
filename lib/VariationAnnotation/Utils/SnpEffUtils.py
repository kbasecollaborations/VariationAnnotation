import shutil
import os
import subprocess


class SnpEffUtils:
    def init():
        pass

    def run_cmd(self, cmd):
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stdout:
                print("ret> ", process.returncode)
                print("OK> output ", stdout)
            if stderr:
                print("ret> ", process.returncode)
                print("Error> error ", stderr.strip())

        except OSError as e:
            print("OSError > ", e.errno)
            print("OSError > ", e.strerror)
            print("OSError > ", e.filename)

    def build_genome(self, gff_path, assembly_path, output_dir):
        # shutil.copytree("/kb/module/deps/snp_eff", output_dir + "/snp_eff")   #Todo copy latest jar file
        shutil.copyfile(gff_path, os.path.join(output_dir, "snp_eff/data/kbase_v1/genes.gff"))
        # shutil.copyfile(assembly_path, os.path.join(output_dir,"snp_eff/data/kbase_v1"))

        build_cmd = "java -Xmx4g -jar " + os.path.join(output_dir, "snp_eff/snpEff.jar") + " build -gff3 -v kbase_v1"
        self.run_cmd(build_cmd)
        return "kbase_v1"

    def validate_params(self, params):
        if 'variation_ref' not in params:
            raise ValueError('required variation_ref field was not defined')
        elif 'canon' not in params:
            raise ValueError('required canon field was not defined')
        elif 'no_downstream' not in params:
            raise ValueError('required no_downstream field was not defined')
        elif 'no_intergenic' not in params:
            raise ValueError('required no_intergenic field was not defined')
        elif 'no_intron' not in params:
            raise ValueError('required no_intron field was not defined')
        elif 'no_upstream' not in params:
            raise ValueError('required no_upstream field was not defined')
        elif 'no_utr' not in params:
            raise ValueError('required no_utr field was not defined')
        elif 'output_object_name' not in params:
            raise ValueError('required output_object_name field was not defined')

    def annotate_variants(self, genome_index_name, vcf_path, params, output_dir):
        '''
        cd /kb/module/work/tmp/b3043710-802c-4acf-8996-9dbd54163e6b/snp_eff/ && java -jar /kb/module/work/tmp/b3043710-802c-4acf-8996-9dbd54163e6b/snp_eff/snpEff.jar -v -canon -no-downstream -no-intergenic -no-upstream kbase_v1 /kb/module/work/tmp/variation.vcf |bgzip -c  > /kb/module/work/tmp/variation.ANN.vcf.gz
        '''
        snp_eff_cmd = ["cd"]
        snp_eff_cmd.append(os.path.join(output_dir, "snp_eff/"))
        snp_eff_cmd.append("&&")
        snp_eff_cmd.append("java")
        snp_eff_cmd.append("-Xmx4g")
        snp_eff_cmd.append("-jar")
        snp_eff_cmd.append(os.path.join(output_dir, "snp_eff/snpEff.jar"))
        snp_eff_cmd.append("-v")

        if(params.get("canon")):
            snp_eff_cmd.append("-canon")
        if(params.get("no_downstream")):
            snp_eff_cmd.append("-no-downstream")
        if(params.get("no_intergenic")):
            snp_eff_cmd.append("-no-intergenic")
        if(params.get("no_intron")):
            snp_eff_cmd.append("-no-intron")
        if(params.get("no_upstream")):
            snp_eff_cmd.append("-no-upstream")
        if(params.get("no_utr")):
            snp_eff_cmd.append("-no-utr")

        snp_eff_cmd.append(genome_index_name)
        input_vcf_path = vcf_path.replace(".gz", "")
        snp_eff_cmd.append(input_vcf_path)
        out_path = vcf_path.replace(".vcf", ".ANN.vcf")
        snp_eff_cmd.extend(["|bgzip", "-c "])
        snp_eff_cmd.extend([">", out_path])
        snp_eff_command = " ".join(snp_eff_cmd)
        print("^^^^^^" + snp_eff_command + "^^^^^^^")
        self.run_cmd(snp_eff_command)

        return out_path
