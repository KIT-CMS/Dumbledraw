#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import ROOT
import copy

logger = logging.getLogger(__name__)


class Rootfile_parser(object):

    _dataset_map = {
        "data": "data",
        "ZTT": "DY",
        "ZL": "DY",
        "ZJ": "DY",
        "ZTT_NLO": "DYNLO",
        "ZL_NLO": "DYNLO",
        "ZJ_NLO": "DYNLO",
        "TTT": "TT",
        "TTL": "TT",
        "TTJ": "TT",
        "STT": "ST",
        "STL": "ST",
        "STJ": "ST",
        "VVT": "VV",
        "VVL": "VV",
        "VVJ": "VV",
        "W": "W",
        "W_NLO": "WNLO",
        "EMB": "EMB",
        "QCDEMB": "QCD",
        "QCD": "QCDMC",
        "jetFakesEMB": "jetFakes",
        "jetFakes": "jetFakesMC",
        "QCDEMB_NLO": "QCD_NLO",
        "QCD_NLO": "QCDMC_NLO",
        "jetFakesEMB_NLO": "jetFakes_NLO",
        "jetFakes_NLO": "jetFakesMC_NLO",
        "ggH125": "ggH",
        "qqH125": "qqH",
        "VH": "VH",
        "ggH_tt": "ggH_tt",
        "qqH_tt": "qqH_tt",
        "VH_tt": "VH_tt",
        "ggH_bb": "ggH_bb",
        "qqH_bb": "qqH_bb",
        "VH_bb": "VH_bb",
        "EWK": "EWK",
        "wFakes": "wFakes",
        "nmssm_Ybb": "nmssm_Ybb",
        "nmssm_Ytautau": "nmssm_Ytautau",
    }

    _process_map = {
        "data": "data",
        "ZTT": "DY-ZTT",
        "ZL": "DY-ZL",
        "ZJ": "DY-ZJ",
        "ZTT_NLO": "DY_NLO-ZTT",
        "ZL_NLO": "DY_NLO-ZL",
        "ZJ_NLO": "DY_NLO-ZJ",
        "TTT": "TT-TTT",
        "TTL": "TT-TTL",
        "TTJ": "TT-TTJ",
        "STT": "ST-STT",
        "STL": "ST-STL",
        "STJ": "ST-STJ",
        "VVT": "VV-VVT",
        "VVL": "VV-VVL",
        "VVJ": "VV-VVJ",
        "W": "W",
        "W_NLO": "W",
        "EMB": "Embedded",
        "QCDEMB": "QCD",
        "QCD": "QCDMC",
        "QCDEMB_NLO": "QCD_NLO",
        "QCD_NLO": "QCDMC_NLO",
        "jetFakesEMB": "jetFakes",
        "jetFakes": "jetFakesMC",
        "ggH125": "ggH125",
        "qqH125": "qqH125",
        "VH": "VH125",
        "ggH_tt": "ggH125",
        "qqH_tt": "qqH125",
        "VH_tt": "VH125",
        "ggH_bb": "ggH125",
        "qqH_bb": "qqH125",
        "VH_bb": "VH125",
        "EWK": "EVK",
        "wFakes": "wFakes",
        "nmssm_Ybb": "NMSSM_Ybb",
        "nmssm_Ytautau": "NMSSM_Ytt",
    }

    def __init__(self, inputrootfilename, variable, tt_boosted):
        self._rootfilename = inputrootfilename
        self._rootfile = ROOT.TFile(self._rootfilename, "READ")
        self._variable = variable
        self._tt_boosted = tt_boosted

    @property
    def rootfile(self):
        return self._rootfile

    def get(self, channel, process, category=None, shape_type="Nominal", analysis_plots=False):
        dataset = self._dataset_map[process]
        if category is None:
            category = "" if "data" in process else "-" + self._process_map[process]
        else:
            category = (
                "-" + category
                if "data" in process
                else "-" + "-".join([self._process_map[process], category])
            )
        if analysis_plots:
            appendix = ""
            if self._tt_boosted:
                appendix = "_boosted"
            category = category + f"-{self._variable}"
            hist_hash = "{dataset}#{channel}{category}#{shape_type}#{variable}".format(
                dataset=dataset,
                channel=channel,
                category=category,
                shape_type=shape_type,
                variable="mt_score"+appendix,
            )
        else:
            hist_hash = "{dataset}#{channel}{category}#{shape_type}#{variable}".format(
                dataset=dataset,
                channel=channel,
                category=category,
                shape_type=shape_type,
                variable=self._variable,
            )
        logger.debug("Try to access %s in %s" % (hist_hash, self._rootfilename))
        print("rootfile: ", self._rootfile.Get(hist_hash), " hash: ", hist_hash)

        return self._rootfile.Get(hist_hash)

    def list_contents(self):
        return [key.GetTitle() for key in self._rootfile.GetListOfKeys()]

    def get_bins(self, channel, category):
        hist = self.get(channel, category)
        nbins = hist.GetNbinsX()
        bins = []
        for i in range(nbins):
            bins.append(hist.GetBinLowEdge(i + 1))
        bins.append(hist.GetBinLowEdge(i + 1) + hist.GetBinWidth(i + 1))
        return bins

    def get_values(self, channel, category):
        hist = self.get(channel, category)
        nbins = hist.GetNbinsX()
        values = []
        for i in range(nbins):
            values.append(hist.GetBinContent(i + 1))
        return values

    def __del__(self):
        logger.debug("Closing rootfile %s" % (self._rootfilename))
        self._rootfile.Close()
