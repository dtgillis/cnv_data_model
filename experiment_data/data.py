__author__ = 'dtgillis'

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cnv_data.settings'
import experiment.models as exp
import experiment_data.models as exp_data
import glob

def load_cnv_chip_data(in_dir):

    chip_file = 'cma_cnv_calls_real.csv'
    data_list = []
    for line in open(in_dir + os.sep + chip_file, 'r'):

        line = line.strip(os.linesep)

        if len(line) != 0:

            fields = line.split()
            sample_name = fields[0]
            cn_state = int(fields[1])
            chrm_str = 'chr' + fields[2]
            chrm = exp.Chromosome.objects.filter(alternate_name=chrm_str).get()
            start = int(fields[3])
            end = int(fields[4])
            cnv_call = exp_data.CNVChipCall(
                sample_name=sample_name, cn_state=cn_state, chromosome=chrm, start=start, end=end)
            data_list.append(cnv_call)

    exp_data.CNVChipCall.objects.bulk_create(data_list)


def load_cnv_test_data(in_dir, software_name, cnv_file, extra_parameters=None):

    data_list = []
    if extra_parameters is not None:
        software = exp.Software.objects.all().filter(name=software_name)
    else:
        software = exp.Software.objects.all().filter(name=software_name, parameters=extra_parameters)
    for line in open(in_dir + os.sep + cnv_file, 'r'):

        line = line.strip(os.linesep)

        if len(line) > 0:
            pass


def load_bam_list_samples(data_dir):

    os.chdir(data_dir)
    sample_group_list = []
    current_groups = exp.SampleGroup.objects.values_list('group_name', flat=True)

    for bam_list in glob.glob('*'):
        if bam_list not in current_groups:
            for line in open(bam_list, 'r'):
                fields = line.split('/')
                bam_file = fields[-1].strip(os.linesep)
                sample = exp.Sample.objects.filter(bam_file=bam_file).get()
                sample_group_list.append(exp.SampleGroup(sample=sample, group_name=bam_list))

    exp.SampleGroup.objects.bulk_create(sample_group_list)


def assign_cn_state(ratio):

    guess = ratio * 2
    return int(round(guess))


def load_exome_depth_data(data_dir):

    os.chdir(data_dir)
    data_list = []
    software = exp.Software.objects.all().filter(software_name='exome_depth', extra_params='non-normal input').get()
    sample_groups_used = exp_data.CNVSoftwareCall.objects.filter(software=software).values_list('sample_group')
    sample_groups = exp.SampleGroup.objects.filter(pk__in=sample_groups_used).values_list('group_name')
    for data_set_csv in glob.glob('*'):

        data_set = data_set_csv[0:-4]

        if data_set not in sample_groups:
            for line in open(data_set_csv, 'r'):
                fields = line.strip(os.linesep).split(',')
                bam_file = fields[0].replace('.', '-', 1).split('.')[0]
                num_exons = int(fields[4])
                start = int(fields[5])
                end = int(fields[6])
                chrm = fields[7].strip('"')
                bayes_factor = float(fields[9])
                ratio = float(fields[-1])
                cn_state = assign_cn_state(ratio)
                chrm_obj = exp.Chromosome.objects.filter(chromosome_name=chrm).get()
                print bam_file
                sample_obj = exp.Sample.objects.filter(bam_file__startswith=bam_file).get()
                print sample_obj.sample_name, data_set
                group_obj = exp.SampleGroup.objects.filter(
                    sample=sample_obj, group_name=data_set).get()

                data_list.append(
                    exp_data.CNVSoftwareCall(software=software, sample_group=group_obj, chromosome=chrm_obj,
                                             num_exons=num_exons, start=start, end=end,
                                             bayes_factor=bayes_factor, cn_state=cn_state))

    exp_data.CNVSoftwareCall.objects.bulk_create(data_list)


if __name__ == '__main__':
    #load_cnv_chip_data('/home/dtgillis/sim_capture/django_data/truth')
    #load_bam_list_samples('/home/dtgillis/sim_capture/django_data/sample_group')
    load_exome_depth_data('/home/dtgillis/sim_capture/django_data/exome_depth')

