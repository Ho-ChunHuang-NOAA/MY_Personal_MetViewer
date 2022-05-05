import sys
import datetime
import shutil
import os 
import subprocess
import fnmatch

###METviewer_AWS_scripts_dir = "/gpfs/hps3/emc/global/noscrub/Mallory.Row/VRFY/METviewer_AWS"
###METviewer_AWS_scripts_dir = "/gpfs/hps3/emc/meso/save/Ho-Chun.Huang/METviewer_AWS"
METviewer_AWS_scripts_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/METviewer_AWS/script"
MODIS_dust_obs_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/aod_dust/conc/aquamodis."
MET_verif_out_dir = "/gpfs/dell2/emc/modeling/noscrub/Ho-Chun.Huang/com/verif/prod/hysplitdust."

obs_fhead = "MYDdust.aod_conc.v6.3.4."
obs_ftail = ".grib"

stat_var = "me"
stat_var = "aod"
stat_var = "rmse"
stat_var = "csi"

if stat_var == "aod":
    plot_var = "hysplit_dust_time_series"
else:
    plot_var = "hysplit_dust_"+stat_var.lower()

### PASSED AGRUEMENTS
if len(sys.argv) < 7:
    print("you must set 5 arguments as area title_area [day1|day2] start_date end_date run_cycle csi_thresh")
    sys.exit()
else:
    area = sys.argv[1]
    label_area = sys.argv[2]
    verf_day_id = sys.argv[3]
    start_date = sys.argv[4]
    end_date = sys.argv[5]
    verf_cycle_id=sys.argv[6]
    csi_thresh=sys.argv[7]
sdate = datetime.datetime(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:]), 00)
edate = datetime.datetime(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:]), 23)
date_inc = datetime.timedelta(hours=24)
hour_inc = datetime.timedelta(hours=1)
val_date_format = "%Y-%m-%d %H:%M:%S"
lbl_date_format = "%d"
title_date_format = "%Y%m%d"
title_time_format = "%m%d"
title_hour_format = "%H"
database_date_format = "%Y%m"
database_date = sdate.strftime(database_date_format)
tmp_data_dir="/gpfs/dell2/stmp/Ho-Chun.Huang/working/check_fcst_lead_daily_"+database_date
if os.path.exists(tmp_data_dir):
    shutil.rmtree(tmp_data_dir)
os.makedirs(tmp_data_dir)

ymax="0.00001"
ymax="1.0"
ymin="0.0"
ybuf="0.01"
ybuf="0.04"
models = [ "hysplitdustprod" ]
lend_mdl = [ "PROD" ]
lend_obs = [ "OBS" ]
regs = [ "FULL", "G236", "G245", "G246" ]
ymax="0.2"
if verf_cycle_id == "12Z":
   hour_cycle=12
elif verf_cycle_id == "06Z":
   hour_cycle=6
else:
    print("verification cycle hour "+verf_cycle_id+" not recongized.")
    exit()
if verf_day_id == "day1":
    vhour_beg = 1
    vhour_end = 24
elif verf_day_id == "day2":
    vhour_beg = 25
    vhour_end = 48
else:
    print("verification day "+verf_day_id+" not recongized.")
    exit()
vhour_inc = 1
print("{0:0>2}".format(vhour_beg)+"  "+str(vhour_end))

### CREATE PLOT XML
### for area in regs:
###    xml.write("                    <val>"+area+"</val>\n")
plot_xml_file = os.path.join(os.path.join(os.getcwd(), "plot_"+plot_var+"_daily.xml"))
print("2) Creating plot xml "+plot_xml_file)
if os.path.exists(plot_xml_file):
    os.remove(plot_xml_file)
with open(plot_xml_file, 'a') as xml:
    xml.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
    xml.write("<plot_spec>\n")
    xml.write("    <connection>\n")
    xml.write("        <host>rds_host:3306</host>\n")
    xml.write("        <database>mv_hysplit_dust"+database_date+"_grid2grid_metplus</database>\n")
    xml.write("        <user>rds_user</user>\n")
    xml.write("        <password>rds_pwd</password>\n")
    ### xml.write("        <management_system>aurora</management_system>\n")
    xml.write("    </connection>\n")
    xml.write("    <rscript>Rscript</rscript>\n")
    xml.write("    <folders>\n")
    xml.write("        <r_tmpl>rds_R_tmpl</r_tmpl>\n")
    xml.write("        <r_work>rds_R_work</r_work>\n")
    xml.write("        <plots>rds_plots</plots>\n")
    xml.write("        <data>rds_data</data>\n")
    xml.write("        <scripts>rds_scripts</scripts>\n")
    xml.write("    </folders>\n")
    xml.write("    <plot>\n")
    xml.write("        <template>series_plot.R_tmpl</template>\n")
    xml.write("        <dep>\n")
    xml.write("            <dep1>\n")
    xml.write("                <fcst_var name=\"LIPMF\">\n")
    xml.write("                    <stat>"+stat_var.upper()+"</stat>\n")
    xml.write("                </fcst_var>\n")
    xml.write("            </dep1>\n")
    xml.write("            <dep2/>\n")
    xml.write("        </dep>\n")
    xml.write("        <series1>\n")
    xml.write("            <field name=\"model\">\n")
    for model in models:
        xml.write("                <val>"+model.upper()+"</val>\n")
    xml.write("            </field>\n")
    xml.write("        </series1>\n")
    xml.write("        <series2/>\n")
    xml.write("        <plot_fix>\n")
    xml.write("            <field equalize=\"false\" name=\"vx_mask\">\n")
    xml.write("                <set name=\"vx_mask_0\">\n")
    if area == "NEUS":
        xml.write("                    <val>APL</val>\n")
        xml.write("                    <val>NEC</val>\n")
    elif area == "SEUS":
        xml.write("                    <val>GMC</val>\n")
        xml.write("                    <val>LMV</val>\n")
        xml.write("                    <val>SEC</val>\n")
    elif area == "NWUS":
        xml.write("                    <val>NMT</val>\n")
        xml.write("                    <val>NPL</val>\n")
        xml.write("                    <val>NWC</val>\n")
    elif area == "SWUS":
        xml.write("                    <val>GRB</val>\n")
        xml.write("                    <val>SMT</val>\n")
        xml.write("                    <val>SWC</val>\n")
        xml.write("                    <val>SWD</val>\n")
    else:
        xml.write("                    <val>"+area+"</val>\n")
    xml.write("                </set>\n")
    xml.write("            </field>\n")
    xml.write("            <field equalize=\"false\" name=\"fcst_lead\">\n")
    xml.write("                <set name=\"fcst_lead_1\">\n")
    date = sdate
    while date <= edate:
        verifout=MET_verif_out_dir+date.strftime(title_date_format)+"/hysplitdust_prod_"+date.strftime(title_date_format)+".stat.tar"
        if os.path.isfile(verifout):
            shutil.copy(verifout, tmp_data_dir)
            os.chdir(tmp_data_dir)
            subprocess.call(["/usr/bin/tar", "-xf", verifout])
        else:
            print("Can not find "+verifout)
        date = date + date_inc
    os.chdir(tmp_data_dir)
    vhour = vhour_beg
    while vhour <= vhour_end:
        search_index="*F"+"{0:0>2}".format(vhour)+"*"
        for file in os.listdir(tmp_data_dir):
            if fnmatch.fnmatch(file, search_index):
                xml.write("                    <val>"+str(vhour)+"0000</val>\n")
                break
        vhour = vhour + vhour_inc
    xml.write("                </set>\n")
    xml.write("            </field>\n")
    xml.write("            <field equalize=\"false\" name=\"obs_thresh\">\n")
    xml.write("                <set name=\"obs_thresh_2\">\n")
    xml.write("            <val label=\"&gt;"+csi_thresh+"\" plot_val=\"\">&gt;"+csi_thresh+"</val>\n")
    xml.write("                </set>\n")
    xml.write("            </field>\n")
    xml.write("            <field equalize=\"false\" name=\"fcst_valid_beg\">\n")
    xml.write("                <set name=\"fcst_valid_beg_3\">\n")
    date = sdate
    while date <= edate:
        obs_dir=MODIS_dust_obs_dir+date.strftime(title_date_format)
        if os.path.exists(obs_dir):
            obsfile=os.path.join(obs_dir, obs_fhead+date.strftime(title_date_format)+".hr"+date.strftime(title_hour_format)+obs_ftail)
            if os.path.isfile(obsfile):
                val_date = date.strftime(val_date_format)
                label_date = date.strftime(lbl_date_format)
                xml.write("                    <val>"+val_date+"</val>\n")
        else:
            print("Can not find "+obs_dir)
        date = date + hour_inc
    xml.write("                </set>\n")
    xml.write("            </field>\n")
    xml.write("        </plot_fix>\n")
    xml.write("        <plot_cond/>\n")
    xml.write("        <indep equalize=\"false\" name=\"fcst_init_beg\">\n")
    date = sdate
    while date <= edate:
        if date.hour == hour_cycle:
            val_date = date.strftime(val_date_format)
            label_date = date.strftime(lbl_date_format)
            xml.write("            <val label=\""+label_date+"\" plot_val=\"\">"+val_date+"</val>\n")
        date = date + hour_inc
    xml.write("        </indep>\n")
    xml.write("        <agg_stat>\n")
    xml.write("            <agg_ctc>true</agg_ctc>\n")
    xml.write("            <boot_repl>1</boot_repl>\n")
    xml.write("            <boot_random_seed/>\n")
    xml.write("            <boot_ci>perc</boot_ci>\n")
    xml.write("            <eveq_dis>false</eveq_dis>\n")
    xml.write("            <cache_agg_stat>false</cache_agg_stat>\n")
    xml.write("        </agg_stat>\n")
    xml.write("        <plot_stat>median</plot_stat>\n")
    xml.write("        <tmpl>\n")
    xml.write("            <data_file>"+label_area+"_"+plot_var.upper()+"_"+verf_day_id.upper()+"_"+verf_cycle_id.upper()+"_"+sdate.strftime(database_date_format)+"_"+csi_thresh+".data</data_file>\n")
    xml.write("            <plot_file>"+label_area+"_"+plot_var.upper()+"_"+verf_day_id.upper()+"_"+verf_cycle_id.upper()+"_"+sdate.strftime(database_date_format)+"_"+csi_thresh+".png</plot_file>\n")
    xml.write("            <r_file>plot_"+label_area+"_"+plot_var.upper()+"_"+verf_day_id.upper()+"_"+verf_cycle_id.upper()+".R</r_file>\n")
    xml.write("            <title>MET_"+plot_var.upper()+"_Verification_"+verf_day_id.upper()+"_"+verf_cycle_id.upper()+"_"+database_date+" - "+label_area+"</title>\n")
    xml.write("            <x_label>Day of the month</x_label>\n")
    xml.write("            <y1_label>"+stat_var.upper()+"</y1_label>\n")
    xml.write("            <y2_label/>\n")
    xml.write("            <caption/>\n")
    xml.write("            <job_title>plot_"+label_area+"_"+plot_var.upper()+"_"+verf_day_id.upper()+"_"+verf_cycle_id.upper()+"_"+database_date+"_"+csi_thresh+"</job_title>\n")
    xml.write("            <keep_revisions>false</keep_revisions>\n")
    xml.write("            <listdiffseries1>list()</listdiffseries1>\n")
    xml.write("            <listdiffseries2>list()</listdiffseries2>\n")
    xml.write("        </tmpl>\n")
    xml.write("        <execution_type>Python</execution_type>\n")
    xml.write("        <event_equal>false</event_equal>\n")
    xml.write("        <vert_plot>false</vert_plot>\n")
    xml.write("        <x_reverse>false</x_reverse>\n")
    xml.write("        <num_stats>false</num_stats>\n")
    xml.write("        <indy1_stag>false</indy1_stag>\n")
    xml.write("        <indy2_stag>false</indy2_stag>\n")
    xml.write("        <grid_on>true</grid_on>\n")
    xml.write("        <sync_axes>false</sync_axes>\n")
    xml.write("        <dump_points1>true</dump_points1>\n")
    xml.write("        <dump_points2>false</dump_points2>\n")
    xml.write("        <log_y1>false</log_y1>\n")
    xml.write("        <log_y2>false</log_y2>\n")
    xml.write("        <varianceinflationfactor>false</varianceinflationfactor>\n")
    xml.write("        <plot_type>png16m</plot_type>\n")
    xml.write("        <plot_height>8.5</plot_height>\n")
    xml.write("        <plot_width>11</plot_width>\n")
    xml.write("        <plot_res>72</plot_res>\n")
    xml.write("        <plot_units>in</plot_units>\n")
    xml.write("        <mar>c(8,4,5,4)</mar>\n")
    xml.write("        <mgp>c(1,1,0)</mgp>\n")
    xml.write("        <cex>1</cex>\n")
    xml.write("        <title_weight>2</title_weight>\n")
    xml.write("        <title_size>1.4</title_size>\n")
    xml.write("        <title_offset>-2</title_offset>\n")
    xml.write("        <title_align>0.5</title_align>\n")
    xml.write("        <xtlab_orient>3</xtlab_orient>\n")
    xml.write("        <xtlab_perp>0.5</xtlab_perp>\n")
    xml.write("        <xtlab_horiz>0.8</xtlab_horiz>\n")
    xml.write("        <xtlab_freq>0</xtlab_freq>\n")
    xml.write("        <xtlab_size>1.5</xtlab_size>\n")
    xml.write("        <xlab_weight>1</xlab_weight>\n")
    xml.write("        <xlab_size>1.5</xlab_size>\n")
    xml.write("        <xlab_offset>2</xlab_offset>\n")
    xml.write("        <xlab_align>0.5</xlab_align>\n")
    xml.write("        <ytlab_orient>1</ytlab_orient>\n")
    xml.write("        <ytlab_perp>0.5</ytlab_perp>\n")
    xml.write("        <ytlab_horiz>0.65</ytlab_horiz>\n")
    xml.write("        <ytlab_size>1.5</ytlab_size>\n")
    xml.write("        <ylab_weight>1</ylab_weight>\n")
    xml.write("        <ylab_size>2</ylab_size>\n")
    xml.write("        <ylab_offset>-1.2</ylab_offset>\n")
    xml.write("        <ylab_align>0.5</ylab_align>\n")
    xml.write("        <grid_lty>3</grid_lty>\n")
    xml.write("        <grid_col>#cccccc</grid_col>\n")
    xml.write("        <grid_lwd>1</grid_lwd>\n")
    xml.write("        <grid_x>listX</grid_x>\n")
    xml.write("        <x2tlab_orient>1</x2tlab_orient>\n")
    xml.write("        <x2tlab_perp>1</x2tlab_perp>\n")
    xml.write("        <x2tlab_horiz>0.5</x2tlab_horiz>\n")
    xml.write("        <x2tlab_size>0.8</x2tlab_size>\n")
    xml.write("        <x2lab_size>0.8</x2lab_size>\n")
    xml.write("        <x2lab_offset>-0.5</x2lab_offset>\n")
    xml.write("        <x2lab_align>0.5</x2lab_align>\n")
    xml.write("        <y2tlab_orient>1</y2tlab_orient>\n")
    xml.write("        <y2tlab_perp>0.5</y2tlab_perp>\n")
    xml.write("        <y2tlab_horiz>0.5</y2tlab_horiz>\n")
    xml.write("        <y2tlab_size>1</y2tlab_size>\n")
    xml.write("        <y2lab_size>1</y2lab_size>\n")
    xml.write("        <y2lab_offset>1</y2lab_offset>\n")
    xml.write("        <y2lab_align>0.5</y2lab_align>\n")
    xml.write("        <legend_box>n</legend_box>\n")
    xml.write("        <legend_inset>c(0,-0.25)</legend_inset>\n")
    xml.write("        <legend_ncol>1</legend_ncol>\n")
    xml.write("        <legend_size>1</legend_size>\n")
    xml.write("        <caption_weight>1</caption_weight>\n")
    xml.write("        <caption_col>#333333</caption_col>\n")
    xml.write("        <caption_size>0.8</caption_size>\n")
    xml.write("        <caption_offset>3</caption_offset>\n")
    xml.write("        <caption_align>0</caption_align>\n")
    xml.write("        <ci_alpha>0.05</ci_alpha>\n")
    xml.write("        <plot_ci>c(\"none\")</plot_ci>\n")
    xml.write("        <show_signif>c(FALSE)</show_signif>\n")
    xml.write("        <plot_disp>c(TRUE)</plot_disp>\n")
    xml.write("        <colors>c(\"#ff0000FF\")</colors>\n")
    xml.write("        <pch>c(19)</pch>\n")
    xml.write("        <type>c(\"b\")</type>\n")
    xml.write("        <lty>c(1)</lty>\n")
    xml.write("        <lwd>c(2)</lwd>\n")
    xml.write("        <con_series>c(1)</con_series>\n")
    xml.write("        <order_series>c(1)</order_series>\n")
    xml.write("        <plot_cmd/>\n")
    xml.write("        <legend>c(\"OBS Threshold &gt;"+csi_thresh+" ug/m3\")</legend>\n")
    xml.write("        <create_html>FALSE</create_html>\n")
## autoscaling
##    xml.write("        <y1_lim>c()</y1_lim>\n")
    xml.write("        <y1_lim>c("+ymin+","+ymax+")</y1_lim>\n")
    xml.write("        <x1_lim>c()</x1_lim>\n")
    xml.write("        <y1_bufr>"+ybuf+"</y1_bufr>\n")
##    xml.write("        <y1_bufr/>\n")
    xml.write("        <y2_lim>c()</y2_lim>\n")
##    xml.write("        <y2_lim>c("+ymin+","+ymax+")</y2_lim>\n")
    xml.write("    </plot>\n")
    xml.write("</plot_spec>\n")
