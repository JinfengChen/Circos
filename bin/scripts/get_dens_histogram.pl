#!usr/bin/perl
use strict;

die "perl $0 <data> <len> <feature>\n" if(@ARGV != 3);
my ($data, $len, $feature) = @ARGV;

my %len  = ();
open(FH, $len) || die $!;
while(<FH>)
{
	chomp;
	my @tmp = split /\s+/;
	$len{$tmp[2]} = $tmp[5];
}
close FH;

=pod
open(OUT, ">dens.color.conf") || die $!;
my @color;
my $num = 0;
my @arr = (0, 0, 128);
for my $i (128..254)
{
	push @color, "dens$num";
	print OUT "dens$num = $arr[0],$arr[1],$arr[2]\n";
	$arr[2]++;
	$num++;
}
for my $i (0..254)
{
	$arr[1]++;
	push @color, "dens$num";
	print OUT "dens$num = $arr[0],$arr[1],$arr[2]\n";
	$num++;
}
for my $i (0..254)
{
	$arr[0]++;
	$arr[2]--;
	push @color, "dens$num";
	print OUT "dens$num = $arr[0],$arr[1],$arr[2]\n";
	$num++;
}
for my $i (0..254)
{
	$arr[1]--;
	push @color, "dens$num";
	print OUT "dens$num = $arr[0],$arr[1],$arr[2]\n";
	$num++;
}
for my $i (0..126)
{
	$arr[0]--;
	push @color, "dens$num";
	print OUT "dens$num = $arr[0],$arr[1],$arr[2]\n";
	$num++;
}

close OUT;
=cut

#A01     LTR-RT/gypsy    0       13.2098 433
my (%max, %min);
my %data;
open(FH, $data) || die $!;
while(<FH>)
{
	chomp;
	my @tmp = split /\t/;
        next unless ($tmp[1]=~/$feature/);
	$tmp[0] =~ s/A/Chr/;
        #print $tmp[0], $tmp[1], "\n";
	$max{$tmp[0]} = 0 if(not exists $max{$tmp[0]});
	$min{$tmp[0]} = 1 if(not exists $min{$tmp[0]});
	my $start = $tmp[2] * 100000;
	my $stop = $start + 99999;
	$stop = $len{$tmp[0]} if($stop > $len{$tmp[0]});
	push @{$data{$tmp[0]}}, [$start, $stop, $tmp[3]];
	$max{$tmp[0]} = $tmp[3] if($tmp[3] > $max{$tmp[0]});
	$min{$tmp[0]} = $tmp[3] if($tmp[3] < $min{$tmp[0]});
}
close FH;
for my $id (sort {$a <=> $b or $a cmp $b} keys %data)
{
        #print $id, "\n";
	for (my $i=0; $i < @{$data{$id}}; $i++)
	{
                #print $i, "\n";
                print "$id $data{$id}[$i][0] $data{$id}[$i][1] $data{$id}[$i][2]\n";
	}
}

