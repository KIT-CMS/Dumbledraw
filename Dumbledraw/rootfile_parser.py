#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import ROOT
import copy
import yaml
from array import array

logger = logging.getLogger(__name__)

def get_custom_binning(era, channel, tag, category):
    cat_dict = {
         '1': "Pt20to25", '2': "Pt25to30", '3': "Pt30to35", '4': "Pt35to40", '5': "PtGt40",
         '6': "Inclusive", '7': "DM0", '8': "DM1", '9': "DM1011", '10': "DM10", '11': "DM11",
         '12': "DM0_PT20_40", '13': "DM1_PT20_40", '14': "DM1011_PT20_40", '15': "DM10_PT20_40", 
         '16': "DM11_PT20_40", '17': "DM0_PT40_200", '18': "DM1_PT40_200", '19': "DM1011_PT40_200", 
         '20': "DM10_PT40_200", '21': "DM11_PT40_200", '100': "CR"}
    cat = cat_dict[category]
    if era.startswith("Run"):
        era = era.replace("Run", "")
    if tag != "mm":
        yaml_filename = f"/work/jvoss/ntuples/smhtt_ul_SFs/config/gof_binning/binning_{era}_{channel}_{tag}.yaml"
        with open(yaml_filename, "r") as f:
            binning_info = yaml.safe_load(f)
        # The correct key is given by the category value.
        # (Assume that for data_obs the histogram variable is 'm_vis').
        if cat in binning_info and "m_vis" in binning_info[cat] and "bins" in binning_info[cat]["m_vis"]:
            return binning_info[cat]["m_vis"]["bins"]
        else:
            return None
    else:
        return None  # For the 'mm' tag, no custom binning is defined.
    

def convert_tgraph_to_custom_th1(graph, new_name, era, channel, tag, cat):
    custom_binning = get_custom_binning(era, channel, tag, cat)
    if custom_binning is None:
        # If no custom binning is found, fall back on a default conversion.
        n_points = graph.GetN()
        x_vals = graph.GetX()
        x_min = x_vals[0] - graph.GetErrorXlow(0)
        x_max = x_vals[n_points - 1] + graph.GetErrorXhigh(n_points - 1)
        new_hist = ROOT.TH1F(new_name, new_name, n_points, x_min, x_max)
        for i in range(n_points):
            bin_center = x_vals[i]
            bin_content = graph.GetY()[i]
            bin_error = graph.GetErrorYhigh(i)
            bin_index = new_hist.FindBin(bin_center)
            new_hist.SetBinContent(bin_index, bin_content)
            new_hist.SetBinError(bin_index, bin_error)
        return new_hist
    else:
        nbins = len(custom_binning) - 1
        # Create a histogram with the fixed bin edges from the YAML file.
        new_hist = ROOT.TH1F(new_name, new_name, nbins, array('d', custom_binning))
        n_points = graph.GetN()
        x_vals = graph.GetX()
        y_vals = graph.GetY()
        # Loop over each graph point and fill the corresponding bin.
        for i in range(n_points):
            bin_center = x_vals[i]
            bin_index = new_hist.FindBin(bin_center)
            # In case multiple points fall into the same bin, you may need to sum.
            new_hist.SetBinContent(bin_index, y_vals[i])
            new_hist.SetBinError(bin_index, graph.GetErrorYhigh(i))
        return new_hist

class Rootfile_parser(object):
    def __init__(self, inputrootfilename, mode="CombineHarvester", prefit=False, tag=None):
        self._rootfilename = inputrootfilename
        self._rootfile = ROOT.TFile(self._rootfilename, "READ")
        self._tag = tag
        self._type = "control"
        content = [entry.GetName() for entry in self._rootfile.GetListOfKeys()]
        for entry in content:
            if entry.endswith("prefit"):
                self._type = "prefit"
        if not prefit:
            for entry in content:
                if entry.endswith("postfit"):
                    self._type = "postfit"
        logger.debug(
            "Identified rootfile %s as %s shapes" % (inputrootfilename, self._type)
        )
        if mode == "standard":
            self._hist_hash = "{channel}_{category}{plottype}/{process}{unc}"
        elif mode == "CombineHarvester":
            self._hist_hash = "htt_{channel}_{category}_{era}{plottype}/{process}{unc}"
        else:
            logger.fatal("Cannot detect mode to open file {}.".format(mode))
            raise Exception
        logger.debug("Use mode {} to read file.".format(mode))

    @property
    def rootfile(self):
        return self._rootfile

    def get(self, era, channel, category, process, syst=None):
        if syst != None and self._type != "control":
            logger.fatal("Uncertainty shapes are only available in control plots!")
            raise Exception
        hist_hash = self._hist_hash.format(
            era=era,
            channel=channel,
            category=category,
            process=process,
            plottype="{plottype}",
            unc="{unc}",
        )
        if self._type == "control":
            syst = "" if syst == None else "_" + syst
            hist_hash = hist_hash.format(plottype="", unc=syst)
        else:
            hist_hash = hist_hash.format(plottype="_" + self._type, unc="")
        logger.debug("Try to access %s in %s" % (hist_hash, self._rootfilename))
        # perform check if file is available and otherwise return some dummy TH1F
        available_processes = [
            entry.GetName()
            for entry in self._rootfile.Get(hist_hash.split("/")[0]).GetListOfKeys()
        ]
        if hist_hash.split("/")[1] in available_processes:
            return self._rootfile.Get(hist_hash)
        elif len(available_processes) != 0:
            logger.warning(
                "%s in %s does not exist !" % (hist_hash, self._rootfilename)
            )
            logger.debug("Available Histograms are: %s" % available_processes)
            logger.debug("Returning a dummy histogram")
            dummy = self._rootfile.Get(
                "{}/{}".format(hist_hash.split("/")[0], available_processes[0])
            )
            # Instead of converting the TGraphAsymmErrors object,
            # check its type. If it is a TGraphAsymmErrors, return it as-is,
            # preserving the special binning (perhaps defined in your YAML file).
            if dummy.InheritsFrom("TGraphAsymmErrors"):
                logger.debug("Dummy is a TGraphAsymmErrors; converting to TH1F using special binning")
                dummy = convert_tgraph_to_custom_th1(dummy, hist_hash, era, channel, self._tag, category)
            else:
                dummy.Reset()
            dummy.SetTitle(process)
            dummy.SetName(hist_hash)
            return dummy
        else:
            logger.fatal(
                "None of the requested Histograms are available in %s. Aborting."
                % hist_hash.split("/")[0]
            )
            raise Exception

    def get_bins(self, era, channel, category, process, syst=None):
        hist = self.get(era, channel, category, process, syst)
        nbins = hist.GetNbinsX()
        bins = []
        for i in range(nbins):
            bins.append(hist.GetBinLowEdge(i + 1))
        bins.append(hist.GetBinLowEdge(i + 1) + hist.GetBinWidth(i + 1))
        return bins

    def get_values(self, era, channel, category, process, syst=None):
        hist = self.get(era, channel, category, process, syst)
        nbins = hist.GetNbinsX()
        values = []
        for i in range(nbins):
            values.append(hist.GetBinContent(i + 1))
        return values

    def get_values_up(self, era, channel, category, process, syst=None):
        hist = self.get(era, channel, category, process, syst)
        nbins = hist.GetNbinsX()
        values = []
        for i in range(nbins):
            values.append(hist.GetBinErrDown(i + 1))
        return values

    def get_values_down(self, era, channel, category, process, syst=None):
        hist = self.get(era, channel, category, process, syst)
        nbins = hist.GetNbinsX()
        values = []
        for i in range(nbins):
            values.append(hist.GetBinErrDown(i + 1))
        return values

    def __del__(self):
        logger.debug("Closing rootfile %s" % (self._rootfilename))
        self._rootfile.Close()
