import csv

NanoporeNamesList = ["Oxford Nanopore Artic", "ONT_ARTIC", "Oxford Nanopore", "Oxford Nanopore GridION",
                     "Oxford Nanopore ARTIC", "MinION Oxford Nanopore", "Nanopore MinION", "MinION", "Nanopore ARTIC",
                     "GridION", "Nanopore MinIon", "Ion Torrent", "ONT ARTIC", "Nanopore minION",
                     "Nanopore MinION Mk1C", "Oxford Nanopore Technologies ARTIC", "Nanopore GridION",
                     "Nanopore GridION, ARTIC V3 protocol", "Oxford Nanopore MinION", "Nanopore",
                     "Oxford Nanopore - Artic", "Nanopore GridION", "Oxford Nanopore Technologies ARTIC",
                     "Nanopore GridION -- ARTIC protocol", "Oxford Nanopore Technologies", "Nanopore- MinION",
                     "IonTorrent", "Ion Torrent S5", "Ion Torrent S5 XL- Ion AmpliSeq SARS-CoV-2",
                     "Nanopore_GridION_--_ARTIC_protocol", "Ion_Torrent", "Nanopore,_MinION",
                     "IonTorrent", "Nanopore_GridION_-_ARTIC_protocol", "ClearLabs_ONT_GridION",
                     "Ion_AmpliSeq?_SARS-CoV-2_Research_Panel_and_Ion_Proton?",
                     "Nanopore_GridIon,_ARTIC_protocol_v3", "MinION", "ONT_ARTIC",
                     "Oxford_Nanopore_Technologies_GridION_X5_(Flongle_flow-cell)",
                     "Oxford_Nanopore_Technologies,_GridION_X5", "ONT_GridION_", "Oxford_Nanopore/",
                     "Nanopore_/Flongle", "Nanopre", "ONT_GridION", "GridION", "multiplex-pcr_nanopore",
                     "Nanopore_GridION_--_ARTIC_sequencing_protocol", "Nanpore_GridION_--_ARTIC_protocol"]

IlluminaNamesList = ["Illumina NextSeq", "MiSeq", "Illumina NexteraFlex", "Illumina MiniSeq, MiSeq, or HiSeq",
                     "Illumina Miseq, 1200bp", "NextSeq 550", "Illumina_NexteraFlex", "Illumina HiSeq",
                     "Illumina Miseq", "Illumina NextSeq 2000", "Illumina MiSeq", "NovaSeq 6000", "Illumina Nextseq",
                     "Illumina MiniSeq", "Illumina nextSeq", "Illumina NovaSeq 6000", "Illumina MiSeq, 1200bp",
                     "Illumina Nextera Flex", "Illumina NextSeq 550", "Illumina", "Illumina iSeq 100",
                     "Illumina NovaSeq", "Illumina MiSeq; ARTIC V3",
                     "Illumina MiSeq DX- (2x250bp- Amplicon- LNS primer scheme)",
                     "Illumina NextSeq 500", "ILLUMINA NovaSeq", "Illumina NextSeq500", "nCoV_NextSeq", "Illumina iSeq",
                     "Illumina NextSeq2000", "illumina NextSeq500", "illumina NextSeq2000", "Illumina- MiSeq",
                     "Illumna MiSeq", "Illumina,_MiSeq", "Illumna_MiSeq"
                                                         "Illumina iSeq- 2 x 150bp paired end reads- ARTIC V3- "
                                                         "Nextera Flex prep",
                     "Illumina Nextseq 550",
                     "llumina NextSeq", "Illumina MiniSeq (Amplicon- ARTIC primer set V1)", "Illumina Novaseq",
                     "Illumina NextSeq 500- Freed-Silander v1-1200bp (see https://doi.org/10.1101/2020.05.28.122648)",
                     "nCoV MiSeq", "NovaSeq", "ILLUMINA MiSeq",
                     "Illumina_MiSeq_DX,_(2x250bp,_Amplicon,_LNS_primer_scheme)"
                     "Illumina_iSeq,_2_x_150bp_paired_end_reads,_ARTIC_V3,_Nextera_Flex_prep",
                     "llumina_NextSeq", "Illumina_MiniSeq_(Amplicon,_ARTIC_primer_set_V1)", "Illumna_NextSeq",
                     "NextSeq", "Ribo-depleted,_Illumina_Novaseq", "nCoV_MiSeq", "NovaSeq",
                     "Illumina__with_tiling_multiplex_PCR_(artic-ncov2019_protocol)",
                     "Illumina_MiniSeq,_(2x150bp,_Amplicon,_LNS_primer_scheme)", "MiSeq",
                     "Illumina_MiSeq,_ARTICProtocol_v3", "Illumina__(Ribo-depleted)",
                     "Illumina_,_2_x_250bp_paired_end_reads,_ARTIC_V3,_Nextera_Flex_prep",
                     "Illumina_,_ARTIC_protocol_v3", "Illumina_;_ARTIC_V3", "MiniSeq",
                     "Illumina__/_Respiratory_Virus_Oligo_Panel", "Targeted_capture,_Illumina_",
                     "Swift_Amplicon_SARS-CoV-2_Panel+Illumina_MiniSeq", "Illumina_;_Swift_SNAP_SARS-Cov-2_Panel",
                     "ARTIC_protocol+Illumina_NestSeq500", "Illumina_,_assembled_sequences",
                     "Illumina_,_ARTICProtocol", "Amplicon_(Swift),_Illumina_", "Illumina_Next-Seq",
                     "Illumina_,_(2x250bp,_Amplicon,_LNS_primer_scheme)",
                     "Illumina_,_2_x_150bp_paired_end_reads,_ARTIC_V3,_Nextera_Flex_prep",
                     "Illumina_;_ARTIC_v.3", "ARTIC_protocol_+_Illumina_", "ARTIC_protocol+Illumina_",
                     "Illumina__(2_x_250bp_paired_end_reads,_ARTIC_V3,_TruSeq_Nano_ligation_prep)",
                     "_V3_2x75_paired_reads_(Illumina)_+Nextera_Flex_Enrichment_Library_with_Respiratory_Virus_Oligo",
                     "Illumina,_assembled_sequences", "llumina_", "lllumina_HiSeq_X", "ARTIC_+_Illumina_",
                     "Illumina__and_Sanger", "Illumina__(Amplicon,_ARTIC_primer_set)",
                     "Illumina_,_2_x_250bp_paired_end_reads,_ARTIC_v2,_Kapa_ligation_prep",
                     "Illumina_/_iSeq", "iSeq100", "Illumina_Artic-V3",
                     "Illumina_Nano__-_Zymo-Seq_RiboFree_Total_RNA_Library_Kit"]

unknownSequencerList = ["MGI CleanPlex", "MGI", "unknown", "PacBio", "MGI DNBSEQ-G400", "Nanopore MinION- Sanger",
                        "Illumina Miseq / Sanger", "MGISEQ-T7", "unknown"
                                                                "CleanPlex SARS-CoV-2 Research and Surveillance "
                                                                "Panel; Illumina NextSeq 500",
                        "PacBio", "MGI_CleanPlex", "None", "MGI_DNBSEQ-G400", "Nanopore_MinION,_Sanger",
                        "Illumina_Miseq_/_Sanger", "_S5", "_S5_XL,_Ion_AmpliSeq_SARS-CoV-2",
                        "I_500,_Freed-Silander_v1-1200bp_(see_https://doi.org/10.1101/2020.05.28.122648)",
                        "MGISEQ-T7", "CleanPlex_SARS-CoV-2_Research_and_Surveillance_Panel;_I_500",
                        "_550", "ClearLabs", "I_500,_Freed-Silander_v1-1200bp", "Pacific_Biosciences_Sequel_I",
                        "Sanger_dideoxy_sequencing", "Illumina_,_Sanger", ",_Gene_Studio",
                        "I_500,_combined_data_from_ARTIC_v3-400bp_and_Freed-Silander_v1-1200bp_(see_https://do",
                        "_S21", "_sequencing", "Sanger", "Artic", "Ribo-depleted,_I", "BGISEQ-500",
                        "I_with_MSSPE+tiling_multiplex_PCR", "Illumina__+_Nanopore_", "DNBSEQ",
                        "DNBSEQ-G400RS,_MGI_Tech_Co.,_Ltd", "illumina__and_Nanopore_", "I_500,_ARTIC_v3",
                        "_Genexus_System,_Ion_AmpliSeq_SARS-CoV-2", "Nanopore,_Sanger", "MGISEQ2000",
                        "BioelectronSeq_4000", "MGISEQ-G400", "?_Personal_Genome_Machine?_(PGM)_System",
                        "Nanopore__and_Illumina_", "Illumina;_MGI", "Artic+500", "Illumina_;_Nanopore",
                        "metagenomics_BGI", "Sanger,_Nanopore", "MGISEQ_2000", "Immumina_",
                        "I_with_MSSPE,_tiling_multiplex_PCR", "Illumina;_Oxford_Nanopore;_Sanger_dideoxy",
                        "I_500,_combined_data_from_ARTIC_v1-400bp_and_Arbor_Biosciences_myBaits_Expert_SARS-Co",
                        "Illumina__System_+_Sanger", "Illumina_,_Nanopore_"
                        ]


def add_sequencing_technology(metadata_file, input_fasta_file, output_fasta_file):
    write_flag = False
    with open(output_fasta_file, 'a', encoding='utf-8') as outFastaFile:
        with open(input_fasta_file) as infile:
            for line in infile:
                if line.__contains__('>'):
                    accession_id = line.split("|")[1]
                    with open(metadata_file, encoding="utf8") as rf:
                        csv_reader = csv.reader(rf)
                        next(csv_reader)  # skip the header
                        for csvLine in csv_reader:
                            if csvLine.__contains__(accession_id):
                                sequencing_technology = csvLine[9]
                                if IlluminaNamesList.__contains__(sequencing_technology):
                                    sequencing_technology = "Illumina"
                                elif NanoporeNamesList.__contains__(sequencing_technology):
                                    sequencing_technology = "Nanopore"
                                elif unknownSequencerList.__contains__(sequencing_technology):
                                    sequencing_technology = "-"
                                else:
                                    print(sequencing_technology)
                                line = line.strip() + "|" + sequencing_technology
                                outFastaFile.write(str(line) + "\n")
                                write_flag = True
                elif write_flag:
                    outFastaFile.write(line)
                    write_flag = False


# input_file = 'files/input/msa_0206.fasta'
input_file = 'files/input/test_MSA_2.fasta'
# output_file = 'files/input/msa_0206_with_sequencing_technology.fasta'
output_file = 'files/input/test_msa_2_with_sequencing_technology.fasta'
input_metadata_file = 'files/input/Bias/metadata.csv'
# add_sequencing_technology(input_metadata_file, input_file, output_file)
