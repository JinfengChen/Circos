#!/opt/Python/2.7.3/bin/python
import sys
import re
import argparse

def usage():
    test="name"
    message='''
    python CircosConf.py --input circos.config --output test
    Produce Conf file for circos: test
    '''
    print message

def ideogram():
    ideo='''
<ideogram>

<spacing>

default = 1u  #    0.05r
break   = 0r   # 0.35r
#<pairwise Foc1_chr01;Foc4_chr01>
#spacing = 200u
#</pairwise>

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
label_radius   = 1.8r
label_size     = 40p
label_parallel = yes
label_center   = no

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

def tick():
    tick='''
show_ticks          = yes
show_tick_labels    = yes

<ticks>
skip_first_label     = no
skip_last_label      = no
radius               = 1.65r
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
spacing        = 10u
size           = 20p
thickness      = 2p
color          = black
show_label     = yes
label_size     = 30p
label_offset   = 0p
format         = %d
grid           = yes
grid_color     = dgrey
grid_thickness = 1p
</tick>

<tick>
show           = yes
position       = start
size           = 20p
label_size     = 30p
label_offset   =0p
label          = 0'
color          = black
suffix         = Mb
format         = %s
thickness      = 2p
show_label     = yes
</tick>

</ticks>
'''
    with open('pipe.ticks.conf','w') as tickfh:
        tickfh.write(tick)
 

def header():
    header='''
karyotype   = circos.karyotype

chromosomes_units = 1000000
chromosomes_display_default = yes
chromosomes = chr01;chr02;chr03;chr04;chr05;chr06;chr07;chr08;chr09;chr10;chr11;chr12

######################################################################
<<include ideogram.conf>>
<<include ticks.conf>>
####################################################################
'''
    return header

def image():
    image='''
################################################################
# The remaining content is standard and required. It is imported from
# default files in the Circos distribution.

<image>

dir = ./
file  = circos.SD.png
svg = yes
png = yes
24bit = yes
# radius of inscribed circle in image
radius         = 1500p
background     = white
# by default angle=0 is at 3 o'clock position
angle_offset   = -90
#transparent
auto_alpha_colors = yes
auto_alpha_steps = 40

</image>

# RGB/HSV color definitions, color lists, location of fonts
<<include etc/colors_fonts_patterns.conf>> 
<<include etc/brewer.conf>>

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

def plot(hist,style,color,minx,maxx,r0,r1):
    plot='''

<plot>

file = '''+hist+'''
type = '''+style+'''

r0 = '''+r0+'''
r1 = '''+r1+'''

min='''+minx+'''
max='''+maxx
    heatcolor='''
color = spectral-9-div-rev
'''
    histcolor='''
color     = '''+color+'''
fill_under = yes
fill_color = '''+color+'''
thickness = 2

extend_bin = no

<backgrounds>
<background>
color = vvlgrey
</background>
</backgrounds>

</plot>

'''
    if style == 'histogram':
        plot = plot + histcolor
    else:
        plot = plot + heatcolor
    return plot

def highlight(hlight,r0,r1):
    highlight='''

<highlight>
file = '''+hlight+'''
r0 = '''+r0+'''
r1 = '''+r1+'''
</highlight>

'''
    return highlight

def circos(config):
    binh = 0.15
    bini = 0.05
    plots=[]
    highlights=[]
    with open(config, 'r') as configfh:
        hist=configfh.readlines()
        for line in hist:
            line=line.rstrip()
            feild=line.split('\t')
            s = re.compile(r'^\w+')
            if s.search(line):
                print line
'''
            if feild[1] == 'histogram' or feild[1] == 'heatmap':
                histfile = feild[0]
                style    = feild[1]
                color    = feild[2]
                minx     = feild[3]
                maxx     = feild[4]
                rank     = feild[5]
                r0       = bini*rank + binh*(rank-1)
                r1       = r0+binh
                plots.append(plot(histfile,style,color,minx,maxx,r0,r1))
            elif feild[1] == 'highlight':
                highfile = feild[0]
                rank     = feild[5]
                r0       = bini*rank + binh*(rank-1)
                r1       = r0+binh             
    with open (args.output,'w') as conf:
        conf.write(header())
        conf.write('<plots>')
        for p in plots:
            conf.write(p)
        conf.write('</plots>')
        for h in highlights:
            conf.write(h)
        conf.write(image())
'''     

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

    #print header()
    #print image()
    #print link()
    #print highlight()
    ideogram()
    tick()
    circos(args.input)

if __name__ == '__main__':
    main()

