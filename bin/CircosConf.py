#!/opt/Python/2.7.3/bin/python
import sys
import re
import os
import argparse

def usage():
    test="name"
    message='''
python CircosConf.py --input circos.config --output pipe.conf

Produce Conf file for circos and run circos (Based on circos v0.64 2 May 2013).
Config file format:
###############################
#Config file for circos Wrapper
#1. chromosome file, which contains chromosome name and length, will be used to create a karyotype file
#Format: Chr01	43270923
#2. feature, like histogram, highlight and heatmap used to display in circos
#Format histogram: chr01 0 99999 16.575
#Format highlight: chr01 40180 57658 fill_color=red
#Format heatmap: chr01 0 4999999 80510.000000 
#########################################
#File	Type	Color	BackgroundColor	Min	Max	Rank
circos.chrlen	chromosome	NA	0	0	0	0
Rice.RT.histogram.txt	histogram	green	1	0	80	5
Rice.exon.histogram.txt	histogram	orange	0	0	24	5
Rice.RT.histogram.txt	heatmap	NA	0	0	80	4
Rice.exon.histogram.txt	heatmap	NA	0	0	24	3
Rice.RT.histogram.txt	line	vdorange	0	0	80	4
Rice.exon.histogram.txt	line	vdorange	0	0	24	3
contract.highlight.txt	highlight	red	0	0	0	2
expand.highlight.txt	highlight	blue	0	0	0	1

    '''
    print message

def ideogram(chrp):
    ideo='''
<ideogram>

<spacing>

default = 1u  #    0.05r
break   = 0r   # 0.35r

<pairwise Chr12;Chr1>
spacing = 5u
</pairwise>

axis_break_at_edge = no
axis_break         = no
#axis_break_style   = 2

<break_style 1>
stroke_color = black
fill_color   = blue
thickness    = 0r
stroke_thickness = 0
</break>

<break_style 2>
stroke_color     = black
stroke_thickness = 0
thickness        = 0r
</break>

</spacing>

# thickness (px) of chromosome ideogram
thickness        = 100p
stroke_thickness = 0r
# ideogram border color
  stroke_color     =  white #   chr18
fill             = no
# the default chromosome color is set here and any value
# defined in the karyotype file overrides it
fill_color       =    white #  chr18

# fractional radius position of chromosome ideogram within image
radius         = 0.4r
show_label     = yes
label_with_tag = yes
label_font     = condensedbold
label_radius   = '''+chrp+'''r
label_size     = 40p
label_parallel = yes
label_center   = no
rotation       = 180
label_rotate   = yes

# cytogenetic bands
band_stroke_thickness = 0

# show_bands determines whether the outline of cytogenetic bands will be seen
show_bands            = no
# in order to fill the bands with the color defined in the karyotype file you must set fill_bands
fill_bands            = no

</ideogram>
'''
    with open('pipe.ideogram.conf','w') as ideofh:
        ideofh.write(ideo)

def tick(tickp):
    tick='''
show_ticks          = yes
show_tick_labels    = yes

<ticks>
skip_first_label     = no
skip_last_label      = no
radius               = '''+tickp+'''r
multiplier = 1e-6
color = black

<tick>
spacing        = 5u
size           = 10p
thickness      = 2p
color          = black
show_label     = no
label_size     = 8p
label_offset   = 0p
format         = %d
grid           = yes
grid_color     = grey
grid_thickness = 1p
</tick>

<tick>
skip_first_label     = yes
spacing        = 10u
size           = 20p
thickness      = 2p
color          = black
show_label     = yes
label_size     = 30p
label_offset   = 10p
format         = %d
grid           = yes
grid_color     = dgrey
grid_thickness = 1p
</tick>

<tick>

position       = 0.01u
label          = 0 (Mb)
show_label     = yes
label_offset   = 10p
label_size     = 30p
size           = 20p
color          = black
thickness      = 2p
format         = %d
grid           = yes
grid_color     = dgrey
grid_thickness = 1p

</tick>

</ticks>
'''
    with open('pipe.ticks.conf','w') as tickfh:
        tickfh.write(tick)
 

def header(ideogram,ticks, karyotype):
    header='''
karyotype   = '''+karyotype+'''

chromosomes_units = 1000000
chromosomes_display_default = yes
chromosomes = Chr1;Chr2;Chr3;Chr4;Chr5;Chr6;Chr7;Chr8;Chr9;Chr10;Chr11;Chr12

######################################################################
<<include '''+ideogram+'''>>
<<include '''+ticks+'''>>
####################################################################
'''
    return header

def image(png):
    image='''
################################################################
# The remaining content is standard and required. It is imported from
# default files in the Circos distribution.

<image>

dir = ./
file  = '''+png+'''
svg = yes
png = yes
24bit = yes
# radius of inscribed circle in image
radius         = 1500p
background     = white
# by default angle=0 is at 3 o'clock position
angle_offset   = -88
#transparent
auto_alpha_colors = yes
auto_alpha_steps = 40

</image>

# RGB/HSV color definitions, color lists, location of fonts
<<include etc/colors_fonts_patterns.conf>> 
<<include etc/brewer.conf>>
<colors>
greent   = 51,204,94,0.8
oranget  = 253,141,60,0.8
</colors>

# Debugging, I/O an dother system parameters
# Included from Circos distribution.
<<include etc/housekeeping.conf>>
'''
    return image

def link():
    linkfile=""
    link='''
chromosomes_units = 1000000
chromosomes_display_default = yes
chromosomes = chr01;chr02;chr03;chr04;chr05;chr06;chr07;chr08;chr09;chr10;chr11;chr12

<links>
z      = 10
radius = 0.9r
crest  = 0.7
bezier_radius = 0.1r

<link segdup>
show = yes
thickness = 2
file = '''+linkfile+'''

</link>

</links>
'''
    return link

def plot(hist,style,color,minx,maxx,r0,r1,bg):
    plot='''

<plot>

file = '''+hist+'''
type = '''+style+'''

r0 = '''+r0+'''r
r1 = '''+r1+'''r

min='''+minx+'''
max='''+maxx+'''

'''

    heatcolor='''
color = spectral-9-div-rev

</plot>

'''
    histcolor='''
color     = '''+color+'''
fill_under = yes
fill_color = '''+color+'''
thickness = 2

extend_bin = no

''' 
    nobackground='''

</plot>

'''
    background='''

<backgrounds>
<background>
color = vvlgrey
</background>
</backgrounds>

</plot>

'''
    linecolor='''

color     = '''+color+'''
thickness = 5

</plot>

''' 
 
    if style == 'histogram':
        if bg == '1':
            plot = plot + histcolor + background
        else:
            plot = plot + histcolor + nobackground
    elif style == 'heatmap':
        plot = plot + heatcolor
    elif style == 'line':
        plot = plot + linecolor
    return plot

def highlight(hlight,r0,r1):
    highlight='''

<highlight>
file = '''+hlight+'''
r0 = '''+r0+'''r
r1 = '''+r1+'''r
</highlight>

'''
    return highlight

def karyotype(chrlen,karyo):
    kline=[]
    with open (chrlen,'r') as length:
        chrs=length.readlines()
        for c in chrs:
            c=c.rstrip()
            cs=c.split('\t')
            s = re.compile(r'^\w+')
            if s.search(c):
                s = re.compile(r'\d+')
                ss= s.search(cs[0])
                chrnum=ss.group(0)
                s = re.compile(r'(?<=0)\d+')
                ss = s.search(chrnum)
                if ss:
                    chrnum = ss.group(0)
                line = 'chr - '+cs[0]+' '+cs[0]+' 0 '+cs[1]+' chr'+chrnum
                kline.append(line)
    with open (karyo, 'w') as kfile:
        for l in kline:
            kfile.write(l+'\n') 

def circos(config, circosconf):
    binh = 0.15
    bini = 0.05
    tickp = 0
    chrp  = 0
    plots=[]
    highlights=[]
    with open(config, 'r') as configfh:
        hist=configfh.readlines()
        for line in hist:
            line=line.rstrip()
            feild=line.split('\t')
            s = re.compile(r'^\w+')
            if s.search(line):
                if feild[1] == 'histogram' or feild[1] == 'heatmap' or feild[1] == 'line':
                    histfile = feild[0]
                    style    = feild[1]
                    color    = feild[2]
                    bgcolor  = feild[3]
                    minx     = feild[4]
                    maxx     = feild[5]
                    rank     = feild[6]
                    r0       = str(1 + bini * int (rank) + binh * ( int (rank) - 1))
                    r1       = str(float(r0) + binh)
                    if float (r1) > tickp:
                        tickp = float (r1)
                        chrp  = tickp + 0.15
                    print rank, r0, r1
                    plots.append(plot(histfile,style,color,minx,maxx,r0,r1,bgcolor))
                elif feild[1] == 'highlight':
                    highfile = feild[0]
                    rank     = feild[6]
                    r0       = str(1 + bini * int (rank) + binh * ( int (rank) - 1))
                    r1       = str(+ float (r0) + binh)
                    if float (r1) > tickp:
                        tickp = float (r1)
                        chrp  = tickp + 0.15
                    print rank, r0, r1
                    highlights.append(highlight(highfile,r0,r1))
                elif feild[1] == 'chromosome':
                    chrlen   = feild[0]
                    karyotype(chrlen,'pipe.karyotype')

    ideogram(str(chrp))
    tick(str(tickp)) 
    with open (circosconf,'w') as conf:
        conf.write(header('pipe.ideogram.conf','pipe.ticks.conf','pipe.karyotype'))
        conf.write('<plots>')
        for p in plots:
            conf.write(p)
        conf.write('</plots>\n')
        if len(highlights) > 1: 
            conf.write('<highlights>')
            for h in highlights:
                conf.write(h)
            conf.write('</highlights>\n')
        conf.write(image('pipe.circos.png'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.output) > 0
    except:
        usage()
        sys.exit(2)

    circos(args.input,args.output)
    os.system('perl /rhome/cjinfeng/software/tools/circos/circos-0.64/bin/circos -conf pipe.conf')

if __name__ == '__main__':
    main()

