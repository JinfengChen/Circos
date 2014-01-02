#!/usr/bin/perl
use Getopt::Long;
use FindBin qw($Bin);

GetOptions (\%opt, "repeat_gff:s", "gene_gff:s", "chrlen:s", "prefix:s", "project:s", "help");


my $help=<<USAGE;
The pipeline prepare data for drawing chromosome view using circos.
perl ../scripts/PreDraw.pl --repeat_gff ../../input/MSU_r7.fa.RepeatMasker.out.gff --gene_gff ../../input/MSU7.gene.gff --chrlen ../../input/MSU7.chrlen
--repeat_gff:
--gene_gff:
--chrlen: Chr1\t43270923
--prefix: prefix for data
--project: dir for output

USAGE


if ($opt{help} or keys %opt < 1){
    print "$help\n";
    exit();
} 

$opt{project} ||= "Draw_Data";
$opt{prefix}  ||= "MSU7";
`mkdir $opt{project}` unless (-e $opt{project});

`sed 's/Chr/A/' $opt{chrlen} > $opt{project}/$opt{prefix}.chrlen`;
`cp $opt{chrlen} $opt{project}/$opt{prefix}.chrlen.raw`;
splitTE($opt{repeat_gff}, "$opt{project}/$opt{prefix}");
cpGene($opt{gene_gff}, "$opt{project}/$opt{prefix}");
prepare($opt{project}, $opt{prefix}, "$opt{project}/$opt{prefix}.chrlen");

###################################################

sub prepare
{
my ($dir,$species,$len)=@_;
system ("perl $Bin/remove_redundance.pl $dir/$species.RT.gff $dir/$species.DNA.gff $dir/$species.Gene.gff");
system ("perl $Bin/distri_data_pre.pl $len distri.gff.nr.out");
`cat A*.data.distri > $opt{project}/$opt{prefix}.data.distri`;
`perl $Bin/circos_head.pl --chrlen $opt{chrlen} > $opt{project}/$opt{prefix}.circos.head`;
`perl $Bin/get_dens_histogram.pl $opt{project}/$opt{prefix}.data.distri $opt{project}/$opt{prefix}.circos.head RT > $opt{project}/$opt{prefix}.RT.histogram.txt`;
`perl $Bin/get_dens_histogram.pl $opt{project}/$opt{prefix}.data.distri $opt{project}/$opt{prefix}.circos.head DNA > $opt{project}/$opt{prefix}.DNA.histogram.txt`;
`perl $Bin/get_dens_histogram.pl $opt{project}/$opt{prefix}.data.distri $opt{project}/$opt{prefix}.circos.head exon > $opt{project}/$opt{prefix}.exon.histogram.txt`;
system ("rm A*.data.distri distri.gff.nr.out");
}

sub cpGene
{
my ($gff,$prefix)=@_;
my $target=$prefix.".Gene.gff";
open IN, "$gff" or die "$!";
open GENE, ">$target" or die "$!";
while(<IN>){
   next if ($_ eq "");
   next if ($_ =~/^#/);
   my @temp=split("\t",$_);
   $temp[0]=~s/Chr/A/;
   my $line=join("\t",@temp);
   print GENE "$line"; 
}
close GENE;
close IN;
}


sub splitTE
{
my ($gff,$prefix)=@_;
open IN, "$gff" or die "$!";
open DNA, ">$prefix.DNA.gff" or die "$!";
open RT, ">$prefix.RT.gff" or die "$!";
open CACTA, ">$prefix.CACTA.gff" or die "$!";
open MITE, ">$prefix.MITE.gff" or die "$!";
open MUDR, ">$prefix.MUDR.gff" or die "$!";
open GYPSY, ">$prefix.GYPSY.gff" or die "$!";
open COPIA, ">$prefix.COPIA.gff" or die "$!";
while(<IN>){
    next if ($_ eq "");
    next if ($_ =~/^#/);
    my @temp=split("\t",$_);
    $temp[0]=~s/Chr/A/;
    my $line=join("\t",@temp);
    my $TE_class= $1 if ($temp[8] =~ /Class=([^;]+);*/);
    #print "$TE_class\n";
    if ($TE_class =~/^DNA/){
       print DNA "$line";
    }elsif($TE_class=~/^LTR/){
       print RT "$line";
    } 
    if ($TE_class=~/En-Spm/i){
       print CACTA "$line"; 
    }elsif($TE_class=~/MuDR/i){
       print MUDR "$line";
    }elsif($TE_class=~/Stowaway/i or $TE_class=~/Tourist/i or $TE_class=~/MITE/i){
       print MITE "$line";
    }elsif($TE_class=~/Gypsy/i){
       print GYPSY "$line";
    }elsif($TE_class=~/Copia/i){
       print COPIA "$line";
    }
}
close GYPSY;
close COPIS;
close MUDR;
close MITE;
close CACTA;
close DNA;
close RT;
close IN;
}



