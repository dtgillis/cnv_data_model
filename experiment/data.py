__author__ = 'dtgillis'

import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'cnv_data.settings'; import django
from experiment import models as exp


def create_sample_from_mapping(sample_line, xt2):

    line = sample_line.strip(os.linesep)
    fields = line.split()
    sample_name = fields[0]
    bam_file = fields[1]
    sample = exp.Sample.objects.create_sample_model(sample_name, bam_file, xt2)
    sample.save()


def create_chrm_record(chrm_line):

    fields = chrm_line.strip(os.linesep).split()
    chrom_name = fields[0]
    chrm_alt = fields[1]
    chromosome = exp.Chromosome.objects.create_chromosome(chrom_name, chrm_alt)
    chromosome.save()


def create_interval_record(interval_line, chrm_obj):

    fields = interval_line.strip(os.linesep).split(":")
    chrm_name = fields[0]
    if str(chrm_obj.chromosome_name) != chrm_name:
        chrm_obj = exp.Chromosome.objects.filter(chromosome_name=chrm_name).get()
    start = int(fields[1].split("-")[0])
    end = int(fields[1].split("-")[1])
    interval = exp.GenomeInterval(chromosome=chrm_obj, start=start, end=end)
    return interval, chrm_obj


def build_data(base_dir):
    #different file names
    xt2_sample_list = 'xt2_mapping.dat'
    old_bam_list = 'old_bam_map.dat'
    chrm_list_file = 'chrm_list'
    interval_list_file = 'agilent.interval_list'
    ## load sample data into database

    # xt2 samples
    for line in open(base_dir + os.sep + 'sample' + os.sep + xt2_sample_list, 'r'):
        if len(line) > 0:
            create_sample_from_mapping(line, True)

    for line in open(base_dir + os.sep + 'sample' + os.sep + old_bam_list, 'r'):
        if len(line) > 0:
            create_sample_from_mapping(line, False)

    # load up chromosome table

    for line in open(base_dir + os.sep + 'interval' + os.sep + chrm_list_file):
        if len(line) > 0:
            create_chrm_record(line)

    interval_list = []
    chrm_obj = exp.Chromosome.objects.filter(chromosome_name='NC_000001.10').get()
    for line in open(base_dir + os.sep + 'interval' + os.sep + interval_list_file):

        if len(line) > 0:
            interval, chrm_obj = create_interval_record(line, chrm_obj)
            interval_list.append(interval)

    exp.GenomeInterval.objects.bulk_create(interval_list)


def build_sample_group_list(dir):

    sample_group_list_dir = dir + os.sep + 'sample_group'
    group_list = []
    for sample_group_list in ['bam_list_a', 'bam_list_b', 'bam_list_c']:
        for line in open(sample_group_list_dir + os.sep + sample_group_list, 'r'):
            bam_file_name = line.split(os.sep)[-1].strip(os.linesep)
            sample = exp.Sample.objects.all().filter(bam_file=bam_file_name).get()
            sample_group = exp.SampleGroup(sample_name=sample.sample_name, group_name=sample_group_list)
            group_list.append(sample_group)

    exp.SampleGroup.objects.bulk_create(group_list)

def build_software_data():

    software_names = ['exome_depth', ]

    software_list = []
    for software_name in software_names:

        software_list.append(exp.Software(software_name=software_name, extra_params='non-normal input'))

    exp.Software.objects.bulk_create(software_list)


if __name__ == '__main__':
    #build_data('/home/dtgillis/sim_capture/django_data')
    #build_sample_group_list('/home/dtgillis/sim_capture/django_data')
    build_software_data()