#!/usr/bin/perl
use Getopt::Long;
use File::Basename;
use Data::Dumper;
use FindBin qw($Bin);


GetOptions (\%opt, "chrlen:s", "help");


my $help=<<USAGE;

perl $0 --chrlen MSU7.chrlen > circos.MSU7.head

chrlen:
Chr1	43270923
Chr2	35937250
Chr3	36413819
Chr4	35502694
Chr5	29958434
Chr6	31248787
Chr7	29697621
Chr8	28443022
Chr9	23012720
Chr10	23207287
Chr11	29021106
Chr12	27531856

circos.head
chr - Chr1 1 0 43270923 chr1
chr - Chr2 2 0 35937250 chr2
chr - Chr3 3 0 36413819 chr3
chr - Chr4 4 0 35502694 chr4
chr - Chr5 5 0 29958434 chr5
chr - Chr6 6 0 31248787 chr6
chr - Chr7 7 0 29697621 chr7
chr - Chr8 8 0 28443022 chr8
chr - Chr9 9 0 23012720 chr9
chr - Chr10 10 0 23207287 chr10
chr - Chr11 11 0 29021106 chr11
chr - Chr12 12 0 27531856 chr12

USAGE


if ($opt{help} or keys %opt < 1){
    print "$help\n";
    exit();
}

readtable($opt{chrlen});

sub readtable
{
my ($file)=@_;
my %hash;
open IN, "$file" or die "$!";
while(<IN>){
    chomp $_;
    next if ($_=~/^$/);
    my @unit=split("\t",$_);
    my $chrn = $1 if ($unit[0]=~/(\d+)/);
    print "chr - $unit[0] $chrn 0 $unit[1] chr$chrn\n";
}
close IN;
return \%hash;
}


