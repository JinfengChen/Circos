perl get_highlight.pl circos.head evidence.nonblock.list
perl get_dens_highlight.pl example circos.head >example.highlight.txt
cat colors.conf dens.color.conf >all.colors.conf
perl get_line.pl segmental_result_sim90.nr.filter.cluster >line.txt
perl /share/raid1/genome/bin/circos -conf circos.SD.conf
echo "generate position for chr label"
awk '{print $3,int ($6/2),int ($6/2),$3}' circos.head > circos.text
echo "rice gene and te, sd"
perl get_dens_histogram.pl Rice.distri circos.head > Rice.exon.histogram.txt
perl get_dens_histogram.pl Rice.distri circos.head > Rice.RT.histogram.txt


echo "circos pipe"
perl /rhome/cjinfeng/software/tools/circos/circos-0.64/bin/circos -conf circos.test2.conf
python CircosConf.py --input circos.config --output pipe.conf

echo "MSU7"
mkdir MSU7 
cd MSU7
perl ../scripts/PreDraw.pl --repeat_gff MSU_r7.fa.RepeatMasker.out.gff --gene_gff MSU7.gene.gff --chrlen MSU7.chrlen
python ../../CircosConf.py --input circos.config --output pipe.conf

